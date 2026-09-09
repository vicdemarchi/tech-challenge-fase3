"""Segmentacao de municipios por contexto anterior ao desfecho."""

from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def cluster_municipalities(
    frame: pd.DataFrame,
    numeric_features: list[str],
    group_column: str = "id_municipio",
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Escolhe k entre 2 e 5 por silhouette e devolve perfis dos clusters."""
    usable = [column for column in numeric_features if column in frame.columns]
    if not usable:
        return pd.DataFrame(), pd.DataFrame()
    aggregation = {column: "median" for column in usable}
    municipality = frame.groupby(group_column, as_index=False).agg(aggregation)
    if len(municipality) < 4:
        return pd.DataFrame(), pd.DataFrame()

    transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
            ("scaler", StandardScaler()),
        ]
    )
    matrix = transformer.fit_transform(municipality[usable])
    best_model = None
    best_score = float("-inf")
    upper = min(5, len(municipality) - 1)
    for k in range(2, upper + 1):
        model = KMeans(n_clusters=k, n_init=20, random_state=random_state)
        labels = model.fit_predict(matrix)
        score = silhouette_score(matrix, labels)
        if score > best_score:
            best_score = score
            best_model = model
    assert best_model is not None
    municipality["cluster"] = best_model.labels_.astype(int)
    municipality["silhouette_global"] = best_score
    profiles = municipality.groupby("cluster")[usable].mean().round(3)
    profiles.insert(0, "n_municipios", municipality.groupby("cluster").size())
    return municipality, profiles.reset_index()

