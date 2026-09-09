import unittest

import numpy as np

from src.evaluation.metrics import (
    classification_metrics,
    select_balanced_accuracy_threshold,
)


class MetricsTests(unittest.TestCase):
    def test_balanced_threshold_and_confusion_counts(self) -> None:
        y_true = np.array([0, 0, 0, 1, 1, 1])
        probability = np.array([0.10, 0.30, 0.45, 0.40, 0.70, 0.90])
        threshold = select_balanced_accuracy_threshold(y_true, probability)
        metrics = classification_metrics(y_true, probability, threshold)

        self.assertGreaterEqual(threshold, 0.30)
        self.assertLessEqual(threshold, 0.46)
        self.assertEqual(
            metrics["verdadeiros_negativos"]
            + metrics["falsos_positivos"]
            + metrics["falsos_negativos"]
            + metrics["verdadeiros_positivos"],
            len(y_true),
        )


if __name__ == "__main__":
    unittest.main()
