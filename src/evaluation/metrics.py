"""Metricas orientadas a deteccao de risco e selecao de limiar."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    fbeta_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


THRESHOLD_GRID = np.linspace(0.05, 0.95, 181)


def select_f2_threshold(y_true: np.ndarray, probability: np.ndarray) -> float:
    """Seleciona no conjunto de validacao o limiar que maximiza F2."""
    scores = [
        fbeta_score(y_true, probability >= threshold, beta=2, zero_division=0)
        for threshold in THRESHOLD_GRID
    ]
    return float(THRESHOLD_GRID[int(np.argmax(scores))])


def select_balanced_accuracy_threshold(
    y_true: np.ndarray, probability: np.ndarray
) -> float:
    """Seleciona na validacao o limiar de maior acuracia balanceada."""
    scores = [
        balanced_accuracy_score(y_true, probability >= threshold)
        for threshold in THRESHOLD_GRID
    ]
    return float(THRESHOLD_GRID[int(np.argmax(scores))])


def classification_metrics(
    y_true: np.ndarray,
    probability: np.ndarray,
    threshold: float,
) -> dict[str, float | int]:
    prediction = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, prediction, labels=[0, 1]).ravel()
    return {
        "n": int(len(y_true)),
        "prevalencia_risco": float(np.mean(y_true)),
        "roc_auc": float(roc_auc_score(y_true, probability)),
        "pr_auc": float(average_precision_score(y_true, probability)),
        "accuracy": float(accuracy_score(y_true, prediction)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, prediction)),
        "precision": float(precision_score(y_true, prediction, zero_division=0)),
        "recall": float(recall_score(y_true, prediction, zero_division=0)),
        "f1": float(f1_score(y_true, prediction, zero_division=0)),
        "f2": float(fbeta_score(y_true, prediction, beta=2, zero_division=0)),
        "brier": float(brier_score_loss(y_true, probability)),
        "taxa_alertas": float(np.mean(prediction)),
        "verdadeiros_negativos": int(tn),
        "falsos_positivos": int(fp),
        "falsos_negativos": int(fn),
        "verdadeiros_positivos": int(tp),
    }
