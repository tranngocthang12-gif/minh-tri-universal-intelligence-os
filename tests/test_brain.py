import tempfile
import unittest
from pathlib import Path

from minhtri.brain import BRAIN_ARTIFACTS, brain_bundle, build_brain_manifest, verify_brain_manifest
from minhtri.core import GateError


class BrainManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for index, relative in enumerate(BRAIN_ARTIFACTS, start=1):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"artifact-{index}\n", encoding="utf-8")
        self.revision = "a" * 40

    def test_manifest_pins_revision_and_all_brain_artifacts(self):
        bundle = brain_bundle(self.root, self.revision)
        self.assertEqual(bundle["manifest"]["brain_revision"], self.revision)
        self.assertEqual([item["path"] for item in bundle["manifest"]["artifacts"]], list(BRAIN_ARTIFACTS))
        self.assertEqual(len(bundle["fingerprint"]), 64)
        self.assertEqual(verify_brain_manifest(self.root, bundle["manifest"]), bundle["fingerprint"])

    def test_any_brain_artifact_drift_invalidates_old_manifest(self):
        manifest = build_brain_manifest(self.root, self.revision)
        (self.root / "docs" / "ARCHITECTURE.md").write_text("changed architecture\n", encoding="utf-8")
        with self.assertRaisesRegex(GateError, "does not match"):
            verify_brain_manifest(self.root, manifest)

    def test_unpinned_or_malformed_revision_fails_closed(self):
        with self.assertRaisesRegex(GateError, "brain_revision"):
            build_brain_manifest(self.root, "not-a-git-sha")


if __name__ == "__main__":
    unittest.main()
