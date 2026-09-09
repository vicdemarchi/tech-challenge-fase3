# Dados

Os microdados nao sao versionados por privacidade e volume.

## Entrada esperada

Salve a exportacao de `sql/02_exportar_amostra.sql` em:

```text
data/raw/ml_alfabetizacao.csv
```

Colunas minimas: `id_municipio`, `alfabetizado_bool` e pelo menos um atributo seguro listado em `docs/dicionario_dados.md`.

## Saidas

O pipeline grava metricas, predicoes anonimizadas, ranking municipal, importancia de atributos e clusters em `data/processed/`. Esses arquivos tambem ficam fora do Git por serem derivados da execucao local.

## Fixture

`tests/fixtures/amostra_teste_sintetica.csv` e um conjunto pequeno, inventado e explicitamente marcado. Sua unica finalidade e provar que o codigo executa; seus resultados nao podem ser usados no relatorio academico.

