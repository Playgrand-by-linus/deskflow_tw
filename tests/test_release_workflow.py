import os
import unittest
try:
    import yaml
except ImportError:
    yaml = None

class TestReleaseWorkflow(unittest.TestCase):
    def setUp(self):
        self.repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.workflow_path = os.path.join(self.repo_dir, ".github", "workflows", "release-tw.yml")

    def test_workflow_file_exists(self):
        self.assertTrue(os.path.isfile(self.workflow_path), f"{self.workflow_path} does not exist")

    def test_workflow_triggers_and_targets(self):
        with open(self.workflow_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check triggers
        self.assertIn("v*-tw*", content, "Must trigger on v*-tw* tags")
        self.assertIn("workflow_dispatch", content, "Must allow manual triggering")

        # Check platform targets
        self.assertIn("windows", content.lower(), "Must build Windows package")
        self.assertIn("macos", content.lower(), "Must build macOS package")

        # Check release step
        self.assertIn("action-gh-release", content, "Must publish release via action-gh-release")

if __name__ == "__main__":
    unittest.main()
