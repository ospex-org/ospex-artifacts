#!/usr/bin/env python3
"""Generate Ospex artifact index files from canonical artifacts on disk.

The repository has a lightweight top-level index plus full-history archive
shards. Keeping those files by hand is easy to get wrong, so this script treats
artifact JSON files as the source of truth and rewrites:

- index.json
- archive/YYYY/index.json

Existing entry-level publishedAt values are preserved by dataPath. New artifacts
receive the current UTC time unless the artifact JSON already has a top-level
publishedAt.
"""

from __future__ import annotations

import argparse
import copy
import difflib
import json
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPOSITORY = "ospex-org/ospex-artifacts"
INDEX_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/artifact-index.schema.json"
ARCHIVE_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/artifact-archive.schema.json"

ARTIFACT_TYPES = ("run", "release-acceptance", "daily-digest")
RECENT_ARTIFACT_LIMIT = 100
LATEST_BY_TYPE_LIMIT = 10

ARTIFACT_SOURCES = (
    {
        "artifact_type": "run",
        "glob": "runs/*/evidence.json",
        "summary_name": "summary.md",
    },
    {
        "artifact_type": "release-acceptance",
        "glob": "releases/*/*/acceptance.json",
        "summary_name": "acceptance.md",
    },
    {
        "artifact_type": "daily-digest",
        "glob": "daily/*/digest.json",
        "summary_name": "summary.md",
    },
)

ENTRY_KEY_ORDER = (
    "artifactId",
    "artifactType",
    "dataPath",
    "date",
    "network",
    "rawPath",
    "release",
    "status",
    "summaryPath",
    "publishedAt",
)

ISO_DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-|$)")


