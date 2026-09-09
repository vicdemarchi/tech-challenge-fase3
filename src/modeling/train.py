"""Definicao, comparacao e ajuste dos modelos supervisionados."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.evaluation.metrics import classification_metrics, select_f2_threshold
from src.preprocessing.schema import FeatureSet


@dataclass
class TrainedModel:
    name: str
    pipeline: Pipeline
    threshold: float
    validation_metrics: dict[str, float | int | str]


def _preprocessor(features: FeatureSet) -> ColumnTransformer:
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=2)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric, features.numeric),
            ("categorical", categorical, features.categorical),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def candidate_pipelines(features: FeatureSet, random_state: int = 42) -> dict[str, Pipeline]:
    """Retorna baseline e candidatos com pre-processamento encapsulado."""
    estimators = {
        "baseline_majoritario": DummyClassifier(strategy="prior"),
        "regressao_logistica_c0_3": LogisticRegression(
            max_iter=1500,
            class_weight="balanced",
            solver="liblinear",
            C=0.3,
            random_state=random_state,
        ),
        "regressao_logistica_c1_0": LogisticRegression(
            max_iter=1500,
            class_weight="balanced",
            solver="liblinear",
            C=1.0,
            random_state=random_state,
        ),
        "random_forest_depth16_leaf10": RandomForestClassifier(
            n_estimators=180,
            max_depth=16,
            min_samples_leaf=10,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=random_state,
        ),
        "random_forest_leaf20": RandomForestClassifier(
            n_estimators=180,
            min_samples_leaf=20,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=random_state,
        ),
    }
    return {
        name: Pipeline(
            steps=[("preprocessor", _preprocessor(features)), ("model", estimator)]
        )
        for name, estimator in estimators.items()
    }


def train_and_select(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    features: FeatureSet,
    target: str = "nao_alfabetizado",
    random_state: int = 42,
) -> tuple[TrainedModel, pd.DataFrame]:
    """Ajusta candidatos e escolhe o maior PR-AUC na validacao."""
    rows: list[dict[str, float | int | str]] = []
    fitted: dict[str, Pipeline] = {}
    thresholds: dict[str, float] = {}

    for name, pipeline in candidate_pipelines(features, random_state).items():
        pipeline.fit(train[features.all], train[target])
        train_probability = pipeline.predict_proba(train[features.all])[:, 1]
        probability = pipeline.predict_proba(validation[features.all])[:, 1]
        threshold = select_f2_threshold(validation[target].to_numpy(), probability)
        train_metrics = classification_metrics(
            train[target].to_numpy(), train_probability, threshold
        )
        metrics = classification_metrics(
            validation[target].to_numpy(), probability, threshold
        )
        metrics["modelo"] = name
        metrics["limiar"] = threshold
        metrics["pr_auc_treino"] = train_metrics["pr_auc"]
        metrics["roc_auc_treino"] = train_metrics["roc_auc"]
        metrics["gap_pr_auc"] = train_metrics["pr_auc"] - metrics["pr_auc"]
        rows.append(metrics)
        fitted[name] = pipeline
        thresholds[name] = threshold

    table = pd.DataFrame(rows).sort_values(
        ["pr_auc", "recall"], ascending=False
    ).reset_index(drop=True)
    eligible = table.loc[table["modelo"] != "baseline_majoritario"]
    winner_row = eligible.iloc[0] if not eligible.empty else table.iloc[0]
    winner = str(winner_row["modelo"])
    return (
        TrainedModel(
            name=winner,
            pipeline=fitted[winner],
            threshold=thresholds[winner],
            validation_metrics=winner_row.to_dict(),
        ),
        table,
    )


def refit_selected(
    trained: TrainedModel,
    train: pd.DataFrame,
    validation: pd.DataFrame,
    features: FeatureSet,
    target: str = "nao_alfabetizado",
) -> TrainedModel:
    """Reajusta o vencedor em treino+validacao sem tocar no conjunto de teste."""
    combined = pd.concat([train, validation], ignore_index=True)
    trained.pipeline.fit(combined[features.all], combined[target])
    return trained


def leakage_diagnostic(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    target: str = "nao_alfabetizado",
) -> dict[str, float | int | str]:
    """Quantifica o atalho criado pela proficiencia; nunca seleciona o modelo final."""
    if "proficiencia" not in train.columns:
        raise ValueError("A coluna proficiencia nao esta disponivel para o diagnostico.")
    train_x = pd.to_numeric(train["proficiencia"], errors="coerce").to_frame()
    validation_x = pd.to_numeric(validation["proficiencia"], errors="coerce").to_frame()
    diagnostic = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("model", LogisticRegression(max_iter=500, random_state=42)),
        ]
    )
    diagnostic.fit(train_x, train[target])
    probability = diagnostic.predict_proba(validation_x)[:, 1]
    threshold = select_f2_threshold(validation[target].to_numpy(), probability)
    metrics = classification_metrics(validation[target].to_numpy(), probability, threshold)
    metrics.update({"modelo": "diagnostico_com_proficiencia", "limiar": threshold})
    return metrics
