"""End-to-end CLI smoke test using generated non-medical patterns.

This verifies the training *software*, NOT diagnostic accuracy.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


class PipelineSmokeTests(unittest.TestCase):
    def test_train_generates_models_and_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            dataset = root / "synthetic"
            for label, kind in [("stripes_horizontal", "horizontal"), ("stripes_vertical", "vertical")]:
                target = dataset / label
                target.mkdir(parents=True)
                for i in range(12):
                    # Deterministically varied non-medical patterns; no external downloads.
                    pixels = np.zeros((48, 48), dtype=np.uint8)
                    for j in range(48):
                        if (j + i % 3) % 12 < 6:
                            if kind == "horizontal":
                                pixels[j, :] = 190 + i
                            else:
                                pixels[:, j] = 190 + i
                    pixels[(i * 3) % 48, (i * 7) % 48] = 255
                    Image.fromarray(pixels).save(target / f"img_{i:02d}.png")
            output = root / "results"
            process = subprocess.run(
                [sys.executable, "-m", "ml.train", "--data-dir", str(dataset),
                 "--output-dir", str(output), "--test-size", "0.25"],
                cwd=ROOT, text=True, capture_output=True, timeout=120,
            )
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            report = json.loads((output / "metrics.json").read_text())
            self.assertEqual(set(report["models"]),
                             {"majority_class_baseline", "svm", "random_forest"})
            self.assertEqual(report["data_integrity"]["cross_split_exact_duplicates"], 0)
            self.assertEqual(report["split_type"], "stratified_image")
            self.assertTrue((output / "svm.joblib").exists())
            self.assertTrue((output / "random_forest.joblib").exists())
            for metrics in report["models"].values():
                self.assertTrue(0 <= metrics["accuracy"] <= 1)
                self.assertTrue(0 <= metrics["macro_f1"] <= 1)


if __name__ == "__main__":
    unittest.main()
