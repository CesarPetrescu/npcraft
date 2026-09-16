#!/usr/bin/env python3
"""Structural/policy lint, not a replacement for Minecraft's command parser."""
from __future__ import annotations
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IDENTIFIER = re.compile(r"^[a-z0-9_./-]+$")
FUNCTION_REF = re.compile(r"\bfunction\s+(#?npcraft:[a-z0-9_./-]+)")
BLOCK_TAG = re.compile(r"#npcraft:([a-z0-9_./-]+)")


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    pack = root / "datapack"
    try:
        project = json.loads((root / "project.json").read_text(), object_pairs_hook=unique_object)
        meta = json.loads((pack / "pack.mcmeta").read_text(), object_pairs_hook=unique_object)["pack"]
        if meta["min_format"] != project["pack_format"] or meta["max_format"] != project["pack_format"]:
            errors.append("Pack format must match the exact tested project target")
        if "supported_formats" in meta:
            errors.append("Obsolete supported_formats field")
        if project["version"] not in meta["description"]:
            errors.append("Pack description version drift")
    except (OSError, ValueError, KeyError) as exc:
        return [f"Project metadata: {exc}"]
    functions = {"npcraft:" + p.relative_to(pack / "data/npcraft/function").with_suffix("").as_posix(): p
                 for p in (pack / "data/npcraft/function").rglob("*.mcfunction")}
    if not functions:
        errors.append("No datapack functions")
    for path in sorted(pack.rglob("*")):
        if path.is_symlink():
            errors.append(f"Symlink: {path.relative_to(root)}")
            continue
        if not path.is_file():
            continue
        relative = path.relative_to(pack).as_posix()
        if not IDENTIFIER.fullmatch(relative):
            errors.append(f"Invalid resource filename: {relative}")
        if "/functions/" in relative or "/tags/blocks/" in relative:
            errors.append(f"Legacy plural resource directory: {relative}")
        if path.suffix not in {".json", ".mcfunction", ".mcmeta", ".png", ".nbt", ".txt"}:
            errors.append(f"Unexpected pack file: {relative}")
        if path.suffix not in {".json", ".mcfunction", ".mcmeta"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            if not text.endswith("\n") or "\r" in text or "\ufeff" in text:
                errors.append(f"Require UTF-8, LF and terminal newline: {relative}")
            if path.suffix in {".json", ".mcmeta"}:
                value = json.loads(text, object_pairs_hook=unique_object)
                if "/tags/function/" in relative:
                    for ref in value.get("values", []):
                        if isinstance(ref, str) and ref.startswith("npcraft:") and ref not in functions:
                            errors.append(f"Missing function tag target {ref}: {relative}")
                if "/dialog/" in relative and "/tags/" not in relative:
                    for action in value.get("actions", []) + [value.get("yes", {})]:
                        event = action.get("action", {})
                        if event.get("type") == "run_command" and not re.fullmatch(r"trigger npcraft set \d+", event.get("command", "")):
                            errors.append(f"Dialog uses privileged/arbitrary commands: {relative}")
            if path.suffix == ".mcfunction":
                for line_no, raw in enumerate(text.splitlines(), 1):
                    line = raw.strip()
                    where = f"{relative}:{line_no}"
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("/"):
                        errors.append(f"Leading slash in function: {where}")
                    if "$(" in line and not line.startswith("$"):
                        errors.append(f"Missing macro prefix: {where}")
                    for ref in FUNCTION_REF.findall(line):
                        if ref.startswith("#") or ref not in functions:
                            errors.append(f"Unresolved function {ref}: {where}")
                    for tag in BLOCK_TAG.findall(line):
                        if not (pack / f"data/npcraft/tags/block/{tag}.json").is_file():
                            errors.append(f"Unresolved block tag {tag}: {where}")
                    # No persistent force-loading, administrative escalation or remote commands.
                    if re.search(r"(?:^|\brun\s+)(?:forceload|op|deop|ban|whitelist|stop|save-off)\b", line.lstrip("$")):
                        errors.append(f"Forbidden production command: {where}")
                    if "/nav/" in relative and re.search(r"\b(?:setblock|fill|clone)\b", line):
                        errors.append(f"Navigation may not mutate blocks: {where}")
                    if re.search(r"\bsetblock\b", line) and not relative.endswith(("/work/commit.mcfunction", "/actions/mine_commit.mcfunction")):
                        errors.append(f"Block mutation outside harvest commit: {where}")
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            errors.append(f"{relative}: {exc}")
    for name in ("load", "tick"):
        if not (pack / f"data/minecraft/tags/function/{name}.json").exists():
            errors.append(f"Missing {name} hook")
    return errors


if __name__ == "__main__":
    issues = validate()
    if issues:
        print("\n".join(issues), file=sys.stderr)
        raise SystemExit(1)
    print("Datapack structure, references and safety policy: PASS")
