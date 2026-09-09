#!/usr/bin/env python3
"""Atualiza a referencia publica de codigos e nomes de municipios do IBGE."""

from __future__ import annotations

import json
import gzip
from pathlib import Path
from urllib.request import urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "reference" / "municipios_ibge.csv"
URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"


def main() -> None:
    with urlopen(URL, timeout=60) as response:  # noqa: S310 - fonte publica fixa do IBGE
        raw = response.read()
        if response.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
        payload = json.loads(raw.decode("utf-8"))
    rows = [
        {"id_municipio": str(item["id"]), "nome_municipio": item["nome"]}
        for item in payload
    ]
    frame = pd.DataFrame(rows).sort_values("id_municipio")
    if frame["id_municipio"].duplicated().any() or len(frame) < 5_500:
        raise ValueError("Resposta inesperada da API de Localidades do IBGE.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)
    print(f"Referencia criada: {OUTPUT} ({len(frame)} municipios)")


if __name__ == "__main__":
    main()
