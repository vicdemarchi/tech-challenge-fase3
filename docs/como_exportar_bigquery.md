# Como gerar o unico arquivo de dados necessario

Este procedimento usa o mesmo projeto GCP da Fase 2: `tech-alfabetizacao-vdemarchi`.

## Passo 1 - criar a tabela analitica

1. Abra o BigQuery Studio no Google Cloud.
2. Selecione o projeto `tech-alfabetizacao-vdemarchi`.
3. Abra uma nova consulta e cole todo o conteudo de `sql/01_criar_tabela_ml.sql`.
4. Confira a estimativa de bytes processados exibida pelo BigQuery.
5. Execute. A tabela `gold.ml_alfabetizacao_fase3` sera criada e a ultima consulta mostrara a cobertura.

## Passo 2 - auditar

Execute `sql/03_auditar_tabela_ml.sql`. Os cinco testes da primeira tabela devem retornar zero falhas. A segunda tabela mostra a cobertura municipal dos atributos; valores ausentes sao aceitos e tratados no pipeline, mas precisam ser documentados.

## Passo 3 - exportar uma amostra local

1. Execute `sql/02_exportar_amostra.sql`.
2. Na grade de resultados, clique em **Salvar resultados** e escolha **CSV (arquivo local)**.
3. Renomeie o arquivo para `ml_alfabetizacao.csv`.
4. Coloque-o em `data/raw/`.

A consulta usa um hash e preserva aproximadamente 10% das linhas e a prevalencia natural. Se o download ultrapassar o limite da interface, altere o divisor de 10 para 20, execute novamente e exporte aproximadamente 5%.

## Passo 4 - executar o trabalho

Na raiz do repositorio:

```bash
python run_pipeline.py --input data/raw/ml_alfabetizacao.csv --leakage-demo
```

Os numeros finais ficam em `reports/resultados_automaticos.md`; os graficos, em `images/`.

## Privacidade

O SQL usa o identificador original apenas para construir uma amostra deterministica e nao o inclui no CSV. Nao envie nem publique a tabela `silver.alunos`, chaves de servico ou arquivos de credenciais.

