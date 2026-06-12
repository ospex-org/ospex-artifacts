#!/usr/bin/env python3
"""Validate public Ospex artifact repository data.

This intentionally uses only Python stdlib so GitHub Actions can run it without
fetching package dependencies. It enforces the repository's current schema-backed
contracts, path checks, JSON/NDJSON parse checks, and a conservative public-safety
scan for secrets/local-only material.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

INDEX_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/artifact-index.schema.json"
ARCHIVE_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/artifact-archive.schema.json"
RELEASE_ACCEPTANCE_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/release-acceptance.schema.json"
SCENARIO_MATRIX_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/scenario-matrix.schema.json"
MVE_SCORECARD_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/mve-scorecard.schema.json"

RECENT_ARTIFACT_LIMIT = 100
ARTIFACT_TYPES = ("run", "release-acceptance", "daily-digest")
STATUS_BY_ARTIFACT_TYPE = {
    "run": {"complete_verified", "complete_verified_with_caveats", "partial", "superseded"},
    "release-acceptance": {
        "stage0_green",
        "stage0_green_with_caveats",
        "stage0_partial",
        "stage0_failed",
        "superseded",
    },
    "daily-digest": {"complete", "complete_with_caveats", "partial", "superseded"},
}

TEXT_SUFFIXES = {".json", ".md", ".ndjson", ".txt", ".yml", ".yaml"}
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
TX_HASH_RE = re.compile(r"^0x[a-fA-F0-9]{64}$")
RAW_SIGNATURE_RE = re.compile(r"0x[a-fA-F0-9]{130}\b")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Scenario matrix v2 + MVE readiness scorecard contracts (docs/mm-live-canary-evidence.md).
# These checks apply only to runs that adopt the schema-backed shapes; earlier
# free-form scenario-matrix.json files are grandfathered.
SCENARIO_MATRIX_MIN_VERSION = 2
SCENARIO_STATUSES = {"pass", "pass_with_caveats", "fail", "deferred", "not_run", "not_applicable"}
PROOF_LEVELS = {"proven_live", "proven_synthetic_only", "deferred", "failed", "not_applicable"}
PROVEN_LEVELS = {"proven_live", "proven_synthetic_only"}
VERDICT_LABELS = {
    "FULL_GREEN",
    "GREEN_LIVE_WINDOW_POSTGAME_DEFERRED",
    "AMBER_QUOTED_NO_FILL",
    "AMBER_TOKEN_TOPUP_NEEDED",
    "RED_SAFETY_HALT",
}
# The run status vocabulary has no failure status; failed runs stay internal.
UNPUBLISHABLE_VERDICTS = {"RED_SAFETY_HALT"}
RUN_STATUS_BY_VERDICT = {
    "FULL_GREEN": {"complete_verified", "complete_verified_with_caveats"},
    "GREEN_LIVE_WINDOW_POSTGAME_DEFERRED": {"partial"},
    "AMBER_QUOTED_NO_FILL": {"partial", "complete_verified_with_caveats"},
    "AMBER_TOKEN_TOPUP_NEEDED": {"partial", "complete_verified_with_caveats"},
}
TX_CATEGORIES = {
    "approve",
    "create-contest",
    "seed-match",
    "match-commitment",
    "cancel-commitment",
    "nonce-floor-raise",
    "score-request",
    "score-callback",
    "settle",
    "claim",
    "other",
}
POSTGAME_TX_CATEGORIES = {"score-request", "score-callback", "settle", "claim"}
MM_LIVE_CANARY_CAPABILITY_IDS = {
    "target-preflight",
    "repo-runtime-gates",
    "wallet-auth-balances",
    "bounded-approvals",
    "dry-run-quote-loop",
    "live-commitments-posted",
    "live-fill",
    "own-state-sse-canonical-fill",
    "exposure-drain-zero",
    "restart-cold-start-safety",
    "postgame-score",
    "postgame-settle",
    "postgame-claim",
    "cost-within-cap",
}
POSTGAME_CAPABILITY_IDS = {"postgame-score", "postgame-settle", "postgame-claim"}
FULL_GREEN_CORE_CAPABILITY_IDS = {
    "live-commitments-posted",
    "live-fill",
    "exposure-drain-zero",
    "cost-within-cap",
} | POSTGAME_CAPABILITY_IDS
ZERO_EXPOSURE_COUNT_KEYS = (
    "publicMakerVisibleCommitments",
    "publicContestSpecVisibleCommitments",
    "contestOrderbookCount",
    "orphanProcessCount",
)
TEAM_IDENTITY_POSITION_TYPE_BY_ROLE = {"home": "lower", "away": "upper"}

# Patterns are intentionally specific to reduce false positives from docs that
# describe excluded material. Broad words like "secret" or "password" are not
# failures by themselves; actual secret surfaces and local-only paths are.
SAFETY_PATTERNS = [
    ("private-key marker", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\bPRIVATE_KEY\b", re.I)),
    ("seed phrase marker", re.compile(r"\b(mnemonic|seed phrase)\b\s*[:=]", re.I)),
    ("postgres connection URL", re.compile(r"postgres(?:ql)?://[^\s)\]}>\"']+", re.I)),
    ("authorization header", re.compile(r"\bAuthorization\s*:\s*(Bearer|Basic|token)\b", re.I)),
    ("bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}", re.I)),
    ("API key assignment", re.compile(r"\b(api[_-]?key|supabase[_-]?key|rpc[_-]?url)\b\s*[:=]\s*['\"][^'\"]{8,}", re.I)),
    ("local home path", re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+(?:/|$)")),
    ("ospex secret path", re.compile(r"\.ospex/(?:secrets|wallets|keystores)|\.(?:pass|pem|key)\b", re.I)),
    ("raw EIP-712 signature-sized hex", RAW_SIGNATURE_RE),
    (
        "signature/signedPayload-keyed hex value",
        re.compile(
            r"\"(?:raw)?(?:eip712)?(?:signature|signedPayload|signedMessage|signedTypedData)\"\s*:\s*\"0x[a-fA-F0-9]{8,}",
            re.I,
        ),
    ),
    (
        "specific upstream odds provider name",
        re.compile(r"\b(draftkings|fan\s?duel|betrivers|betmgm|pinnacle|the[- ]odds[- ]api|sportradar)\b", re.I),
    ),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def display_path(path: Path) -> str:
    try:
        return rel(path)
    except ValueError:
        return path.as_posix()


def is_under_repo(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
        return True
    except ValueError:
        return False


def iter_repo_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        files.append(path)
    return files


def parse_datetime_value(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed


def parse_datetime(value: Any) -> bool:
    return parse_datetime_value(value) is not None


def parse_date(value: Any) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def is_plain_int(value: Any) -> bool:
    return type(value) is int


def check_relative_path(path_value: Any, *, base: Path, errors: list[str], context: str, expect_dir: bool = False) -> None:
    if path_value is None:
        return
    if not isinstance(path_value, str) or not path_value:
        errors.append(f"{context}: path must be a non-empty string")
        return
    posix = PurePosixPath(path_value)
    if posix.is_absolute() or ".." in posix.parts:
        errors.append(f"{context}: path must stay inside repo/artifact directory: {path_value!r}")
        return
    target = (base / Path(path_value)).resolve()
    if not is_under_repo(target):
        errors.append(f"{context}: path escapes repo: {path_value!r}")
        return
    if expect_dir or path_value.endswith("/"):
        if not target.is_dir():
            errors.append(f"{context}: directory does not exist: {path_value}")
    elif not target.is_file():
        errors.append(f"{context}: file does not exist: {path_value}")


def parse_json_files(files: list[Path], errors: list[str]) -> dict[Path, Any]:
    docs: dict[Path, Any] = {}
    for path in sorted(p for p in files if p.suffix == ".json"):
        try:
            docs[path] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report any parse/read failure.
            errors.append(f"{rel(path)}: invalid JSON: {exc}")
    return docs


def parse_ndjson_files(files: list[Path], errors: list[str]) -> int:
    count = 0
    for path in sorted(p for p in files if p.suffix == ".ndjson"):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            count += 1
            try:
                json.loads(line)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{rel(path)}:{line_no}: invalid NDJSON line: {exc}")
    return count


def validate_schema_files(docs: dict[Path, Any], errors: list[str]) -> None:
    schema_ids: dict[str, Path] = {}
    for path, doc in docs.items():
        if not path.name.endswith(".schema.json"):
            continue
        if not isinstance(doc, dict):
            errors.append(f"{rel(path)}: schema must be a JSON object")
            continue
        schema_id = doc.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            errors.append(f"{rel(path)}: schema is missing $id")
        elif schema_id in schema_ids:
            errors.append(f"{rel(path)}: duplicate schema $id also used by {rel(schema_ids[schema_id])}")
        else:
            schema_ids[schema_id] = path


def validate_artifact_entry(
    artifact: Any,
    *,
    context: str,
    docs: dict[Path, Any],
    errors: list[str],
    seen_ids: set[str] | None = None,
) -> str | None:
    if not isinstance(artifact, dict):
        errors.append(f"{context}: must be an object")
        return None
    for key in ["artifactType", "artifactId", "status", "publishedAt", "summaryPath", "dataPath"]:
        if key not in artifact:
            errors.append(f"{context}: missing required key {key!r}")
    artifact_type = artifact.get("artifactType")
    artifact_id = artifact.get("artifactId")
    status = artifact.get("status")
    published_at = artifact.get("publishedAt")

    if artifact_type not in STATUS_BY_ARTIFACT_TYPE:
        errors.append(f"{context}: unsupported artifactType {artifact_type!r}")
    elif status not in STATUS_BY_ARTIFACT_TYPE[artifact_type]:
        allowed = ", ".join(sorted(STATUS_BY_ARTIFACT_TYPE[artifact_type]))
        errors.append(f"{context}: status {status!r} is not allowed for {artifact_type}; expected one of: {allowed}")
    if not isinstance(artifact_id, str) or not artifact_id:
        errors.append(f"{context}: artifactId must be a non-empty string")
    elif seen_ids is not None:
        if artifact_id in seen_ids:
            errors.append(f"{context}: duplicate artifactId {artifact_id}")
        else:
            seen_ids.add(artifact_id)
    if not parse_datetime(published_at):
        errors.append(f"{context}: publishedAt must be an ISO date-time")
    if not parse_date(artifact.get("date")):
        errors.append(f"{context}: date must be YYYY-MM-DD or null")

    check_relative_path(artifact.get("summaryPath"), base=ROOT, errors=errors, context=f"{context}.summaryPath")
    check_relative_path(artifact.get("dataPath"), base=ROOT, errors=errors, context=f"{context}.dataPath")
    check_relative_path(artifact.get("rawPath"), base=ROOT, errors=errors, context=f"{context}.rawPath", expect_dir=True)

    data_path_value = artifact.get("dataPath")
    if isinstance(data_path_value, str):
        data_path = (ROOT / data_path_value).resolve()
        data_doc = docs.get(data_path)
        if isinstance(data_doc, dict):
            if "artifactType" in data_doc and data_doc["artifactType"] != artifact_type:
                errors.append(
                    f"{context}: artifactType {artifact_type!r} disagrees with {data_path_value} value {data_doc['artifactType']!r}"
                )
            if "status" in data_doc and data_doc["status"] != status:
                errors.append(f"{context}: status {status!r} disagrees with {data_path_value} value {data_doc['status']!r}")
    return data_path_value if isinstance(data_path_value, str) else None


def validate_published_order(entries: list[Any], *, context: str, errors: list[str]) -> None:
    previous: datetime | None = None
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        parsed = parse_datetime_value(entry.get("publishedAt"))
        if parsed is None:
            continue
        if previous is not None and parsed > previous:
            errors.append(f"{context}: entries must be sorted by publishedAt descending; item {idx} is newer than item {idx - 1}")
        previous = parsed


def validate_index(index_path: Path, docs: dict[Path, Any], errors: list[str]) -> None:
    doc = docs.get(index_path)
    if not isinstance(doc, dict):
        errors.append("index.json: must be a JSON object")
        return

    allowed_top = {"$schema", "schemaVersion", "generatedAt", "repository", "latestByArtifactType", "recentArtifacts", "archiveIndexes"}
    for key in doc:
        if key not in allowed_top:
            errors.append(f"index.json: unexpected top-level key {key!r}")

    required = ["$schema", "schemaVersion", "generatedAt", "repository", "latestByArtifactType", "recentArtifacts", "archiveIndexes"]
    for key in required:
        if key not in doc:
            errors.append(f"index.json: missing required key {key!r}")

    if doc.get("$schema") != INDEX_SCHEMA_ID:
        errors.append(f"index.json: $schema must be {INDEX_SCHEMA_ID}")
    if doc.get("schemaVersion") != 2:
        errors.append("index.json: schemaVersion must be 2")
    if not parse_datetime(doc.get("generatedAt")):
        errors.append("index.json: generatedAt must be an ISO date-time")
    if doc.get("repository") != "ospex-org/ospex-artifacts":
        errors.append("index.json: repository must be ospex-org/ospex-artifacts")

    recent = doc.get("recentArtifacts")
    if not isinstance(recent, list):
        errors.append("index.json: recentArtifacts must be an array")
        recent = []
    elif len(recent) > RECENT_ARTIFACT_LIMIT:
        errors.append(f"index.json: recentArtifacts must stay within the recent-N cap of {RECENT_ARTIFACT_LIMIT}")
    validate_published_order(recent, context="index.json recentArtifacts", errors=errors)

    seen_recent_ids: set[str] = set()
    recent_by_path: dict[str, dict[str, Any]] = {}
    for idx, artifact in enumerate(recent):
        data_path = validate_artifact_entry(
            artifact,
            context=f"index.json recentArtifacts[{idx}]",
            docs=docs,
            errors=errors,
            seen_ids=seen_recent_ids,
        )
        if data_path and isinstance(artifact, dict):
            recent_by_path[data_path] = artifact

    latest = doc.get("latestByArtifactType")
    if not isinstance(latest, dict):
        errors.append("index.json: latestByArtifactType must be an object")
    else:
        if set(latest) != set(ARTIFACT_TYPES):
            errors.append("index.json: latestByArtifactType keys must exactly match artifactType values: run, release-acceptance, daily-digest")
        for artifact_type in ARTIFACT_TYPES:
            values = latest.get(artifact_type)
            if not isinstance(values, list):
                errors.append(f"index.json latestByArtifactType.{artifact_type}: must be an array")
                continue
            for item_idx, value in enumerate(values):
                context = f"index.json latestByArtifactType.{artifact_type}[{item_idx}]"
                check_relative_path(value, base=ROOT, errors=errors, context=context)
                entry = recent_by_path.get(value) if isinstance(value, str) else None
                if entry is None:
                    errors.append(f"{context}: latest pointer must also appear in recentArtifacts")
                elif entry.get("artifactType") != artifact_type:
                    errors.append(f"{context}: points to {entry.get('artifactType')!r}, expected {artifact_type!r}")

    archives = doc.get("archiveIndexes")
    archive_paths: set[str] = set()
    if not isinstance(archives, list):
        errors.append("index.json: archiveIndexes must be an array")
        archives = []
    for idx, archive in enumerate(archives):
        context = f"index.json archiveIndexes[{idx}]"
        if not isinstance(archive, dict):
            errors.append(f"{context}: must be an object")
            continue
        for key in ["scope", "year", "path", "artifactCount", "oldestPublishedAt", "newestPublishedAt"]:
            if key not in archive:
                errors.append(f"{context}: missing required key {key!r}")
        if archive.get("scope") != "year":
            errors.append(f"{context}: scope must be 'year'")
        if not is_plain_int(archive.get("year")):
            errors.append(f"{context}: year must be an integer")
        if not is_plain_int(archive.get("artifactCount")) or archive.get("artifactCount", -1) < 0:
            errors.append(f"{context}: artifactCount must be an integer >= 0")
        for key in ["oldestPublishedAt", "newestPublishedAt"]:
            if not parse_datetime(archive.get(key)):
                errors.append(f"{context}: {key} must be an ISO date-time")
        path_value = archive.get("path")
        check_relative_path(path_value, base=ROOT, errors=errors, context=f"{context}.path")
        if isinstance(path_value, str):
            archive_paths.add(path_value)
            archive_doc = docs.get((ROOT / path_value).resolve())
            if isinstance(archive_doc, dict):
                archive_entries = archive_doc.get("artifacts")
                if isinstance(archive_entries, list):
                    if archive.get("artifactCount") != len(archive_entries):
                        errors.append(f"{context}: artifactCount {archive.get('artifactCount')} disagrees with {path_value} count {len(archive_entries)}")
                    published = [parse_datetime_value(e.get("publishedAt")) for e in archive_entries if isinstance(e, dict)]
                    published = [p for p in published if p is not None]
                    if published:
                        first = min(published).isoformat().replace("+00:00", "Z")
                        last = max(published).isoformat().replace("+00:00", "Z")
                        if archive.get("oldestPublishedAt") != first:
                            errors.append(f"{context}: oldestPublishedAt must match oldest artifact publishedAt in {path_value}")
                        if archive.get("newestPublishedAt") != last:
                            errors.append(f"{context}: newestPublishedAt must match newest artifact publishedAt in {path_value}")

    archive_data_paths: set[str] = set()
    for path, archive_doc in docs.items():
        if rel(path) in archive_paths and isinstance(archive_doc, dict):
            for entry in archive_doc.get("artifacts", []):
                if isinstance(entry, dict) and isinstance(entry.get("dataPath"), str):
                    archive_data_paths.add(entry["dataPath"])
    for data_path in recent_by_path:
        if data_path not in archive_data_paths:
            errors.append(f"index.json: recent artifact {data_path} is missing from archiveIndexes")


def validate_archive_index(path: Path, doc: Any, docs: dict[Path, Any], errors: list[str]) -> None:
    context = rel(path)
    if not isinstance(doc, dict):
        errors.append(f"{context}: must be a JSON object")
        return
    allowed_top = {"$schema", "schemaVersion", "generatedAt", "repository", "archive", "artifacts"}
    for key in doc:
        if key not in allowed_top:
            errors.append(f"{context}: unexpected top-level key {key!r}")
    for key in ["$schema", "schemaVersion", "generatedAt", "repository", "archive", "artifacts"]:
        if key not in doc:
            errors.append(f"{context}: missing required key {key!r}")
    if doc.get("$schema") != ARCHIVE_SCHEMA_ID:
        errors.append(f"{context}: $schema must be {ARCHIVE_SCHEMA_ID}")
    if not is_plain_int(doc.get("schemaVersion")) or doc.get("schemaVersion", 0) < 1:
        errors.append(f"{context}: schemaVersion must be an integer >= 1")
    if not parse_datetime(doc.get("generatedAt")):
        errors.append(f"{context}: generatedAt must be an ISO date-time")
    if doc.get("repository") != "ospex-org/ospex-artifacts":
        errors.append(f"{context}: repository must be ospex-org/ospex-artifacts")

    archive = doc.get("archive")
    if not isinstance(archive, dict):
        errors.append(f"{context}: archive must be an object")
    else:
        if archive.get("scope") != "year":
            errors.append(f"{context}: archive.scope must be 'year'")
        if not is_plain_int(archive.get("year")):
            errors.append(f"{context}: archive.year must be an integer")
        expected_path = f"archive/{archive.get('year')}/index.json"
        if is_plain_int(archive.get("year")) and rel(path) != expected_path:
            errors.append(f"{context}: year archive must live at {expected_path}")

    artifacts = doc.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append(f"{context}: artifacts must be an array")
        return
    validate_published_order(artifacts, context=f"{context} artifacts", errors=errors)
    seen_ids: set[str] = set()
    for idx, artifact in enumerate(artifacts):
        validate_artifact_entry(artifact, context=f"{context} artifacts[{idx}]", docs=docs, errors=errors, seen_ids=seen_ids)


def validate_release_acceptance(path: Path, doc: Any, errors: list[str]) -> None:
    context = rel(path)
    if not isinstance(doc, dict):
        errors.append(f"{context}: must be a JSON object")
        return
    for key in ["$schema", "artifactType", "schemaVersion", "status", "release", "setupGates", "liveGates", "artifactFiles"]:
        if key not in doc:
            errors.append(f"{context}: missing required key {key!r}")
    if doc.get("$schema") != RELEASE_ACCEPTANCE_SCHEMA_ID:
        errors.append(f"{context}: $schema must be {RELEASE_ACCEPTANCE_SCHEMA_ID}")
    if doc.get("artifactType") != "release-acceptance":
        errors.append(f"{context}: artifactType must be release-acceptance")
    if not is_plain_int(doc.get("schemaVersion")) or doc.get("schemaVersion", 0) < 1:
        errors.append(f"{context}: schemaVersion must be an integer >= 1")
    if doc.get("status") not in STATUS_BY_ARTIFACT_TYPE["release-acceptance"]:
        allowed = ", ".join(sorted(STATUS_BY_ARTIFACT_TYPE["release-acceptance"]))
        errors.append(f"{context}: status {doc.get('status')!r} must be one of: {allowed}")

    release = doc.get("release")
    if not isinstance(release, dict):
        errors.append(f"{context}: release must be an object")
    else:
        for key in ["repo", "tag", "url", "assets"]:
            if key not in release:
                errors.append(f"{context}: release missing {key!r}")
        if release.get("publishedAt") is not None and not parse_datetime(release.get("publishedAt")):
            errors.append(f"{context}: release.publishedAt must be an ISO date-time or null")
        assets = release.get("assets")
        if not isinstance(assets, list):
            errors.append(f"{context}: release.assets must be an array")
        else:
            for idx, asset in enumerate(assets):
                if not isinstance(asset, dict):
                    errors.append(f"{context}: release.assets[{idx}] must be an object")
                    continue
                if not isinstance(asset.get("name"), str) or not asset.get("name"):
                    errors.append(f"{context}: release.assets[{idx}].name must be a non-empty string")
                if not isinstance(asset.get("sha256"), str) or not SHA256_RE.match(asset["sha256"]):
                    errors.append(f"{context}: release.assets[{idx}].sha256 must be a 64-character hex digest")

    for gates_key in ["setupGates", "liveGates"]:
        gates = doc.get(gates_key)
        if not isinstance(gates, dict):
            errors.append(f"{context}: {gates_key} must be an object")
        else:
            for gate_name, gate_value in gates.items():
                if not isinstance(gate_value, (str, int, float, bool)) and gate_value is not None:
                    errors.append(f"{context}: {gates_key}.{gate_name} must be scalar or null")

    txs = doc.get("txs", [])
    if not isinstance(txs, list):
        errors.append(f"{context}: txs must be an array when present")
    else:
        for idx, tx in enumerate(txs):
            if not isinstance(tx, dict):
                errors.append(f"{context}: txs[{idx}] must be an object")
                continue
            for key in ["purpose", "transactionHash", "success"]:
                if key not in tx:
                    errors.append(f"{context}: txs[{idx}] missing {key!r}")
            if not isinstance(tx.get("transactionHash"), str) or not TX_HASH_RE.match(tx["transactionHash"]):
                errors.append(f"{context}: txs[{idx}].transactionHash must be a 0x-prefixed 32-byte hash")
            if not isinstance(tx.get("success"), bool):
                errors.append(f"{context}: txs[{idx}].success must be boolean")

    artifact_files = doc.get("artifactFiles")
    if not isinstance(artifact_files, dict):
        errors.append(f"{context}: artifactFiles must be an object")
    else:
        for key, value in artifact_files.items():
            check_relative_path(value, base=path.parent, errors=errors, context=f"{context} artifactFiles.{key}")


def validate_projection_convergence(path: Path, doc: Any, errors: list[str]) -> None:
    if not isinstance(doc, dict):
        return
    projection = doc.get("projectionConvergence")
    if projection is None:
        return

    try:
        context = rel(path)
    except ValueError:
        context = path.as_posix()

    if not isinstance(projection, dict):
        errors.append(f"{context}: projectionConvergence must be an object")
        return

    expectation = projection.get("expectation")
    if not isinstance(expectation, str) or not expectation.strip():
        errors.append(f"{context}: projectionConvergence.expectation must be a non-empty string")

    gates = projection.get("gates")
    if not isinstance(gates, list) or not gates:
        errors.append(f"{context}: projectionConvergence.gates must be a non-empty array")
        return

    required_gate_keys = [
        "name",
        "afterWrite",
        "txConfirmed",
        "waitTarget",
        "expectedFinalState",
        "observedFinalState",
        "converged",
    ]
    for idx, gate in enumerate(gates):
        gate_context = f"{context}: projectionConvergence.gates[{idx}]"
        if not isinstance(gate, dict):
            errors.append(f"{gate_context} must be an object")
            continue
        for key in required_gate_keys:
            if key not in gate:
                errors.append(f"{gate_context} missing required key {key!r}")
        for key in ["name", "afterWrite", "waitTarget"]:
            if key in gate and (not isinstance(gate[key], str) or not gate[key].strip()):
                errors.append(f"{gate_context}.{key} must be a non-empty string")
        for key in ["txConfirmed", "converged"]:
            if key in gate and not isinstance(gate[key], bool):
                errors.append(f"{gate_context}.{key} must be boolean")
        if "staleReadObserved" in gate and not isinstance(gate["staleReadObserved"], bool):
            errors.append(f"{gate_context}.staleReadObserved must be boolean when present")
        for key in ["expectedFinalState", "observedFinalState"]:
            if key not in gate:
                continue
            value = gate[key]
            if not isinstance(value, list) or not value:
                errors.append(f"{gate_context}.{key} must be a non-empty array")
                continue
            for item_idx, item in enumerate(value):
                if not isinstance(item, str) or not item.strip():
                    errors.append(f"{gate_context}.{key}[{item_idx}] must be a non-empty string")


def validate_raw_file_maps(path: Path, doc: Any, errors: list[str]) -> None:
    if not isinstance(doc, dict):
        return
    if doc.get("artifactType") != "odds-stream-monitor":
        return
    files_map = doc.get("files")
    if files_map is None:
        return
    context = rel(path)
    if not isinstance(files_map, dict):
        errors.append(f"{context}: files must be an object when present")
        return
    for key, value in files_map.items():
        check_relative_path(value, base=path.parent, errors=errors, context=f"{context} files.{key}")


def scenario_matrix_is_v2(doc: Any) -> bool:
    return (
        isinstance(doc, dict)
        and is_plain_int(doc.get("schemaVersion"))
        and doc["schemaVersion"] >= SCENARIO_MATRIX_MIN_VERSION
    )


def validate_scenario_matrix(path: Path, doc: Any, errors: list[str]) -> None:
    """Validate schema-backed (v2+) scenario matrices. Earlier free-form shapes are grandfathered."""
    if not scenario_matrix_is_v2(doc):
        return
    context = display_path(path)
    artifact_dir = path.parent

    if doc.get("$schema") != SCENARIO_MATRIX_SCHEMA_ID:
        errors.append(f"{context}: $schema must be {SCENARIO_MATRIX_SCHEMA_ID}")
    if doc.get("artifactId") != artifact_dir.name:
        errors.append(f"{context}: artifactId must equal the artifact directory name {artifact_dir.name!r}")
    if not parse_datetime(doc.get("generatedAt")):
        errors.append(f"{context}: generatedAt must be an ISO date-time")
    run_class = doc.get("runClass")
    if not isinstance(run_class, str) or not run_class.strip():
        errors.append(f"{context}: runClass must be a non-empty string")

    scenarios = doc.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append(f"{context}: scenarios must be a non-empty array")
        return
    seen_ids: set[str] = set()
    for idx, row in enumerate(scenarios):
        row_context = f"{context}: scenarios[{idx}]"
        if not isinstance(row, dict):
            errors.append(f"{row_context} must be an object")
            continue
        for key in ["id", "scenario", "status", "notes"]:
            if key not in row:
                errors.append(f"{row_context} missing required key {key!r}")
        row_id = row.get("id")
        if isinstance(row_id, str) and SLUG_RE.match(row_id):
            if row_id in seen_ids:
                errors.append(f"{row_context}: duplicate scenario id {row_id!r}")
            seen_ids.add(row_id)
        elif "id" in row:
            errors.append(f"{row_context}: id must be a kebab-case slug")
        for key in ["scenario", "notes"]:
            if key in row and (not isinstance(row[key], str) or not row[key].strip()):
                errors.append(f"{row_context}.{key} must be a non-empty string")
        status = row.get("status")
        if "status" in row and status not in SCENARIO_STATUSES:
            allowed = ", ".join(sorted(SCENARIO_STATUSES))
            errors.append(f"{row_context}: status {status!r} must be one of: {allowed}")
        evidence = row.get("evidence")
        if evidence is None:
            if status in {"pass", "pass_with_caveats", "fail"}:
                errors.append(f"{row_context}: evidence is required when status is {status!r}")
        else:
            check_relative_path(evidence, base=artifact_dir, errors=errors, context=f"{row_context}.evidence")


def validate_team_identity(context: str, target: dict[str, Any], errors: list[str]) -> None:
    identity = target.get("teamIdentity")
    if not isinstance(identity, dict):
        errors.append(f"{context}: moneyline target requires a teamIdentity object with home and away entries")
        return
    identities: dict[str, str] = {}
    teams: dict[str, str] = {}
    for role, expected_position in TEAM_IDENTITY_POSITION_TYPE_BY_ROLE.items():
        entry = identity.get(role)
        entry_context = f"{context}: teamIdentity.{role}"
        if not isinstance(entry, dict):
            errors.append(f"{entry_context} must be an object")
            continue
        team = entry.get("team")
        if not isinstance(team, str) or not team.strip():
            errors.append(f"{entry_context}.team must be a non-empty string")
        else:
            teams[role] = team
        if entry.get("positionType") != expected_position:
            errors.append(f"{entry_context}.positionType must be {expected_position!r} for the {role} side")
        odds = entry.get("marketOddsAmerican")
        if not isinstance(odds, str) or not odds.strip():
            errors.append(f"{entry_context}.marketOddsAmerican must be a non-empty string")
        side_identity = entry.get("identity")
        if side_identity not in {"favorite", "underdog", "even"}:
            errors.append(f"{entry_context}.identity must be favorite, underdog, or even")
        else:
            identities[role] = side_identity
    if len(teams) == 2 and teams["home"] == teams["away"]:
        errors.append(f"{context}: teamIdentity home and away teams must differ")
    if len(identities) == 2:
        pair = sorted(identities.values())
        if pair not in (["favorite", "underdog"], ["even", "even"]):
            errors.append(f"{context}: teamIdentity identities must pair favorite/underdog or even/even")


def validate_adopting_run_evidence(
    scorecard_path: Path,
    evidence_doc: dict[str, Any],
    verdict_label: str | None,
    errors: list[str],
) -> None:
    context = display_path(scorecard_path.parent / "evidence.json")

    artifact_files = evidence_doc.get("artifactFiles")
    referenced = set(artifact_files.values()) if isinstance(artifact_files, dict) else set()
    for required_value in ["scenario-matrix.json", "mve-scorecard.json"]:
        if required_value not in referenced:
            errors.append(f"{context}: artifactFiles must reference {required_value}")

    status = evidence_doc.get("status")
    if verdict_label in RUN_STATUS_BY_VERDICT:
        allowed = RUN_STATUS_BY_VERDICT[verdict_label] | {"superseded"}
        if status not in allowed:
            errors.append(
                f"{context}: status {status!r} does not match scorecard verdict {verdict_label}; "
                "expected one of: " + ", ".join(sorted(allowed))
            )

    evidence_verdict = evidence_doc.get("verdict")
    if verdict_label and isinstance(evidence_verdict, dict) and "label" in evidence_verdict:
        if evidence_verdict.get("label") != verdict_label:
            errors.append(f"{context}: verdict.label must equal the scorecard verdict label {verdict_label!r}")

    target = evidence_doc.get("target")
    if isinstance(target, dict) and target.get("market") == "moneyline":
        validate_team_identity(context, target, errors)


def validate_mve_scorecard(path: Path, doc: Any, docs: dict[Path, Any], errors: list[str]) -> None:
    context = display_path(path)
    if not isinstance(doc, dict):
        errors.append(f"{context}: must be a JSON object")
        return
    artifact_dir = path.parent

    required_keys = [
        "$schema",
        "schemaVersion",
        "artifactId",
        "generatedAt",
        "runClass",
        "verdict",
        "capabilities",
        "zeroExposure",
        "transactions",
    ]
    for key in required_keys:
        if key not in doc:
            errors.append(f"{context}: missing required key {key!r}")
    if doc.get("$schema") != MVE_SCORECARD_SCHEMA_ID:
        errors.append(f"{context}: $schema must be {MVE_SCORECARD_SCHEMA_ID}")
    if not is_plain_int(doc.get("schemaVersion")) or doc.get("schemaVersion", 0) < 1:
        errors.append(f"{context}: schemaVersion must be an integer >= 1")
    if doc.get("artifactId") != artifact_dir.name:
        errors.append(f"{context}: artifactId must equal the artifact directory name {artifact_dir.name!r}")
    if not parse_datetime(doc.get("generatedAt")):
        errors.append(f"{context}: generatedAt must be an ISO date-time")
    run_class = doc.get("runClass")
    if not isinstance(run_class, str) or not run_class.strip():
        errors.append(f"{context}: runClass must be a non-empty string")

    verdict_label: str | None = None
    verdict = doc.get("verdict")
    if "verdict" in doc:
        if not isinstance(verdict, dict):
            errors.append(f"{context}: verdict must be an object")
        else:
            label = verdict.get("label")
            if label not in VERDICT_LABELS:
                allowed = ", ".join(sorted(VERDICT_LABELS))
                errors.append(f"{context}: verdict.label {label!r} must be one of: {allowed}")
            elif label in UNPUBLISHABLE_VERDICTS:
                errors.append(
                    f"{context}: verdict.label {label!r} is not publishable; the run status vocabulary has no "
                    "failure status, so halted/failed canary evidence stays internal"
                )
            else:
                verdict_label = label
            reason = verdict.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{context}: verdict.reason must be a non-empty string")

    proof_by_id: dict[str, str] = {}
    seen_capability_ids: set[str] = set()
    capabilities = doc.get("capabilities")
    if "capabilities" in doc:
        if not isinstance(capabilities, list) or not capabilities:
            errors.append(f"{context}: capabilities must be a non-empty array")
        else:
            for idx, row in enumerate(capabilities):
                row_context = f"{context}: capabilities[{idx}]"
                if not isinstance(row, dict):
                    errors.append(f"{row_context} must be an object")
                    continue
                for key in ["id", "capability", "proof", "notes"]:
                    if key not in row:
                        errors.append(f"{row_context} missing required key {key!r}")
                row_id = row.get("id")
                if isinstance(row_id, str) and SLUG_RE.match(row_id):
                    if row_id in seen_capability_ids:
                        errors.append(f"{row_context}: duplicate capability id {row_id!r}")
                    seen_capability_ids.add(row_id)
                elif "id" in row:
                    errors.append(f"{row_context}: id must be a kebab-case slug")
                    row_id = None
                for key in ["capability", "notes"]:
                    if key in row and (not isinstance(row[key], str) or not row[key].strip()):
                        errors.append(f"{row_context}.{key} must be a non-empty string")
                proof = row.get("proof")
                if "proof" in row and proof not in PROOF_LEVELS:
                    allowed = ", ".join(sorted(PROOF_LEVELS))
                    errors.append(f"{row_context}: proof {proof!r} must be one of: {allowed}")
                elif isinstance(row_id, str) and isinstance(proof, str):
                    proof_by_id[row_id] = proof
                evidence = row.get("evidence")
                if evidence is None:
                    if proof in PROVEN_LEVELS or proof == "failed":
                        errors.append(f"{row_context}: evidence is required when proof is {proof!r}")
                else:
                    check_relative_path(evidence, base=artifact_dir, errors=errors, context=f"{row_context}.evidence")

    if run_class == "mm-live-canary" and isinstance(capabilities, list) and capabilities:
        missing = sorted(MM_LIVE_CANARY_CAPABILITY_IDS - set(proof_by_id))
        if missing:
            errors.append(f"{context}: mm-live-canary scorecard is missing capability rows: {', '.join(missing)}")

        exposure_proof = proof_by_id.get("exposure-drain-zero")
        if exposure_proof is not None and exposure_proof != "proven_live":
            errors.append(f"{context}: exposure-drain-zero must be proven_live in every published scorecard")

        failed_ids = sorted(cid for cid, proof in proof_by_id.items() if proof == "failed")
        if verdict_label in {"FULL_GREEN", "GREEN_LIVE_WINDOW_POSTGAME_DEFERRED"} and failed_ids:
            errors.append(f"{context}: verdict {verdict_label} cannot carry failed capabilities: {', '.join(failed_ids)}")
        if verdict_label == "FULL_GREEN":
            unproven = sorted(
                cid
                for cid in FULL_GREEN_CORE_CAPABILITY_IDS
                if cid in proof_by_id and proof_by_id[cid] not in PROVEN_LEVELS
            )
            if unproven:
                errors.append(f"{context}: verdict FULL_GREEN requires proven core capabilities; not proven: {', '.join(unproven)}")
        if verdict_label == "GREEN_LIVE_WINDOW_POSTGAME_DEFERRED":
            not_deferred = sorted(
                cid for cid in POSTGAME_CAPABILITY_IDS if cid in proof_by_id and proof_by_id[cid] != "deferred"
            )
            if not_deferred:
                errors.append(
                    f"{context}: verdict GREEN_LIVE_WINDOW_POSTGAME_DEFERRED requires deferred postgame capabilities; "
                    "not deferred: " + ", ".join(not_deferred)
                )
            unproven_live = sorted(
                cid
                for cid in ("live-commitments-posted", "live-fill", "exposure-drain-zero")
                if cid in proof_by_id and proof_by_id[cid] not in PROVEN_LEVELS
            )
            if unproven_live:
                errors.append(
                    f"{context}: verdict GREEN_LIVE_WINDOW_POSTGAME_DEFERRED requires a proven live window; "
                    "not proven: " + ", ".join(unproven_live)
                )
        if verdict_label == "AMBER_QUOTED_NO_FILL":
            posted_proof = proof_by_id.get("live-commitments-posted")
            if posted_proof is not None and posted_proof not in PROVEN_LEVELS:
                errors.append(f"{context}: verdict AMBER_QUOTED_NO_FILL requires proven live-commitments-posted")
            fill_proof = proof_by_id.get("live-fill")
            if fill_proof is not None and fill_proof not in {"deferred", "failed"}:
                errors.append(f"{context}: verdict AMBER_QUOTED_NO_FILL requires live-fill to be deferred or failed")
        if verdict_label == "AMBER_TOKEN_TOPUP_NEEDED":
            if proof_by_id and not any(proof in {"deferred", "failed"} for proof in proof_by_id.values()):
                errors.append(f"{context}: verdict AMBER_TOKEN_TOPUP_NEEDED requires at least one deferred or failed capability")

    zero = doc.get("zeroExposure")
    if "zeroExposure" in doc:
        if not isinstance(zero, dict):
            errors.append(f"{context}: zeroExposure must be an object")
        else:
            for key in ["checkedAtUtc", *ZERO_EXPOSURE_COUNT_KEYS, "evidence"]:
                if key not in zero:
                    errors.append(f"{context}: zeroExposure missing required key {key!r}")
            if "checkedAtUtc" in zero and not parse_datetime(zero.get("checkedAtUtc")):
                errors.append(f"{context}: zeroExposure.checkedAtUtc must be an ISO date-time")
            for key in ZERO_EXPOSURE_COUNT_KEYS:
                if key in zero and (not is_plain_int(zero[key]) or zero[key] != 0):
                    errors.append(f"{context}: zeroExposure.{key} must be the integer 0 in a published canary")
            if "evidence" in zero:
                check_relative_path(zero.get("evidence"), base=artifact_dir, errors=errors, context=f"{context} zeroExposure.evidence")

    categories_seen: set[str] = set()
    txs = doc.get("transactions")
    if "transactions" in doc:
        if not isinstance(txs, list):
            errors.append(f"{context}: transactions must be an array")
        else:
            seen_hash_category: set[tuple[str, str]] = set()
            for idx, tx in enumerate(txs):
                tx_context = f"{context}: transactions[{idx}]"
                if not isinstance(tx, dict):
                    errors.append(f"{tx_context} must be an object")
                    continue
                for key in ["category", "txHash", "status", "operatorControlled"]:
                    if key not in tx:
                        errors.append(f"{tx_context} missing required key {key!r}")
                category = tx.get("category")
                if "category" in tx and category not in TX_CATEGORIES:
                    allowed = ", ".join(sorted(TX_CATEGORIES))
                    errors.append(f"{tx_context}: category {category!r} must be one of: {allowed}")
                    category = None
                elif isinstance(category, str):
                    categories_seen.add(category)
                tx_hash = tx.get("txHash")
                if "txHash" in tx and (not isinstance(tx_hash, str) or not TX_HASH_RE.match(tx_hash)):
                    errors.append(f"{tx_context}: txHash must be a 0x-prefixed 32-byte hash")
                    tx_hash = None
                if "status" in tx and tx.get("status") not in {"success", "reverted"}:
                    errors.append(f"{tx_context}: status must be success or reverted")
                if "operatorControlled" in tx and not isinstance(tx.get("operatorControlled"), bool):
                    errors.append(f"{tx_context}: operatorControlled must be boolean")
                if category == "score-callback" and tx.get("operatorControlled") is True:
                    errors.append(
                        f"{tx_context}: score-callback transactions are sent by the oracle network; operatorControlled must be false"
                    )
                if isinstance(tx_hash, str) and isinstance(category, str):
                    pair = (tx_hash.lower(), category)
                    if pair in seen_hash_category:
                        errors.append(f"{tx_context}: duplicate transaction entry for {category} {tx_hash}")
                    seen_hash_category.add(pair)
            if verdict_label == "GREEN_LIVE_WINDOW_POSTGAME_DEFERRED":
                postgame_present = sorted(categories_seen & POSTGAME_TX_CATEGORIES)
                if postgame_present:
                    errors.append(
                        f"{context}: verdict GREEN_LIVE_WINDOW_POSTGAME_DEFERRED cannot include postgame "
                        "transaction categories: " + ", ".join(postgame_present)
                    )
            if verdict_label == "FULL_GREEN":
                if "settle" not in categories_seen:
                    errors.append(f"{context}: verdict FULL_GREEN requires at least one settle transaction")
                if not categories_seen & {"score-request", "score-callback"}:
                    errors.append(f"{context}: verdict FULL_GREEN requires score-request or score-callback transaction evidence")

    evidence_doc = docs.get(artifact_dir / "evidence.json")
    if not isinstance(evidence_doc, dict):
        errors.append(f"{context}: missing companion evidence.json in the artifact directory")
    else:
        validate_adopting_run_evidence(path, evidence_doc, verdict_label, errors)


def validate_adoption_pairing(docs: dict[Path, Any], errors: list[str]) -> None:
    scorecard_dirs = {path.parent for path in docs if path.name == "mve-scorecard.json" and "runs" in path.parts}
    v2_matrix_dirs = {
        path.parent
        for path, doc in docs.items()
        if path.name == "scenario-matrix.json" and "runs" in path.parts and scenario_matrix_is_v2(doc)
    }
    for directory in sorted(scorecard_dirs - v2_matrix_dirs):
        errors.append(
            f"{display_path(directory)}: mve-scorecard.json requires a schemaVersion >= {SCENARIO_MATRIX_MIN_VERSION} "
            "scenario-matrix.json in the same run directory"
        )
    for directory in sorted(v2_matrix_dirs - scorecard_dirs):
        errors.append(
            f"{display_path(directory)}: schemaVersion >= {SCENARIO_MATRIX_MIN_VERSION} scenario-matrix.json requires an "
            "mve-scorecard.json in the same run directory"
        )


def validate_schema_pointers(docs: dict[Path, Any], errors: list[str]) -> None:
    known_schema_ids = {
        INDEX_SCHEMA_ID,
        ARCHIVE_SCHEMA_ID,
        RELEASE_ACCEPTANCE_SCHEMA_ID,
        SCENARIO_MATRIX_SCHEMA_ID,
        MVE_SCORECARD_SCHEMA_ID,
    }
    for path, doc in docs.items():
        if not isinstance(doc, dict):
            continue
        if path.name.endswith(".schema.json"):
            continue
        if path == ROOT / "index.json":
            if doc.get("$schema") != INDEX_SCHEMA_ID:
                errors.append(f"{rel(path)}: missing or incorrect $schema pointer")
            continue
        if path.name == "index.json" and "archive" in path.parts:
            if doc.get("$schema") != ARCHIVE_SCHEMA_ID:
                errors.append(f"{rel(path)}: missing or incorrect $schema pointer")
            continue
        if path.name == "acceptance.json" and "releases" in path.parts:
            if doc.get("$schema") != RELEASE_ACCEPTANCE_SCHEMA_ID:
                errors.append(f"{rel(path)}: missing or incorrect $schema pointer")
            continue
        schema_pointer = doc.get("$schema")
        if schema_pointer is not None and schema_pointer not in known_schema_ids:
            errors.append(f"{rel(path)}: unknown $schema pointer {schema_pointer!r}")


def validate_generated_indexes(errors: list[str]) -> None:
    script = ROOT / "scripts" / "generate-indexes.py"
    if not script.is_file():
        errors.append("scripts/generate-indexes.py: missing index generator")
        return
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        output = result.stdout.strip()
        if output:
            for line in output.splitlines():
                errors.append(f"generated indexes: {line}")
        else:
            errors.append("generated indexes: scripts/generate-indexes.py --check failed without output")


def safety_scan(files: list[Path], errors: list[str]) -> int:
    scanned = 0
    for path in sorted(files):
        if path.suffix not in TEXT_SUFFIXES:
            continue
        # Avoid the validator tripping over its own regex literals.
        if rel(path) == "scripts/validate-artifacts.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for label, pattern in SAFETY_PATTERNS:
            match = pattern.search(text)
            if match:
                sample = match.group(0).replace("\n", " ")[:120]
                errors.append(f"{rel(path)}: public-safety scan matched {label}: {sample!r}")
    return scanned


def main() -> int:
    errors: list[str] = []
    files = iter_repo_files()
    docs = parse_json_files(files, errors)
    ndjson_lines = parse_ndjson_files(files, errors)

    validate_schema_files(docs, errors)
    validate_schema_pointers(docs, errors)
    validate_index(ROOT / "index.json", docs, errors)

    for path, doc in sorted(docs.items()):
        if path.name == "index.json" and "archive" in path.parts:
            validate_archive_index(path, doc, docs, errors)
        if path.name == "acceptance.json" and "releases" in path.parts:
            validate_release_acceptance(path, doc, errors)
        if path.name == "scenario-matrix.json" and "runs" in path.parts:
            validate_scenario_matrix(path, doc, errors)
        if path.name == "mve-scorecard.json" and "runs" in path.parts:
            validate_mve_scorecard(path, doc, docs, errors)
        validate_projection_convergence(path, doc, errors)
        validate_raw_file_maps(path, doc, errors)

    validate_adoption_pairing(docs, errors)
    validate_generated_indexes(errors)
    scanned_text_files = safety_scan(files, errors)

    if errors:
        print("Artifact validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Artifact validation passed: "
        f"{sum(1 for p in files if p.suffix == '.json')} JSON files, "
        f"{ndjson_lines} NDJSON lines, "
        f"{scanned_text_files} text files scanned."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
