#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline baseline integration check; independent, strict unified-diff replay in memory."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('make_patch', ROOT / 'scripts/make_patch.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def replay(source, patch, reverse=False):
    original = source.splitlines(True)
    output, cursor = [], 0
    lines = patch.splitlines(True)
    i = 2
    while i < len(lines):
        match = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n', lines[i])
        if not match:
            raise ValueError('Invalid hunk header')
        start = int(match[3] if reverse else match[1]) - 1
        if start < cursor:
            raise ValueError('Overlapping hunk')
        output.extend(original[cursor:start])
        cursor = start
        removed = added = 0
        i += 1
        while i < len(lines) and not lines[i].startswith('@@ '):
            kind, value = lines[i][0], lines[i][1:]
            if kind not in ' +-': raise ValueError('Invalid patch line')
            removed += kind in ' -'
            added += kind in ' +'
            if reverse and kind != ' ': kind = '+' if kind == '-' else '-'
            if kind in ' -':
                if cursor >= len(original) or original[cursor] != value:
                    raise ValueError('Context mismatch')
                cursor += 1
            if kind in ' +': output.append(value)
            i += 1
        if removed != int(match[2] or 1) or added != int(match[4] or 1):
            raise ValueError('Hunk length mismatch')
    output.extend(original[cursor:])
    return ''.join(output)

def main():
    source = Path(sys.argv[1])
    manifest = json.loads(module.MANIFEST.read_text())
    patch, _, verified = module.generate(source)
    assert verified
    assert patch == (ROOT / 'patches/ghidra-12.1.4-ko.patch').read_text()
    original = (source / manifest['path']).read_text()
    translated = replay(original, patch)
    assert replay(translated, patch, reverse=True) == original
    for entry in manifest['replacements']:
        assert translated.count(entry['new']) == 1
        assert entry['old'] not in translated
    # Every other byte/line must match the original, including names and callbacks.
    expected = original
    for entry in manifest['replacements']:
        expected = expected.replace(entry['old'], entry['new'])
    assert translated == expected
    for label in ['OK', 'Cancel', 'Dismiss', 'Apply']:
        assert f'.setName("{label}")' in translated
    print('PASS: baseline hash, bundled patch, strict hunk replay, 8 replacements, identifiers, reverse roundtrip')

if __name__ == '__main__': main()
