"""Data integrity checks; inputs are synthetic bytes, never patient data."""
import tempfile
import unittest
from pathlib import Path

import numpy as np

from ml.quality import audit_images


class QualityTests(unittest.TestCase):
    def test_duplicate_image_crossing_split_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, data in [("a.png", b"same"), ("b.png", b"same"), ("c.png", b"different")]:
                (root / name).write_bytes(data)
            with self.assertRaisesRegex(ValueError, "cross train/test"):
                audit_images(root, ["a.png", "b.png", "c.png"], np.array([0, 0, 1]), [0, 2], [1])

    def test_duplicate_labels_conflict_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "a.png").write_bytes(b"same")
            (root / "b.png").write_bytes(b"same")
            with self.assertRaisesRegex(ValueError, "contradictory labels"):
                audit_images(root, ["a.png", "b.png"], np.array([0, 1]), [0], [1])

    def test_distinct_content_is_accepted(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for i in range(4):
                (root / f"{i}.png").write_bytes(f"image-{i}".encode())
            result = audit_images(root, [f"{i}.png" for i in range(4)],
                                  np.array([0, 0, 1, 1]), [0, 2], [1, 3])
            self.assertEqual(result["cross_split_exact_duplicates"], 0)
            self.assertEqual(result["unique_image_hashes"], 4)


if __name__ == "__main__":
    unittest.main()
