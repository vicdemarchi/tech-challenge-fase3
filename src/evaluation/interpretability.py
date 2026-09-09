"""Interpretabilidade global com metodo agnostico ao algoritmo."""

from __future__ import annotations

import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline


def permutation_feature_importance(
    pipeline: Pipeline,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    random_state: int = 42,
    max_rows: int = 10_000,
) -> pd.DataFrame:
    """Calcula queda de PR-AUC ao permutar cada atributo original."""
    if len(x_test) > max_rows:
        sampled = x_test.sample(max_rows, random_state=random_state)
        sampled_y = y_test.loc[sampled.index]
    else:
        sampled = x_test
        sampled_y = y_test
    result = permutation_importance(
        pipeline,
        sampled,
        sampled_y,
        scoring="average_precision",
        n_repeats=8,
        random_state=random_state,
        n_jobs=-1,
    )
    return (
        pd.DataFrame(
            {
                "variavel": sampled.columns,
                "importancia_media": result.importances_mean,
                "importancia_desvio": result.importances_std,
            }
        )
        .sort_values("importancia_media", ascending=False)
        .reset_index(drop=True)
    )


def try_shap_values(
    pipeline: Pipeline,
    x_test: pd.DataFrame,
    max_rows: int = 2_000,
):
    """Retorna valores SHAP quando a dependencia e o estimador forem compativeis."""
    try:
        import shap  # type: ignore
    except ImportError:
        return None
    model = pipeline.named_steps["model"]
    if model.__class__.__name__ != "RandomForestClassifier":
        return None
    sample = x_test.sample(min(len(x_test), max_rows), random_state=42)
    transformed = pipeline.named_steps["preprocessor"].transform(sample)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    explainer = shap.TreeExplainer(model)
    values = explainer.shap_values(transformed)
    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    return {"values": values, "data": transformed, "feature_names": feature_names}
