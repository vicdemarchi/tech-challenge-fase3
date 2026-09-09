#!/usr/bin/env python3
"""Executa EDA, modelagem, avaliacao, ranking e segmentacao de ponta a ponta."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.evaluation.interpretability import permutation_feature_importance
from src.evaluation.metrics import (
    classification_metrics,
    select_balanced_accuracy_threshold,
)
from src.modeling.clustering import cluster_municipalities
from src.modeling.train import leakage_diagnostic, refit_selected, train_and_select
from src.preprocessing.schema import (
    GROUP_COLUMN,
    TARGET,
    load_dataset,
    normalize_known_units,
    prepare_target,
    select_features,
    validate_dataset,
)
from src.preprocessing.split import grouped_train_validation_test_split
from src.visualization.plots import (
    plot_feature_importance,
    plot_missingness,
    plot_correlation_matrix,
    plot_model_evaluation,
    plot_municipality_ranking,
    plot_numeric_distributions,
    plot_observed_risk_by_category,
    plot_target_distribution,
)


MINIMUM_MUNICIPAL_SAMPLE = 30


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV ou Parquet da tabela ML")
    parser.add_argument(
        "--output-root",
        default=None,
        help="Raiz alternativa para saidas; por padrao usa o repositorio.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Autoriza fixture sintetica e isola saidas em demo_outputs/.",
    )
    parser.add_argument(
        "--leakage-demo",
        action="store_true",
        help="Executa diagnostico separado usando proficiencia, se disponivel.",
    )
    return parser.parse_args()


def _directories(root: Path, demo: bool) -> dict[str, Path]:
    if demo:
        root = root / "demo_outputs"
    paths = {
        "processed": root / "data" / "processed",
        "images": root / "images",
        "models": root / "models",
        "reports": root / "reports",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def _assert_demo_safety(input_path: Path, demo: bool) -> None:
    looks_synthetic = "sintetic" in input_path.name.lower() or "fixture" in str(input_path).lower()
    if looks_synthetic and not demo:
        raise ValueError(
            "A entrada parece sintetica. Use --demo para impedir que resultados de teste "
            "sejam confundidos com evidencia real."
        )


def _ranking(
    test: pd.DataFrame,
    probability: np.ndarray,
    municipality_reference: pd.DataFrame | None = None,
) -> pd.DataFrame:
    columns = [GROUP_COLUMN, TARGET]
    optional = [
        "codigo_uf",
        "regiao",
        "meta_alfabetizacao_2025",
        "taxa_alfabetizacao_anterior",
    ]
    columns.extend(column for column in optional if column in test.columns)
    scored = test[columns].copy()
    scored["probabilidade_risco"] = probability
    aggregations: dict[str, str] = {
        TARGET: "mean",
        "probabilidade_risco": "mean",
    }
    for column in optional:
        if column in scored.columns:
            aggregations[column] = "first" if column in {"codigo_uf", "regiao"} else "median"
    ranking = scored.groupby(GROUP_COLUMN, as_index=False).agg(aggregations)
    counts = scored.groupby(GROUP_COLUMN).size().rename("n_estudantes_teste")
    ranking = ranking.join(counts, on=GROUP_COLUMN)
    ranking = ranking.rename(
        columns={
            TARGET: "risco_observado",
            "probabilidade_risco": "risco_previsto",
        }
    )
    ranking["taxa_alfabetizacao_prevista"] = (1 - ranking["risco_previsto"]) * 100
    standard_error = np.sqrt(
        ranking["risco_previsto"] * (1 - ranking["risco_previsto"])
        / ranking["n_estudantes_teste"].clip(lower=1)
    )
    ranking["risco_ic95_inferior"] = (ranking["risco_previsto"] - 1.96 * standard_error).clip(0, 1)
    ranking["risco_ic95_superior"] = (ranking["risco_previsto"] + 1.96 * standard_error).clip(0, 1)
    if "meta_alfabetizacao_2025" in ranking.columns:
        ranking["deficit_para_meta_pp"] = (
            ranking["meta_alfabetizacao_2025"]
            - ranking["taxa_alfabetizacao_prevista"]
        )
    ranking["amostra_suficiente"] = (
        ranking["n_estudantes_teste"] >= MINIMUM_MUNICIPAL_SAMPLE
    )
    if municipality_reference is not None and not municipality_reference.empty:
        reference = municipality_reference[[GROUP_COLUMN, "nome_municipio"]].copy()
        reference[GROUP_COLUMN] = reference[GROUP_COLUMN].astype("string")
        ranking[GROUP_COLUMN] = ranking[GROUP_COLUMN].astype("string")
        ranking = ranking.merge(reference.drop_duplicates(GROUP_COLUMN), on=GROUP_COLUMN, how="left")
    return ranking.sort_values(
        ["risco_previsto", "n_estudantes_teste"], ascending=[False, False]
    ).reset_index(drop=True)


def _load_municipality_reference(root: Path) -> pd.DataFrame | None:
    path = root / "data" / "reference" / "municipios_ibge.csv"
    if not path.exists():
        return None
    return pd.read_csv(path, dtype={GROUP_COLUMN: "string"})


def _write_eda_tables(frame: pd.DataFrame, features: list[str], output_dir: Path) -> None:
    numeric = [column for column in features if pd.api.types.is_numeric_dtype(frame[column])]
    correlations = (
        frame[numeric + [TARGET]]
        .corr(method="spearman")[TARGET]
        .drop(TARGET)
        .rename("correlacao_spearman_com_risco")
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"index": "variavel"})
    )
    correlations.to_csv(output_dir / "correlacoes_spearman.csv", index=False)

    quality = pd.DataFrame(
        {
            "variavel": frame.columns,
            "nulos": [int(frame[column].isna().sum()) for column in frame.columns],
            "percentual_nulos": [float(frame[column].isna().mean() * 100) for column in frame.columns],
        }
    ).sort_values("percentual_nulos", ascending=False)
    quality.to_csv(output_dir / "qualidade_dados.csv", index=False)

    for column in ["regiao", "sigla_uf"]:
        if column in frame.columns:
            summary = (
                frame.groupby(column, dropna=False)
                .agg(
                    n_estudantes=(TARGET, "size"),
                    n_municipios=(GROUP_COLUMN, "nunique"),
                    risco_observado=(TARGET, "mean"),
                )
                .sort_values("risco_observado", ascending=False)
                .reset_index()
            )
            summary.to_csv(output_dir / f"risco_por_{column}.csv", index=False)


def _markdown_table(frame: pd.DataFrame, decimals: int = 4) -> str:
    if frame.empty:
        return "_Sem resultado._"
    shown = frame.copy()
    for column in shown.select_dtypes(include="number").columns:
        shown[column] = shown[column].map(lambda value: f"{value:.{decimals}f}")
    header = "| " + " | ".join(shown.columns.astype(str)) + " |"
    separator = "|" + "|".join(["---"] * len(shown.columns)) + "|"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in shown.itertuples(index=False, name=None)
    ]
    return "\n".join([header, separator, *rows])


def _write_results_report(
    path: Path,
    demo: bool,
    features: list[str],
    validation: pd.DataFrame,
    test: pd.DataFrame,
    ranking: pd.DataFrame,
    importance: pd.DataFrame,
    leakage: dict[str, float | int | str] | None,
) -> None:
    status = (
        "**ATENCAO: RESULTADOS SINTETICOS PARA TESTE TECNICO. NAO USAR NA ENTREGA.**"
        if demo
        else "Resultados calculados sobre o arquivo real informado na execucao."
    )
    sections = [
        "# Resultados automaticos\n",
        status,
        "\n## Atributos do modelo\n",
        ", ".join(f"`{feature}`" for feature in features),
        "\n## Comparacao na validacao\n",
        _markdown_table(validation),
        "\n## Avaliacao final no teste\n",
        _markdown_table(test),
        "\n## Municipios prioritarios - primeiros 15\n",
        _markdown_table(ranking.head(15), decimals=3),
        "\n## Importancia por permutacao\n",
        _markdown_table(importance.head(15)),
    ]
    if leakage:
        sections.extend(
            [
                "\n## Diagnostico de vazamento\n",
                "Este experimento usa proficiencia, que define o rotulo. Serve apenas para demonstrar o atalho invalido.",
                _markdown_table(pd.DataFrame([leakage])),
            ]
        )
    path.write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    repository_root = Path(__file__).resolve().parent
    input_path = Path(args.input).resolve()
    _assert_demo_safety(input_path, args.demo)
    root = Path(args.output_root).resolve() if args.output_root else repository_root
    paths = _directories(root, args.demo)

    frame = normalize_known_units(load_dataset(input_path))
    unit_corrections = list(frame.attrs.get("unit_corrections", []))
    frame = prepare_target(frame)
    validate_dataset(frame)
    features = select_features(frame)

    plot_target_distribution(frame, paths["images"])
    plot_missingness(frame, features.all, paths["images"])
    plot_observed_risk_by_category(frame, "regiao", paths["images"])
    plot_observed_risk_by_category(frame, "rede_nome", paths["images"])
    plot_numeric_distributions(frame, features.numeric, paths["images"])
    plot_correlation_matrix(frame, features.numeric + [TARGET], paths["images"])
    _write_eda_tables(frame, features.numeric, paths["processed"])

    split = grouped_train_validation_test_split(frame)
    trained, validation_metrics = train_and_select(
        split.train, split.validation, features
    )
    threshold_high_recall = trained.threshold
    validation_probability = trained.pipeline.predict_proba(
        split.validation[features.all]
    )[:, 1]
    threshold_balanced = select_balanced_accuracy_threshold(
        split.validation[TARGET].to_numpy(), validation_probability
    )
    trained = refit_selected(trained, split.train, split.validation, features)

    probability = trained.pipeline.predict_proba(split.test[features.all])[:, 1]
    test_metric_rows = []
    for point, threshold in [
        ("triagem_alta_sensibilidade", threshold_high_recall),
        ("uso_equilibrado_recomendado", threshold_balanced),
    ]:
        metrics = classification_metrics(
            split.test[TARGET].to_numpy(), probability, threshold
        )
        metrics.update(
            {"modelo": trained.name, "ponto_operacao": point, "limiar": threshold}
        )
        test_metric_rows.append(metrics)
    test_metrics_frame = pd.DataFrame(test_metric_rows)
    test_metrics = test_metric_rows[1]

    predictions = split.test[
        [column for column in ["ano", GROUP_COLUMN, "id_aluno", TARGET] if column in split.test.columns]
    ].copy()
    predictions["probabilidade_risco"] = probability
    predictions["predicao_risco_alta_sensibilidade"] = (
        probability >= threshold_high_recall
    ).astype(int)
    predictions["predicao_risco_equilibrado"] = (
        probability >= threshold_balanced
    ).astype(int)
    ranking = _ranking(split.test, probability, _load_municipality_reference(root))
    priority_ranking = ranking.loc[ranking["amostra_suficiente"]].reset_index(drop=True)
    importance = permutation_feature_importance(
        trained.pipeline, split.test[features.all], split.test[TARGET]
    )
    clusters, cluster_profiles = cluster_municipalities(frame, features.numeric)

    validation_metrics.to_csv(paths["processed"] / "metricas_validacao.csv", index=False)
    test_metrics_frame.to_csv(paths["processed"] / "metricas_teste.csv", index=False)
    predictions.to_csv(paths["processed"] / "predicoes_teste.csv", index=False)
    ranking.to_csv(paths["processed"] / "ranking_municipios.csv", index=False)
    priority_ranking.to_csv(
        paths["processed"] / "ranking_municipios_prioritarios.csv", index=False
    )
    importance.to_csv(paths["processed"] / "importancia_variaveis.csv", index=False)
    if not clusters.empty:
        clusters.to_csv(paths["processed"] / "clusters_municipios.csv", index=False)
        cluster_profiles.to_csv(paths["processed"] / "perfis_clusters.csv", index=False)

    joblib.dump(
        {
            "pipeline": trained.pipeline,
            "thresholds": {
                "triagem_alta_sensibilidade": threshold_high_recall,
                "uso_equilibrado_recomendado": threshold_balanced,
            },
            "features": features.all,
            "target": TARGET,
            "positive_class": "nao_alfabetizado",
        },
        paths["models"] / "modelo_risco_alfabetizacao.joblib",
    )
    metadata = {
        "demo": bool(args.demo),
        "input": str(input_path),
        "n_rows": int(len(frame)),
        "n_municipalities": int(frame[GROUP_COLUMN].nunique()),
        "features": features.all,
        "selected_model": trained.name,
        "thresholds": {
            "triagem_alta_sensibilidade": threshold_high_recall,
            "uso_equilibrado_recomendado": threshold_balanced,
        },
        "minimum_municipal_sample": MINIMUM_MUNICIPAL_SAMPLE,
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "unit_corrections": unit_corrections,
        "split_rows": {
            "train": int(len(split.train)),
            "validation": int(len(split.validation)),
            "test": int(len(split.test)),
        },
    }
    (paths["processed"] / "metadados_execucao.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    leakage = None
    if args.leakage_demo and "proficiencia" in frame.columns:
        leakage = leakage_diagnostic(split.train, split.validation)
        pd.DataFrame([leakage]).to_csv(
            paths["processed"] / "diagnostico_vazamento.csv", index=False
        )

    plot_model_evaluation(
        split.test[TARGET], probability, threshold_balanced, paths["images"]
    )
    plot_feature_importance(importance, paths["images"])
    plot_municipality_ranking(priority_ranking, paths["images"])
    _write_results_report(
        paths["reports"] / "resultados_automaticos.md",
        args.demo,
        features.all,
        validation_metrics,
        test_metrics_frame,
        priority_ranking,
        importance,
        leakage,
    )
    print(
        f"Pipeline concluido. Modelo={trained.name}; PR-AUC teste={test_metrics['pr_auc']:.4f}; "
        f"saidas={paths['processed']}"
    )


if __name__ == "__main__":
    main()
