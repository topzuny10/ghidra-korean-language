#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate a reviewed source patch. Never modifies the upstream checkout."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[1] / "translations/ko.json"

def generate(root, allow_unverified=False):
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    root = Path(root).resolve()
    props = root / "Ghidra/application.properties"
    version = dict(line.split("=", 1) for line in props.read_text(encoding="utf-8").splitlines()
                   if "=" in line and not line.lstrip().startswith("#")).get("application.version")
    path = root / m["path"]
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError("Source must be a regular file inside the checkout")
    raw = path.read_bytes()
    verified = version == m["baseline_version"] and hashlib.sha256(raw).hexdigest() == m["sha256"]
    if not verified and not allow_unverified:
        raise ValueError(f"Unverified source/version {version!r}; baseline is {m['baseline_version']}. "
                         "Review upstream changes first; --allow-unverified is for porting only.")
    old = raw.decode("utf-8")
    new = old
    for entry in m["replacements"]:
        if new.count(entry["old"]) != 1 or entry["new"] in new:
            raise ValueError(f"Expected exactly one untranslated anchor: {entry['old']}")
        new = new.replace(entry["old"], entry["new"], 1)
    diff = "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                   fromfile="a/" + m["path"], tofile="b/" + m["path"]))
    return diff, version, verified

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--allow-unverified", action="store_true")
    args = parser.parse_args()
    try:
        patch, version, verified = generate(args.source, args.allow_unverified)
        if args.output.resolve().is_relative_to(args.source.resolve()):
            raise ValueError("Write the patch outside the upstream source tree")
        args.output.write_text(patch, encoding="utf-8", newline="\n")
        print(f"version={version} baseline_verified={verified}; wrote {args.output}")
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, f"error: {exc}\n")

if __name__ == "__main__":
    main()
