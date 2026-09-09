"""Particionamento agrupado para impedir que um municipio vaze entre conjuntos."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


@dataclass
class DataSplit:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def grouped_train_validation_test_split(
    frame: pd.DataFrame,
    group_column: str = "id_municipio",
    random_state: int = 42,
) -> DataSplit:
    """Cria particoes aproximadas de 60/20/20 sem sobrepor grupos."""
    outer = GroupShuffleSplit(
        n_splits=1, test_size=0.20, random_state=random_state
    )
    train_validation_idx, test_idx = next(
        outer.split(frame, groups=frame[group_column])
    )
    train_validation = frame.iloc[train_validation_idx].copy()
    test = frame.iloc[test_idx].copy()

    inner = GroupShuffleSplit(
        n_splits=1, test_size=0.25, random_state=random_state + 1
    )
    train_idx, validation_idx = next(
        inner.split(train_validation, groups=train_validation[group_column])
    )
    train = train_validation.iloc[train_idx].copy()
    validation = train_validation.iloc[validation_idx].copy()

    train_groups = set(train[group_column])
    validation_groups = set(validation[group_column])
    test_groups = set(test[group_column])
    if train_groups & validation_groups or train_groups & test_groups or validation_groups & test_groups:
        raise AssertionError("Um municipio apareceu em mais de uma particao.")
    return DataSplit(train=train, validation=validation, test=test)

