import unittest
from pathlib import Path

from src.preprocessing.schema import (
    TARGET,
    assert_no_leakage,
    load_dataset,
    normalize_known_units,
    prepare_target,
    select_features,
    validate_dataset,
)


FIXTURE = Path(__file__).parent / "fixtures" / "amostra_teste_sintetica.csv"


class SchemaTest(unittest.TestCase):
    def test_contract_and_target(self):
        frame = prepare_target(load_dataset(FIXTURE))
        validate_dataset(frame)
        self.assertIn(TARGET, frame)
        self.assertEqual(set(frame[TARGET].unique()), {0, 1})

    def test_safe_features_exclude_proficiency(self):
        frame = prepare_target(load_dataset(FIXTURE))
        features = select_features(frame)
        self.assertNotIn("proficiencia", features.all)
        self.assertNotIn("alfabetizado_bool", features.all)

    def test_explicit_leakage_guard(self):
        with self.assertRaises(ValueError):
            assert_no_leakage(["regiao", "proficiencia"])

    def test_known_pib_unit_is_corrected(self):
        frame = load_dataset(FIXTURE)
        frame.loc[:, "pib_per_capita_anterior"] = 52_000_000
        corrected = normalize_known_units(frame)
        self.assertEqual(float(corrected["pib_per_capita_anterior"].median()), 52_000)
        self.assertTrue(corrected.attrs["unit_corrections"])


if __name__ == "__main__":
    unittest.main()
