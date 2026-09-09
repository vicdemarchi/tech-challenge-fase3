"""Visualizacoes usadas na EDA e avaliacao final."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
)


BLUE = "#164E63"
TEAL = "#0F766E"
ORANGE = "#EA580C"
RED = "#B91C1C"
GRAY = "#64748B"

DISPLAY_NAMES = {
    "codigo_uf": "UF",
    "media_portugues_anterior": "Média de Português anterior",
    "taxa_alfabetizacao_anterior": "Taxa de alfabetização anterior",
    "percentual_participacao_anterior": "Participação anterior",
    "total_alunos_avaliados_anterior": "Avaliados no ano anterior",
    "populacao_anterior": "População anterior",
    "pib_per_capita_anterior": "PIB per capita anterior",
    "meta_alfabetizacao_2025": "Meta de alfabetização 2025",
    "rede_nome": "Rede",
    "regiao": "Região",
    "nao_alfabetizado": "Não alfabetizado",
}


def _style() -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.dpi": 130,
            "savefig.dpi": 180,
            "axes.titleweight": "bold",
            "axes.titlesize": 13,
            "font.family": "DejaVu Sans",
        }
    )


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_target_distribution(frame: pd.DataFrame, output_dir: Path) -> None:
    _style()
    distribution = frame["nao_alfabetizado"].value_counts().sort_index()
    labels = ["Alfabetizado", "Nao alfabetizado"]
    values = [distribution.get(0, 0), distribution.get(1, 0)]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    bars = ax.bar(labels, values, color=[TEAL, ORANGE], width=0.58)
    ax.set_title("Distribuicao do desfecho")
    ax.set_ylabel("Estudantes")
    ax.bar_label(bars, labels=[f"{value:,}".replace(",", ".") for value in values])
    _save(fig, output_dir / "01_distribuicao_alvo.png")


def plot_missingness(frame: pd.DataFrame, columns: list[str], output_dir: Path) -> None:
    _style()
    missing = (frame[columns].isna().mean() * 100).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, max(3.8, len(missing) * 0.38)))
    ax.barh(missing.index, missing.values, color=BLUE)
    ax.set_title("Dados ausentes nos atributos candidatos")
    ax.set_xlabel("Percentual ausente (%)")
    for index, value in enumerate(missing.values):
        ax.text(value + 0.15, index, f"{value:.1f}%", va="center", fontsize=8)
    _save(fig, output_dir / "02_dados_ausentes.png")


def plot_observed_risk_by_category(
    frame: pd.DataFrame, column: str, output_dir: Path
) -> None:
    if column not in frame.columns:
        return
    _style()
    grouped = (
        frame.groupby(column, dropna=False)["nao_alfabetizado"]
        .agg(["mean", "size"])
        .query("size >= 5")
        .sort_values("mean")
    )
    if grouped.empty:
        return
    fig, ax = plt.subplots(figsize=(8.2, max(4, len(grouped) * 0.34)))
    ax.barh(grouped.index.astype(str), grouped["mean"] * 100, color=TEAL)
    ax.set_title(f"Risco observado por {column}")
    ax.set_xlabel("Nao alfabetizados (%)")
    _save(fig, output_dir / f"03_risco_por_{column}.png")


def plot_numeric_distributions(
    frame: pd.DataFrame, columns: list[str], output_dir: Path
) -> None:
    usable = [column for column in columns if frame[column].notna().any()]
    if not usable:
        return
    _style()
    n_columns = 2
    n_rows = int(np.ceil(len(usable) / n_columns))
    fig, axes = plt.subplots(n_rows, n_columns, figsize=(11, n_rows * 3.3))
    axes = np.atleast_1d(axes).ravel()
    for ax, column in zip(axes, usable):
        sns.histplot(frame[column], bins=30, color=BLUE, ax=ax)
        ax.set_title(column.replace("_", " ").title())
        ax.set_xlabel("")
    for ax in axes[len(usable) :]:
        ax.axis("off")
    fig.suptitle("Distribuicoes dos atributos numericos", y=1.01, fontweight="bold")
    fig.tight_layout()
    _save(fig, output_dir / "04_distribuicoes_numericas.png")


def plot_correlation_matrix(
    frame: pd.DataFrame, columns: list[str], output_dir: Path
) -> None:
    """Exibe associacoes monotônicas sem incluir a proficiencia vazada."""
    usable = [column for column in columns if column in frame.columns]
    usable = [column for column in usable if frame[column].notna().any()]
    if len(usable) < 2:
        return
    _style()
    labels = [DISPLAY_NAMES.get(column, column.replace("_", " ")) for column in usable]
    correlation = frame[usable].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(10.5, 8.2))
    sns.heatmap(
        correlation,
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        annot=True,
        fmt=".2f",
        annot_kws={"fontsize": 7},
        xticklabels=labels,
        yticklabels=labels,
        cbar_kws={"label": "Correlação de Spearman", "shrink": 0.75},
        ax=ax,
    )
    ax.set_title("Correlações entre atributos seguros e desfecho")
    ax.tick_params(axis="x", labelrotation=42, labelsize=8)
    ax.tick_params(axis="y", labelrotation=0, labelsize=8)
    fig.tight_layout()
    _save(fig, output_dir / "04_correlacoes_spearman.png")


def plot_model_evaluation(
    y_true: pd.Series,
    probability: np.ndarray,
    threshold: float,
    output_dir: Path,
) -> None:
    _style()
    prediction = (probability >= threshold).astype(int)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.1))
    RocCurveDisplay.from_predictions(
        y_true, probability, color=BLUE, name="Modelo", ax=axes[0]
    )
    axes[0].set_title("Curva ROC")
    axes[0].set_xlabel("Taxa de falsos positivos")
    axes[0].set_ylabel("Taxa de verdadeiros positivos")
    PrecisionRecallDisplay.from_predictions(
        y_true, probability, color=ORANGE, name="Modelo", ax=axes[1]
    )
    axes[1].set_title("Curva Precisao-Recall")
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precisão")
    ConfusionMatrixDisplay.from_predictions(
        y_true,
        prediction,
        display_labels=["Sem risco", "Em risco"],
        cmap="Blues",
        colorbar=False,
        ax=axes[2],
    )
    axes[2].set_title(f"Matriz de confusao (limiar={threshold:.3f})")
    axes[2].set_xlabel("Classe prevista")
    axes[2].set_ylabel("Classe real")
    fig.tight_layout()
    _save(fig, output_dir / "05_avaliacao_modelo.png")


def plot_feature_importance(importance: pd.DataFrame, output_dir: Path) -> None:
    if importance.empty:
        return
    _style()
    top = importance.head(15).sort_values("importancia_media")
    fig, ax = plt.subplots(figsize=(8.5, max(4.2, len(top) * 0.42)))
    labels = top["variavel"].map(lambda value: DISPLAY_NAMES.get(value, value))
    ax.barh(labels, top["importancia_media"], color=BLUE)
    ax.set_title("Importancia por permutacao")
    ax.set_xlabel("Queda media de PR-AUC")
    _save(fig, output_dir / "06_importancia_variaveis.png")


def plot_municipality_ranking(ranking: pd.DataFrame, output_dir: Path) -> None:
    if ranking.empty:
        return
    _style()
    eligible = ranking
    if "amostra_suficiente" in ranking.columns:
        eligible = ranking.loc[ranking["amostra_suficiente"]]
    top = eligible.head(20).sort_values("risco_previsto")
    fig, ax = plt.subplots(figsize=(9, 7))
    label_column = "nome_municipio" if "nome_municipio" in top.columns else "id_municipio"
    labels = top[label_column].fillna(top["id_municipio"]).astype(str)
    ax.barh(labels, top["risco_previsto"] * 100, color=RED)
    ax.set_title("Municípios prioritários no conjunto de teste")
    ax.set_xlabel("Probabilidade media de nao alfabetizacao (%)")
    ax.set_ylabel("Município" if label_column == "nome_municipio" else "Código IBGE")
    _save(fig, output_dir / "07_ranking_municipios.png")
