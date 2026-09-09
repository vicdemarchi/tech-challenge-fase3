import unittest
from pathlib import Path

from src.preprocessing.schema import load_dataset, prepare_target
from src.preprocessing.split import grouped_train_validation_test_split


FIXTURE = Path(__file__).parent / "fixtures" / "amostra_teste_sintetica.csv"


class GroupSplitTest(unittest.TestCase):
    def test_municipalities_do_not_overlap(self):
        frame = prepare_target(load_dataset(FIXTURE))
        split = grouped_train_validation_test_split(frame)
        train = set(split.train["id_municipio"])
        validation = set(split.validation["id_municipio"])
        test = set(split.test["id_municipio"])
        self.assertFalse(train & validation)
        self.assertFalse(train & test)
        self.assertFalse(validation & test)
        self.assertEqual(len(split.train) + len(split.validation) + len(split.test), len(frame))


if __name__ == "__main__":
    unittest.main()

