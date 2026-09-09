# Resultados automaticos


Resultados calculados sobre o arquivo real informado na execucao.


## Atributos do modelo


`taxa_alfabetizacao_anterior`, `media_portugues_anterior`, `percentual_participacao_anterior`, `total_alunos_avaliados_anterior`, `populacao_anterior`, `pib_per_capita_anterior`, `meta_alfabetizacao_2025`, `rede_nome`, `codigo_uf`, `regiao`


## Comparacao na validacao


| n | prevalencia_risco | roc_auc | pr_auc | accuracy | balanced_accuracy | precision | recall | f1 | f2 | brier | taxa_alertas | verdadeiros_negativos | falsos_positivos | falsos_negativos | verdadeiros_positivos | modelo | limiar | pr_auc_treino | roc_auc_treino | gap_pr_auc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 35869.0000 | 0.4199 | 0.6543 | 0.5442 | 0.4630 | 0.5353 | 0.4381 | 0.9869 | 0.6068 | 0.7892 | 0.2360 | 0.9459 | 1741.0000 | 19065.0000 | 198.0000 | 14865.0000 | regressao_logistica_c0_3 | 0.2300 | 0.5608 | 0.6700 | 0.0166 |
| 35869.0000 | 0.4199 | 0.6542 | 0.5438 | 0.4630 | 0.5353 | 0.4381 | 0.9869 | 0.6068 | 0.7892 | 0.2361 | 0.9459 | 1741.0000 | 19065.0000 | 198.0000 | 14865.0000 | regressao_logistica_c1_0 | 0.2300 | 0.5608 | 0.6700 | 0.0170 |
| 35869.0000 | 0.4199 | 0.6531 | 0.5409 | 0.4617 | 0.5342 | 0.4375 | 0.9872 | 0.6063 | 0.7890 | 0.2338 | 0.9475 | 1691.0000 | 19115.0000 | 193.0000 | 14870.0000 | random_forest_depth16_leaf10 | 0.2400 | 0.6002 | 0.7024 | 0.0593 |
| 35869.0000 | 0.4199 | 0.6530 | 0.5407 | 0.4676 | 0.5389 | 0.4401 | 0.9845 | 0.6083 | 0.7892 | 0.2335 | 0.9393 | 1942.0000 | 18864.0000 | 234.0000 | 14829.0000 | random_forest_leaf20 | 0.2400 | 0.5975 | 0.7008 | 0.0568 |
| 35869.0000 | 0.4199 | 0.5000 | 0.4199 | 0.4199 | 0.5000 | 0.4199 | 1.0000 | 0.5915 | 0.7835 | 0.2438 | 1.0000 | 0.0000 | 20806.0000 | 0.0000 | 15063.0000 | baseline_majoritario | 0.0500 | 0.4044 | 0.5000 | -0.0156 |


## Avaliacao final no teste


| n | prevalencia_risco | roc_auc | pr_auc | accuracy | balanced_accuracy | precision | recall | f1 | f2 | brier | taxa_alertas | verdadeiros_negativos | falsos_positivos | falsos_negativos | verdadeiros_positivos | modelo | ponto_operacao | limiar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 33032.0000 | 0.3974 | 0.6614 | 0.5423 | 0.4695 | 0.5513 | 0.4250 | 0.9499 | 0.5873 | 0.7618 | 0.2251 | 0.8881 | 3039.0000 | 16867.0000 | 657.0000 | 12469.0000 | regressao_logistica_c0_3 | triagem_alta_sensibilidade | 0.2300 |
| 33032.0000 | 0.3974 | 0.6614 | 0.5423 | 0.6284 | 0.6055 | 0.5352 | 0.4936 | 0.5136 | 0.5014 | 0.2251 | 0.3665 | 14279.0000 | 5627.0000 | 6647.0000 | 6479.0000 | regressao_logistica_c0_3 | uso_equilibrado_recomendado | 0.5150 |


## Municipios prioritarios - primeiros 15


