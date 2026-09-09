import unittest
from pathlib import Path

from src.modeling.train import train_and_select
from src.preprocessing.schema import load_dataset, prepare_target, select_features
from src.preprocessing.split import grouped_train_validation_test_split


FIXTURE = Path(__file__).parent / "fixtures" / "amostra_teste_sintetica.csv"


class TrainingTest(unittest.TestCase):
    def test_training_returns_non_baseline_model_and_metrics(self):
        frame = prepare_target(load_dataset(FIXTURE))
        features = select_features(frame)
        split = grouped_train_validation_test_split(frame)
        trained, metrics = train_and_select(split.train, split.validation, features)
        self.assertNotEqual(trained.name, "baseline_majoritario")
        self.assertEqual(len(metrics), 5)
        self.assertIn("gap_pr_auc", metrics.columns)
        self.assertNotIn("proficiencia", features.all)


if __name__ == "__main__":
    unittest.main()

