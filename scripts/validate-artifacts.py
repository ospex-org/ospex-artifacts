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
import sys
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

INDEX_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/artifact-index.schema.json"
RELEASE_ACCEPTANCE_SCHEMA_ID = "https://github.com/ospex-org/ospex-artifacts/schemas/release-acceptance.schema.json"

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
        "specific upstream odds provider name",
        re.compile(r"\b(draftkings|fan\s?duel|betrivers|betmgm|pinnacle|the[- ]odds[- ]api|sportradar)\b", re.I),
    ),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def parse_datetime(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


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


def validate_index(index_path: Path, docs: dict[Path, Any], errors: list[str]) -> None:
    doc = docs.get(index_path)
    if not isinstance(doc, dict):
        errors.append("index.json: must be a JSON object")
        return

    allowed_top = {"$schema", "schemaVersion", "generatedAt", "repository", "artifacts", "latest"}
    for key in doc:
        if key not in allowed_top:
            errors.append(f"index.json: unexpected top-level key {key!r}")

    required = ["$schema", "schemaVersion", "generatedAt", "repository", "artifacts", "latest"]
    for key in required:
        if key not in doc:
            errors.append(f"index.json: missing required key {key!r}")

    if doc.get("$schema") != INDEX_SCHEMA_ID:
        errors.append(f"index.json: $schema must be {INDEX_SCHEMA_ID}")
    if not is_plain_int(doc.get("schemaVersion")) or doc.get("schemaVersion", 0) < 1:
        errors.append("index.json: schemaVersion must be an integer >= 1")
    if not parse_datetime(doc.get("generatedAt")):
        errors.append("index.json: generatedAt must be an ISO date-time")
    if doc.get("repository") != "ospex-org/ospex-artifacts":
        errors.append("index.json: repository must be ospex-org/ospex-artifacts")

    artifacts = doc.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("index.json: artifacts must be an array")
        artifacts = []

    seen_ids: set[str] = set()
    for idx, artifact in enumerate(artifacts):
        context = f"index.json artifacts[{idx}]"
        if not isinstance(artifact, dict):
            errors.append(f"{context}: must be an object")
            continue
        for key in ["artifactType", "artifactId", "status", "summaryPath", "dataPath"]:
            if key not in artifact:
                errors.append(f"{context}: missing required key {key!r}")
        artifact_type = artifact.get("artifactType")
        artifact_id = artifact.get("artifactId")
        status = artifact.get("status")
        if artifact_type not in STATUS_BY_ARTIFACT_TYPE:
            errors.append(f"{context}: unsupported artifactType {artifact_type!r}")
        elif status not in STATUS_BY_ARTIFACT_TYPE[artifact_type]:
            allowed = ", ".join(sorted(STATUS_BY_ARTIFACT_TYPE[artifact_type]))
            errors.append(f"{context}: status {status!r} is not allowed for {artifact_type}; expected one of: {allowed}")
        if not isinstance(artifact_id, str) or not artifact_id:
            errors.append(f"{context}: artifactId must be a non-empty string")
        elif artifact_id in seen_ids:
            errors.append(f"{context}: duplicate artifactId {artifact_id}")
        else:
            seen_ids.add(artifact_id)
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

    latest = doc.get("latest")
    if not isinstance(latest, dict):
        errors.append("index.json: latest must be an object")
        return
    if set(latest) != {"runs", "releases", "daily"}:
        errors.append("index.json: latest must contain exactly runs, releases, and daily arrays")
    for key in ["runs", "releases", "daily"]:
        values = latest.get(key)
        if not isinstance(values, list):
            errors.append(f"index.json latest.{key}: must be an array")
            continue
        for item_idx, value in enumerate(values):
            check_relative_path(value, base=ROOT, errors=errors, context=f"index.json latest.{key}[{item_idx}]")


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


def validate_schema_pointers(docs: dict[Path, Any], errors: list[str]) -> None:
    for path, doc in docs.items():
        if not isinstance(doc, dict):
            continue
        if path.name.endswith(".schema.json"):
            continue
        if path == ROOT / "index.json":
            if doc.get("$schema") != INDEX_SCHEMA_ID:
                errors.append(f"{rel(path)}: missing or incorrect $schema pointer")
            continue
        if path.name == "acceptance.json" and "releases" in path.parts:
            if doc.get("$schema") != RELEASE_ACCEPTANCE_SCHEMA_ID:
                errors.append(f"{rel(path)}: missing or incorrect $schema pointer")
            continue
        schema_pointer = doc.get("$schema")
        if schema_pointer is not None and schema_pointer not in {INDEX_SCHEMA_ID, RELEASE_ACCEPTANCE_SCHEMA_ID}:
            errors.append(f"{rel(path)}: unknown $schema pointer {schema_pointer!r}")


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
        if path.name == "acceptance.json" and "releases" in path.parts:
            validate_release_acceptance(path, doc, errors)
        validate_raw_file_maps(path, doc, errors)

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