| id_municipio | risco_observado | risco_previsto | codigo_uf | regiao | meta_alfabetizacao_2025 | taxa_alfabetizacao_anterior | n_estudantes_teste | taxa_alfabetizacao_prevista | risco_ic95_inferior | risco_ic95_superior | deficit_para_meta_pp | amostra_suficiente | nome_municipio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2930105 | 0.776 | 0.813 | 29.000 | Nordeste | 35.500 | 19.930 | 58.000 | 18.667 | 0.713 | 0.914 | 16.833 | True | Senhor do Bonfim |
| 2924009 | 0.677 | 0.806 | 29.000 | Nordeste | 40.210 | 24.790 | 99.000 | 19.375 | 0.728 | 0.884 | 20.835 | True | Paulo Afonso |
| 2924405 | 0.775 | 0.796 | 29.000 | Nordeste | 39.380 | 23.900 | 40.000 | 20.384 | 0.671 | 0.921 | 18.996 | True | Pilão Arcado |
| 2411205 | 0.553 | 0.784 | 24.000 | Nordeste | 36.930 | 21.350 | 38.000 | 21.628 | 0.653 | 0.915 | 15.302 | True | Santa Cruz |
| 2926004 | 0.528 | 0.779 | 29.000 | Nordeste | 40.500 | 25.100 | 36.000 | 22.129 | 0.643 | 0.914 | 18.371 | True | Remanso |
| 2907103 | 0.683 | 0.773 | 29.000 | Nordeste | 43.560 | 28.550 | 41.000 | 22.728 | 0.644 | 0.901 | 20.832 | True | Carinhanha |
| 2407104 | 0.707 | 0.762 | 24.000 | Nordeste | 44.070 | 29.150 | 58.000 | 23.782 | 0.653 | 0.872 | 20.288 | True | Macaíba |
| 2925501 | 0.839 | 0.747 | 29.000 | Nordeste | 48.750 | 34.880 | 31.000 | 25.331 | 0.594 | 0.900 | 23.419 | True | Prado |
| 1303536 | 0.617 | 0.747 | 13.000 | Norte | 48.190 | 34.170 | 47.000 | 25.335 | 0.622 | 0.871 | 22.855 | True | Presidente Figueiredo |
| 4314902 | 0.766 | 0.740 | 43.000 | Sul | nan | 40.040 | 248.000 | 25.959 | 0.686 | 0.795 | nan | True | Porto Alegre |
| 1500701 | 0.576 | 0.736 | 15.000 | Norte | 42.040 | 26.810 | 33.000 | 26.392 | 0.586 | 0.886 | 15.648 | True | Anajás |
| 1507003 | 0.576 | 0.733 | 15.000 | Norte | 41.060 | 25.720 | 33.000 | 26.659 | 0.583 | 0.884 | 14.401 | True | Santo Antônio do Tauá |
| 1600501 | 0.848 | 0.728 | 16.000 | Norte | 41.390 | 26.090 | 46.000 | 27.245 | 0.599 | 0.856 | 14.145 | True | Oiapoque |
| 2926608 | 0.553 | 0.727 | 29.000 | Nordeste | 48.370 | 34.390 | 47.000 | 27.272 | 0.600 | 0.855 | 21.098 | True | Ribeira do Pombal |
| 2933208 | 0.500 | 0.721 | 29.000 | Nordeste | 52.020 | 39.140 | 36.000 | 27.936 | 0.574 | 0.867 | 24.084 | True | Vera Cruz |


## Importancia por permutacao


| variavel | importancia_media | importancia_desvio |
|---|---|---|
| codigo_uf | 0.0333 | 0.0025 |
| media_portugues_anterior | 0.0257 | 0.0030 |
| taxa_alfabetizacao_anterior | 0.0182 | 0.0025 |
| percentual_participacao_anterior | 0.0048 | 0.0017 |
| regiao | 0.0037 | 0.0017 |
| rede_nome | 0.0000 | 0.0000 |
| meta_alfabetizacao_2025 | -0.0005 | 0.0003 |
| pib_per_capita_anterior | -0.0006 | 0.0003 |
| total_alunos_avaliados_anterior | -0.0008 | 0.0002 |
| populacao_anterior | -0.0010 | 0.0002 |


## Diagnostico de vazamento


Este experimento usa proficiencia, que define o rotulo. Serve apenas para demonstrar o atalho invalido.

| n | prevalencia_risco | roc_auc | pr_auc | accuracy | balanced_accuracy | precision | recall | f1 | f2 | brier | taxa_alertas | verdadeiros_negativos | falsos_positivos | falsos_negativos | verdadeiros_positivos | modelo | limiar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 35869.0000 | 0.4199 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0003 | 0.4199 | 20806.0000 | 0.0000 | 0.0000 | 15063.0000 | diagnostico_com_proficiencia | 0.4650 |
