# SPDX-License-Identifier: Apache-2.0
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("make_patch", ROOT / "scripts/make_patch.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
M = json.loads(module.MANIFEST.read_text())

class PatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / M["path"]
        self.file.parent.mkdir(parents=True)
        (self.root / "Ghidra/application.properties").write_text("application.version=999.0\n")
        self.original = "\n".join(x["old"] for x in M["replacements"]) + '\n'
        self.file.write_text(self.original)
    def test_unknown_fails_closed(self):
        with self.assertRaises(ValueError): module.generate(self.root)
    def test_porting_and_read_only(self):
        patch, version, verified = module.generate(self.root, True)
        self.assertFalse(verified)
        self.assertEqual(version, "999.0")
        self.assertIn('+okButton = new JButton("확인(K)")', patch)
        self.assertEqual(self.file.read_text(), self.original)
    def test_missing_duplicate_and_already_translated(self):
        for text in [self.original.replace(M["replacements"][0]["old"], "removed"),
                     self.original + M["replacements"][0]["old"],
                     self.original.replace(M["replacements"][0]["old"], M["replacements"][0]["new"])]:
            self.file.write_text(text)
            with self.assertRaises(ValueError): module.generate(self.root, True)

if __name__ == "__main__": unittest.main()
