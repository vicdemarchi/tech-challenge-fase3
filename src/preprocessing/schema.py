"""Contrato de dados e protecao contra vazamento de alvo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


TARGET_SOURCE = "alfabetizado_bool"
TARGET = "nao_alfabetizado"
GROUP_COLUMN = "id_municipio"

NUMERIC_FEATURES = [
    "taxa_alfabetizacao_anterior",
    "media_portugues_anterior",
    "percentual_participacao_anterior",
    "total_alunos_avaliados_anterior",
    "populacao_anterior",
    "pib_per_capita_anterior",
    "meta_alfabetizacao_2025",
]

CATEGORICAL_FEATURES = [
    "rede_nome",
    "codigo_uf",
    "regiao",
]

# Colunas proibidas como preditores do modelo acionavel. Algumas podem estar no
# arquivo para auditoria, mas nunca entram no ColumnTransformer principal.
LEAKAGE_COLUMNS = {
    "proficiencia",
    "alfabetizado_codigo",
    "alfabetizado_descricao",
    "taxa_alfabetizacao",
    "taxa_alfabetizacao_resultado",
    "media_portugues",
    "total_alfabetizados",
    "nivel_0_percentual",
    "nivel_1_percentual",
    "nivel_2_percentual",
    "nivel_3_percentual",
    "nivel_4_percentual",
    "nivel_5_percentual",
    "nivel_6_percentual",
    "nivel_7_percentual",
    "nivel_8_percentual",
}


@dataclass(frozen=True)
class FeatureSet:
    numeric: list[str]
    categorical: list[str]

    @property
    def all(self) -> list[str]:
        return self.numeric + self.categorical


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Carrega CSV ou Parquet preservando identificadores como texto."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {path}")
    if path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(path)
    elif path.suffix.lower() in {".csv", ".txt"}:
        frame = pd.read_csv(path, dtype={GROUP_COLUMN: "string", "id_aluno": "string"})
    else:
        raise ValueError("Formato invalido. Use .csv ou .parquet.")
    frame.columns = [str(column).strip().lower() for column in frame.columns]
    return frame


def prepare_target(frame: pd.DataFrame) -> pd.DataFrame:
    """Cria o evento positivo de risco a partir do rotulo oficial."""
    if TARGET not in frame.columns:
        if TARGET_SOURCE not in frame.columns:
            raise ValueError(
                f"A base precisa conter '{TARGET_SOURCE}' ou '{TARGET}'."
            )
        source = pd.to_numeric(frame[TARGET_SOURCE], errors="coerce")
        frame = frame.copy()
        frame[TARGET] = 1 - source
    frame[TARGET] = pd.to_numeric(frame[TARGET], errors="coerce")
    frame = frame.loc[frame[TARGET].isin([0, 1])].copy()
    frame[TARGET] = frame[TARGET].astype("int8")
    return frame


def validate_dataset(frame: pd.DataFrame) -> None:
    """Falha cedo quando o contrato minimo nao e atendido."""
    missing = {GROUP_COLUMN, TARGET}.difference(frame.columns)
    if missing:
        raise ValueError(f"Colunas obrigatorias ausentes: {sorted(missing)}")
    if frame.empty:
        raise ValueError("A base ficou vazia apos a validacao do alvo.")
    if frame[GROUP_COLUMN].isna().any():
        raise ValueError("Existem linhas sem id_municipio; corrija antes do split.")
    if frame[TARGET].nunique() < 2:
        raise ValueError("O alvo precisa conter as duas classes (0 e 1).")
    if frame[GROUP_COLUMN].nunique() < 5:
        raise ValueError("Sao necessarios ao menos cinco municipios distintos.")


def select_features(frame: pd.DataFrame) -> FeatureSet:
    """Seleciona apenas atributos previamente aprovados e presentes."""
    numeric = [column for column in NUMERIC_FEATURES if column in frame.columns]
    categorical = [
        column for column in CATEGORICAL_FEATURES if column in frame.columns
    ]
    selected = set(numeric + categorical)
    leaked = selected.intersection(LEAKAGE_COLUMNS)
    if leaked:
        raise AssertionError(f"Vazamento detectado no conjunto de atributos: {leaked}")
    if not selected:
        raise ValueError(
            "Nenhum atributo seguro foi encontrado. Consulte docs/dicionario_dados.md."
        )
    return FeatureSet(numeric=numeric, categorical=categorical)


def assert_no_leakage(columns: Iterable[str]) -> None:
    """Protecao reutilizavel para testes e futuras alteracoes."""
    normalized = {str(column).strip().lower() for column in columns}
    leaked = normalized.intersection(LEAKAGE_COLUMNS | {TARGET_SOURCE, TARGET})
    if leaked:
        raise ValueError(f"Colunas com vazamento nao podem ser preditores: {sorted(leaked)}")

