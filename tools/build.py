#!/usr/bin/env python3
"""Create a deterministic, directly installable datapack ZIP. Python stdlib only."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(root: Path = ROOT, output: Path | None = None) -> Path:
    metadata = json.loads((root / "project.json").read_text(encoding="utf-8"))
    version = metadata["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-zA-Z0-9.]+)?", version):
        raise ValueError("Unsafe or invalid project version")
    output = output or root / "dist"
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"npcraft-{version}-mc{metadata['minecraft']}.zip"
    source = root / "datapack"
    if not (source / "pack.mcmeta").is_file():
        raise FileNotFoundError("datapack/pack.mcmeta is required")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlinks are not distributable: {path}")
            if not path.is_file():
                continue
            relative = path.relative_to(source).as_posix()
            if path.suffix not in {".json", ".mcfunction", ".mcmeta", ".png", ".nbt", ".txt"}:
                raise ValueError(f"Unexpected distributable: {relative}")
            info = zipfile.ZipInfo(relative, (2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect-tag", help="Reject a release tag that differs from project.json")
    args = parser.parse_args()
    if args.expect_tag:
        version = json.loads((ROOT / "project.json").read_text())["version"]
        if args.expect_tag != f"v{version}":
            parser.error(f"Expected tag v{version}, not {args.expect_tag!r}")
    print(build(output=args.output))


if __name__ == "__main__":
    main()
