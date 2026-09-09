#!/usr/bin/env python3
"""Gera figuras documentais a partir de evidencias agregadas da Fase 2."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"
OUTPUT = ROOT / "images"
OUTPUT.mkdir(parents=True, exist_ok=True)

NAVY = "#123047"
BLUE = "#2563EB"
TEAL = "#0F766E"
ORANGE = "#EA580C"
RED = "#B91C1C"
GRAY = "#64748B"


def setup() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 220,
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.titlecolor": NAVY,
            "axes.labelcolor": NAVY,
        }
    )


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(OUTPUT / filename, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def panorama_nacional() -> None:
    observed = pd.read_csv(REFERENCE / "fase2_brasil.csv")
    goals = pd.read_csv(REFERENCE / "metas_brasil.csv")
    fig, ax = plt.subplots(figsize=(10.5, 5.3))
    ax.plot(
        goals["ano"], goals["meta_alfabetizacao"],
        color=ORANGE, marker="o", linewidth=2.4, label="Trajetoria da meta"
    )
    ax.plot(
        observed["ano"], observed["taxa_alfabetizacao"],
        color=TEAL, marker="o", linewidth=3.0, markersize=8, label="Resultado observado"
    )
    for row in observed.itertuples():
        ax.annotate(
            f"{row.taxa_alfabetizacao:.1f}%",
            (row.ano, row.taxa_alfabetizacao),
            xytext=(0, 11), textcoords="offset points", ha="center", fontweight="bold"
        )
    ax.fill_between(
        goals["ano"], goals["meta_alfabetizacao"], 50, color=ORANGE, alpha=0.06
    )
    ax.set_title(
        "Alfabetizacao nacional: avanco recente e distancia para 2030",
        loc="left", fontsize=15
    )
    ax.text(
        2023, 51.3, "2024 ficou 0,7 p.p. abaixo da meta de 59,9%",
        color=RED, fontsize=10
    )
    ax.set_ylabel("Estudantes alfabetizados (%)")
    ax.set_xlabel("")
    ax.set_xticks(range(2023, 2031))
    ax.set_ylim(50, 83)
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "00_panorama_nacional.png")


def qualidade_base() -> None:
    audit = pd.read_csv(REFERENCE / "auditoria_fase2.csv").set_index("indicador")["valor"]
    total = int(audit["registros_alunos"])
    not_eligible = int(audit["registros_nao_aptos"])
    eligible = total - not_eligible
    comparisons = int(audit["comparacoes_municipais_com_meta"])
    met = int(audit["municipios_atingiram_ou_superaram"])
    below = int(audit["municipios_abaixo_da_meta"])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    axes[0].bar(["Aptos", "Nao aptos"], [eligible, not_eligible], color=[TEAL, GRAY])
    axes[0].set_title("Registros de estudantes")
    axes[0].set_ylabel("Quantidade")
    axes[0].set_ylim(0, 3_750_000)
    axes[0].ticklabel_format(axis="y", style="plain")
    axes[0].text(
        0, eligible * 1.02, f"{eligible/1e6:.2f} mi", ha="center", fontweight="bold"
    )
    axes[0].text(
        1, not_eligible * 1.08, f"{not_eligible/1e3:.0f} mil", ha="center", fontweight="bold"
    )

    axes[1].bar(["Atingiu/superou", "Abaixo"], [met, below], color=[TEAL, RED])
    axes[1].set_title("Comparacoes municipais com meta", pad=12)
    axes[1].set_ylabel("Linhas municipio-ano")
    axes[1].set_ylim(0, 3_350)
    axes[1].text(
        0, met + 80,
        f"{met:,}\n({met/comparisons:.1%})".replace(",", "."),
        ha="center", fontweight="bold"
    )
    axes[1].text(
        1, below + 80,
        f"{below:,}\n({below/comparisons:.1%})".replace(",", "."),
        ha="center", fontweight="bold"
    )
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(
        "Base pronta para analise, com recorte explicito de elegibilidade",
        fontsize=15, fontweight="bold", color=NAVY
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save(fig, "00_qualidade_base.png")


def fluxo_metodologico() -> None:
    fig, ax = plt.subplots(figsize=(12, 3.4))
    ax.axis("off")
    labels = [
        "Silver\nalunos 2024",
        "Gold 2023 +\nIBGE 2023",
        "Split por\nmunicipio",
        "Pipeline +\nmodelos",
        "Risco + ranking\n+ interpretacao",
    ]
    colors = [NAVY, BLUE, TEAL, ORANGE, RED]
    x_positions = [0.03, 0.23, 0.43, 0.63, 0.83]
    for index, (x, label, color) in enumerate(zip(x_positions, labels, colors)):
        box = plt.Rectangle(
            (x, 0.35), 0.14, 0.34, facecolor=color, edgecolor="none", alpha=0.96
        )
        ax.add_patch(box)
        ax.text(
            x + 0.07, 0.52, label, ha="center", va="center",
            color="white", fontweight="bold", fontsize=10
        )
        if index < len(labels) - 1:
            ax.annotate(
                "", xy=(x + 0.19, 0.52), xytext=(x + 0.145, 0.52),
                arrowprops={"arrowstyle": "->", "color": GRAY, "lw": 2}
            )
    ax.text(
        0.03, 0.82, "Desenho preditivo sem vazamento do resultado de 2024",
        fontsize=15, fontweight="bold", color=NAVY
    )
    ax.text(
        0.03, 0.16,
        "Proficiencia e agregacoes do proprio desfecho sao bloqueadas no modelo principal.",
        fontsize=10.5, color=GRAY
    )
    save(fig, "00_fluxo_metodologico.png")


if __name__ == "__main__":
    setup()
    panorama_nacional()
    qualidade_base()
    fluxo_metodologico()
    print(f"Figuras geradas em {OUTPUT}")
