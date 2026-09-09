# Tech Challenge - Fase 3

## Predicao e Inteligencia Analitica para Alfabetizacao no Brasil

Este repositorio transforma a camada Gold da Fase 2 em uma solucao reproduzivel de Machine Learning para identificar estudantes e municipios com maior risco de nao alfabetizacao. O foco e apoiar priorizacao territorial e planejamento de politicas publicas, sem confundir predicao com causalidade.

> Status dos resultados: pipeline executado sobre a exportacao real de 160.978 registros e 5.350 municipios. A regressao logistica com `C=0,3` foi selecionada; no teste territorial obteve ROC-AUC de 0,661 e PR-AUC de 0,542. Resultados do modo `--demo` permanecem isolados e nunca sao usados como evidencia do projeto.

## 1. Problema e objetivo

O Indicador Crianca Alfabetizada classifica como alfabetizado o estudante com desempenho igual ou superior a 743 pontos na escala do Saeb. A base tratada na Fase 2 contem os anos de 2023 e 2024. Neste projeto, o evento positivo do modelo e **risco de nao alfabetizacao** (`1 = nao alfabetizado`), escolha que torna recall, precisao e ranking diretamente interpretaveis para a politica publica.

Objetivos:

- estimar a probabilidade individual de nao alfabetizacao;
- agregar probabilidades para priorizar municipios;
- identificar fatores preditivos, sem afirmar causalidade;
- agrupar municipios com perfis semelhantes;
- estimar distancia entre alfabetizacao prevista e meta futura;
- manter todo o pre-processamento dentro do pipeline para evitar vazamento.

## 2. Base de dados

### Origem principal

- projeto GCP: `tech-alfabetizacao-vdemarchi`;
- camada Silver: `silver.alunos`;
- camada Gold: `gold.indicador_municipio`;
- origem publica: Avaliacao da Alfabetizacao do Inep, distribuida pela Base dos Dados;
- enriquecimento: populacao e PIB municipal do IBGE, consultados nas tabelas publicas `basedosdados.br_ibge_populacao.municipio` e `basedosdados.br_ibge_pib.municipio`.

Auditorias da Fase 2 registraram 3.902.927 linhas preservadas entre Bronze e Silver, 3.867.999 registros de estudantes, 23.995 registros de resultados municipais, 5.550 municipios distintos e ausencia de chaves duplicadas nas tabelas Gold. Esses numeros sao verificacoes de engenharia, nao metricas do modelo.

### Unidade de analise

Cada linha representa um estudante apto a analise de desempenho em 2024. O rotulo e derivado de `alfabetizado_bool`; identificadores pessoais e escolares sao usados apenas para rastreabilidade ou separacao, nunca como atributos do modelo.

### Atributos permitidos no modelo principal

| Dimensao | Exemplos | Momento da informacao |
|---|---|---|
| Educacional | rede de ensino, taxa e media municipal de 2023, participacao anterior | anteriores ao desfecho de 2024 |
| Territorial | UF, regiao | estaveis |
| Socioeconomica | populacao 2023, PIB per capita 2023 | anteriores ao desfecho de 2024 |
| Politica publica | meta municipal de 2025 | meta conhecida, nao e resultado observado |

## 3. Vazamento de dados

O ponto metodologico mais importante e separar uma explicacao retrospectiva de uma previsao acionavel. `proficiencia`, `alfabetizado_codigo`, `alfabetizado_descricao`, indicadores municipais de 2024 e proporcoes dos niveis de desempenho do mesmo ano revelam direta ou indiretamente o rotulo. Eles sao bloqueados por `src/preprocessing/schema.py`.

O projeto permite um experimento diagnostico separado, executado com `--leakage-demo`, para demonstrar por que a proficiencia produz um desempenho irrealista. Esse modelo nao participa da selecao final e nao deve orientar intervencoes.

## 4. Desenho experimental

1. Filtragem de registros aptos e validacao do contrato de dados.
2. Rotulo `nao_alfabetizado = 1 - alfabetizado_bool`.
3. Separacao por grupos de municipio em treino (60%), validacao (20%) e teste (20%). Um municipio nao aparece em mais de uma particao.
4. Imputacao numerica pela mediana e categorica pela moda.
5. Padronizacao numerica e one-hot encoding dentro de `Pipeline`/`ColumnTransformer`.
6. Comparacao de baseline majoritario, regressao logistica e Random Forest.
7. Escolha por PR-AUC na validacao, adequada ao ranking da classe de risco.
8. Escolha de dois limiares na validacao: F2 para triagem ampla e acuracia balanceada para uso mais seletivo.
9. Avaliacao unica no teste, seguida de importancia por permutacao e ranking municipal com amostra minima.

A separacao agrupada testa generalizacao territorial. Como a base possui apenas 2023 e 2024 e os preditores historicos usam 2023, uma validacao temporal genuina deve ser repetida quando os rotulos de 2025 estiverem disponiveis.

## 5. Estrutura

```text
.
|-- data/                  # contrato e locais de entrada/saida
|-- docs/                  # decisoes, dicionario e guia de entrega
|-- images/                # graficos gerados
|-- models/                # modelo serializado
|-- reports/               # relatorio, model card e roteiro do video
|-- sql/                   # criacao da tabela ML e exportacao
|-- src/
|   |-- preprocessing/     # contrato, leakage e split
|   |-- modeling/          # treino e clusterizacao
|   |-- evaluation/        # metricas e interpretabilidade
|   `-- visualization/     # EDA e figuras finais
|-- tests/                 # testes unitarios e fixture sintetica identificada
`-- run_pipeline.py        # orquestracao ponta a ponta
```

