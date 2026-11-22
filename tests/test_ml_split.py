"""Tests for leakage-safe holdout selection (no medical images required)."""
import csv
import tempfile
import unittest
from pathlib import Path

import numpy as np

from ml.train import check_split, select_split


class SplitTests(unittest.TestCase):
    def setUp(self):
        self.y = np.array([0] * 12 + [1] * 12)
        self.paths = [f"class_{label}/img_{i}.png" for i, label in enumerate(self.y)]

    def test_image_split_is_reproducible(self):
        a, b, mode = select_split(self.y, self.paths, 0.25, 42)
        c, d, _ = select_split(self.y, self.paths, 0.25, 42)
        np.testing.assert_array_equal(a, c)
        np.testing.assert_array_equal(b, d)
        check_split(self.y, a, b, 2)
        self.assertEqual(mode, "stratified_image")

    def test_patient_groups_do_not_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "groups.csv"
            # Twelve patients; each has two images, all within the same class.
            patient_ids = [f"patient_{i // 2}" for i in range(24)]
            with manifest.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.writer(stream)
                writer.writerow(["path", "patient_id"])
                writer.writerows(zip(self.paths, patient_ids))
            train, test, mode = select_split(self.y, self.paths, 0.33, 7, manifest)
            self.assertEqual(mode, "patient_group")
            self.assertFalse({patient_ids[i] for i in train} & {patient_ids[i] for i in test})

    def test_missing_patient_id_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "groups.csv"
            manifest.write_text("path,patient_id\n" + self.paths[0] + ",p1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing patient IDs"):
                select_split(self.y, self.paths, 0.2, 42, manifest)

    def test_incomplete_classes_rejected(self):
        with self.assertRaisesRegex(ValueError, "every class"):
            check_split(np.array([0, 0, 1, 1]), np.array([0, 1]), np.array([2, 3]), 2)


if __name__ == "__main__":
    unittest.main()