class GenerationError(Exception):
    """Raised when artifacts cannot be converted into index entries."""


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_json_if_exists(path: Path) -> Any | None:
    if not path.is_file():
        return None
    return read_json(path)


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def now_utc_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_datetime(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise GenerationError(f"expected ISO date-time string, got {value!r}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise GenerationError(f"invalid ISO date-time {value!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_network(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = value.strip().lower()
    if normalized in {"polygon", "polygon-mainnet", "matic", "matic-mainnet"}:
        return "polygon"
    return value.strip()


def artifact_date(artifact_id: str, doc: dict[str, Any]) -> str | None:
    value = doc.get("date")
    if isinstance(value, str) and value:
        return value
    match = ISO_DATE_PREFIX_RE.match(artifact_id)
    return match.group(1) if match else None


def release_label(doc: dict[str, Any]) -> str | None:
    release = doc.get("release")
    if not isinstance(release, dict):
        return None
    repo = release.get("repo")
    tag = release.get("tag")
    if isinstance(repo, str) and repo and isinstance(tag, str) and tag:
        return f"{repo} {tag}"
    return None


def detect_network(doc: dict[str, Any], artifact_dir: Path) -> str | None:
    direct = normalize_network(doc.get("network"))
    if direct:
        return direct

    for relative in (
        "raw/tx-receipts.summary.json",
        "raw/live-gates.json",
        "raw/setup-gates.json",
        "raw/doctor-after-create.sanitized.json",
        "raw/doctor-after-approvals.sanitized.json",
    ):
        raw_doc = read_json_if_exists(artifact_dir / relative)
        if isinstance(raw_doc, dict):
            found = normalize_network(raw_doc.get("network"))
            if found:
                return found

    chain_id = doc.get("chainId")
    if chain_id == 137:
        return "polygon"
    return None


def existing_entries_by_path() -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}

    candidate_paths = [ROOT / "index.json", *sorted((ROOT / "archive").glob("*/index.json"))]
    for path in candidate_paths:
        doc = read_json_if_exists(path)
        if not isinstance(doc, dict):
            continue
        for key in ("recentArtifacts", "artifacts"):
            values = doc.get(key)
            if not isinstance(values, list):
                continue
            for entry in values:
                if not isinstance(entry, dict):
                    continue
                data_path = entry.get("dataPath")
                if isinstance(data_path, str) and data_path:
                    entries[data_path] = entry
    return entries


def choose_published_at(data_path: str, doc: dict[str, Any], existing: dict[str, dict[str, Any]], fallback_now: str) -> str:
    existing_entry = existing.get(data_path)
    if isinstance(existing_entry, dict) and isinstance(existing_entry.get("publishedAt"), str):
        return existing_entry["publishedAt"]
    if isinstance(doc.get("publishedAt"), str) and doc["publishedAt"]:
        return doc["publishedAt"]
    return fallback_now


def ordered_entry(core: dict[str, Any], existing_entry: dict[str, Any] | None) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key in ENTRY_KEY_ORDER:
        if key in core and core[key] is not None:
            output[key] = core[key]

    if existing_entry:
        for key in sorted(existing_entry):
            if key not in output and key not in core:
                output[key] = existing_entry[key]
    return output


def discover_artifacts(fallback_now: str) -> list[dict[str, Any]]:
    existing = existing_entries_by_path()
    entries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()

    for source in ARTIFACT_SOURCES:
        artifact_type = source["artifact_type"]
        for data_file in sorted(ROOT.glob(source["glob"])):
            doc = read_json(data_file)
            if not isinstance(doc, dict):
                raise GenerationError(f"{rel(data_file)}: artifact JSON must be an object")

            declared_type = doc.get("artifactType")
            if declared_type is not None and declared_type != artifact_type:
                raise GenerationError(f"{rel(data_file)}: artifactType {declared_type!r} does not match path type {artifact_type!r}")

            artifact_dir = data_file.parent
            artifact_id = doc.get("artifactId")
            if not isinstance(artifact_id, str) or not artifact_id:
                artifact_id = artifact_dir.name
            if artifact_id in seen_ids:
                raise GenerationError(f"duplicate artifactId {artifact_id!r}")
            seen_ids.add(artifact_id)

            data_path = rel(data_file)
            if data_path in seen_paths:
                raise GenerationError(f"duplicate artifact dataPath {data_path!r}")
            seen_paths.add(data_path)

            status = doc.get("status")
            if not isinstance(status, str) or not status:
                raise GenerationError(f"{data_path}: missing string status")

            summary_path = rel(artifact_dir / source["summary_name"])
            raw_dir = artifact_dir / "raw"
            raw_path = rel(raw_dir) + "/" if raw_dir.is_dir() else None

            core = {
                "artifactId": artifact_id,
                "artifactType": artifact_type,
                "dataPath": data_path,
                "date": artifact_date(artifact_id, doc),
                "network": detect_network(doc, artifact_dir),
                "rawPath": raw_path,
                "release": release_label(doc),
                "status": status,
                "summaryPath": summary_path,
                "publishedAt": choose_published_at(data_path, doc, existing, fallback_now),
            }
            entries.append(ordered_entry(core, existing.get(data_path)))

    for entry in entries:
        parse_datetime(entry.get("publishedAt"))

    return sorted(
        entries,
        key=lambda entry: (parse_datetime(entry["publishedAt"]), entry["dataPath"]),
        reverse=True,
    )


def preserve_generated_at(path: Path, doc: dict[str, Any]) -> dict[str, Any]:
    existing = read_json_if_exists(path)
    if not isinstance(existing, dict) or not isinstance(existing.get("generatedAt"), str):
        return doc

    candidate = copy.deepcopy(doc)
    candidate["generatedAt"] = existing["generatedAt"]

    existing_without_generated = copy.deepcopy(existing)
    candidate_without_generated = copy.deepcopy(candidate)
    existing_without_generated.pop("generatedAt", None)
    candidate_without_generated.pop("generatedAt", None)

    if existing_without_generated == candidate_without_generated:
        return candidate
    return doc


def build_outputs(generated_at: str, recent_limit: int, latest_limit: int) -> dict[Path, str]:
    if recent_limit < 1:
        raise GenerationError("recent limit must be at least 1")
    if latest_limit < 1:
        raise GenerationError("latest-by-type limit must be at least 1")

    entries = discover_artifacts(generated_at)
    recent_entries = entries[:recent_limit]

    by_year: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        year = parse_datetime(entry["publishedAt"]).year
        by_year[year].append(entry)

    archive_docs: dict[Path, dict[str, Any]] = {}
    archive_indexes: list[dict[str, Any]] = []
    for year in sorted(by_year, reverse=True):
        artifacts = by_year[year]
        archive_path = ROOT / "archive" / str(year) / "index.json"
        archive_doc = {
            "$schema": ARCHIVE_SCHEMA_ID,
            "schemaVersion": 1,
            "generatedAt": generated_at,
            "repository": REPOSITORY,
            "archive": {
                "scope": "year",
                "year": year,
            },
            "artifacts": artifacts,
        }
        archive_doc = preserve_generated_at(archive_path, archive_doc)
        archive_docs[archive_path] = archive_doc

        published = [parse_datetime(entry["publishedAt"]) for entry in artifacts]
        archive_indexes.append(
            {
                "scope": "year",
                "year": year,
                "path": rel(archive_path),
                "artifactCount": len(artifacts),
                "oldestPublishedAt": iso_z(min(published)),
                "newestPublishedAt": iso_z(max(published)),
            }
        )

    latest_by_type = {artifact_type: [] for artifact_type in ARTIFACT_TYPES}
    for entry in entries:
        bucket = latest_by_type[entry["artifactType"]]
        if len(bucket) < latest_limit:
            bucket.append(entry["dataPath"])

    index_doc = {
        "$schema": INDEX_SCHEMA_ID,
        "schemaVersion": 2,
        "generatedAt": generated_at,
        "repository": REPOSITORY,
        "latestByArtifactType": latest_by_type,
        "recentArtifacts": recent_entries,
        "archiveIndexes": archive_indexes,
    }
    index_doc = preserve_generated_at(ROOT / "index.json", index_doc)

    outputs: dict[Path, str] = {ROOT / "index.json": dump_json(index_doc)}
    for path, doc in archive_docs.items():
        outputs[path] = dump_json(doc)
    return outputs


def stale_archive_paths(expected_paths: set[Path]) -> list[Path]:
    archive_root = ROOT / "archive"
    if not archive_root.is_dir():
        return []
    return sorted(path for path in archive_root.glob("*/index.json") if path not in expected_paths)


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, text in sorted(outputs.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    for path in stale_archive_paths(set(outputs)):
        path.unlink()


def check_outputs(outputs: dict[Path, str]) -> int:
    errors = 0
    for path, expected_text in sorted(outputs.items()):
        relative = rel(path)
        if not path.exists():
            print(f"{relative}: missing generated file")
            errors += 1
            continue
        actual_text = path.read_text(encoding="utf-8")
        if actual_text != expected_text:
            print(f"{relative}: not up to date; run python3 scripts/generate-indexes.py")
            diff = difflib.unified_diff(
                actual_text.splitlines(),
                expected_text.splitlines(),
                fromfile=f"{relative} (current)",
                tofile=f"{relative} (generated)",
                lineterm="",
            )
            for line in diff:
                print(line)
            errors += 1
    for path in stale_archive_paths(set(outputs)):
        print(f"{rel(path)}: stale archive index; run python3 scripts/generate-indexes.py")
        errors += 1
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated index files differ from the working tree")
    parser.add_argument(
        "--recent-limit",
        type=int,
        default=RECENT_ARTIFACT_LIMIT,
        help=f"number of entries to keep in index.json recentArtifacts (default: {RECENT_ARTIFACT_LIMIT})",
    )
    parser.add_argument(
        "--latest-limit",
        type=int,
        default=LATEST_BY_TYPE_LIMIT,
        help=f"number of latest data paths to keep per artifact type (default: {LATEST_BY_TYPE_LIMIT})",
    )
    args = parser.parse_args(argv)

    try:
        outputs = build_outputs(now_utc_iso(), args.recent_limit, args.latest_limit)
    except GenerationError as exc:
        print(f"index generation failed: {exc}", file=sys.stderr)
        return 1

    if args.check:
        errors = check_outputs(outputs)
        if errors:
            return 1
        print("Generated index files are up to date.")
        return 0

    write_outputs(outputs)
    print(f"Generated {len(outputs)} index file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