## 6. Como reproduzir

### 6.1 Preparar a tabela no BigQuery

Abra `sql/01_criar_tabela_ml.sql`, confirme o projeto `tech-alfabetizacao-vdemarchi` e execute a consulta. Ela cria `gold.ml_alfabetizacao_fase3` com atributos anteriores ao desfecho. Depois execute `sql/02_exportar_amostra.sql` e salve o resultado como:

```text
data/raw/ml_alfabetizacao.csv
```

O procedimento detalhado esta em `docs/como_exportar_bigquery.md`.

O SQL atual calcula PIB per capita sem multiplicacao adicional. Para garantir reproducibilidade com exportacoes antigas, o carregador tambem detecta a assinatura de valores mil vezes maiores, corrige a unidade e registra a decisao em `data/processed/metadados_execucao.json`.

### 6.2 Instalar e executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_pipeline.py --input data/raw/ml_alfabetizacao.csv
```

Para um teste rapido da instalacao, sem produzir evidencia academica:

```bash
python run_pipeline.py --input tests/fixtures/amostra_teste_sintetica.csv --demo
```

## 7. Saidas automaticas

- `models/modelo_risco_alfabetizacao.joblib`;
- `data/processed/metricas_validacao.csv` e `metricas_teste.csv`;
- `data/processed/predicoes_teste.csv`;
- `data/processed/ranking_municipios.csv`;
- `data/processed/ranking_municipios_prioritarios.csv`, com pelo menos 30 registros por municipio;
- `data/processed/importancia_variaveis.csv`;
- `data/processed/correlacoes_spearman.csv`, `qualidade_dados.csv` e resumos por UF/regiao;
- `data/processed/clusters_municipios.csv`;
- figuras de EDA, matriz de confusao, ROC/PR, importancia e ranking em `images/`;
- `reports/resultados_automaticos.md` com as tabelas prontas para incorporar ao relatorio final.

## 8. Interpretacao para negocio

- **Fatores mais associados:** avaliados pela importancia por permutacao e SHAP. Sao sinais preditivos, nao estimativas causais.
- **Municipios em risco:** ordenados pela probabilidade media prevista, com intervalo de incerteza aproximado e tamanho da amostra.
- **Regioes semelhantes:** clusters municipais formados apenas com caracteristicas de contexto, sem usar o rotulo atual.
- **Meta futura:** a taxa prevista de alfabetizacao e comparada com a meta municipal de 2025; municipios com maior deficit entram primeiro na fila de diagnostico.
- **Uso recomendado:** priorizar apoio pedagogico e investigacao local. Nunca negar recursos ou rotular definitivamente um aluno apenas com base no escore.

### Resultado principal

| Indicador no teste | Resultado |
|---|---:|
| Registros / municipios | 33.032 / 1.070 |
| Prevalencia de risco | 39,7% |
| ROC-AUC | 0,661 |
| PR-AUC | 0,542 |
| Ganho relativo de PR-AUC sobre a prevalencia | 36,5% |
| Limiar equilibrado | 0,515 |
| Precisao / recall no limiar equilibrado | 53,5% / 49,4% |

Os atributos sao principalmente municipais. Assim, o escore serve para ordenar territorios e nao para diagnosticar individualmente estudantes. No ranking de teste com pelo menos 30 registros, as primeiras localidades foram Senhor do Bonfim (BA), Paulo Afonso (BA), Pilao Arcado (BA), Santa Cruz (RN) e Remanso (BA).

## 9. Limitacoes e etica

- A base nao contem fatores individuais como renda familiar, deficiencia, lingua materna ou trajetoria escolar; variaveis municipais nao substituem essas informacoes.
- O desenho e preditivo e observacional. Importancia de atributo nao prova causa.
- Estudantes de um mesmo municipio recebem o mesmo escore nesta versao, pois nao ha atributos individuais seguros disponiveis.
- Resultados podem refletir desigualdades historicas e diferencas de participacao na avaliacao.
- A decisao final deve permanecer humana, com monitoramento por UF, regiao e rede.
- A calibracao deve ser revista a cada nova edicao; 2025 e a primeira oportunidade de teste temporal real.
- Identificadores de estudante nao devem ser publicados. O repositorio versiona apenas codigo e resultados agregados.

## 10. Materiais de entrega

- `reports/relatorio_tecnico.pdf`: documento principal;
- `reports/roteiro_video_5min.md`: texto cronometrado para gravacao;
- `reports/guia_defesa.md`: respostas curtas para perguntas da banca;
- `docs/plano_git.md`: historico de commits, branch e pull request sugeridos;
- `docs/checklist_entrega.md`: verificacao final.

## 11. Referencias

- INEP. Avaliacao da Alfabetizacao: https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao
- Base dos Dados. Indicador Crianca Alfabetizada: https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72
- scikit-learn. Pipeline e avaliacao de modelos: https://scikit-learn.org/stable/

## Equipe

Preencher nomes e RM antes da entrega.
