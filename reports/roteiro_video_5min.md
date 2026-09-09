# Roteiro do vídeo executivo - até 5 minutos

## Antes de gravar

Preencha apenas os campos entre colchetes usando `reports/resultados_automaticos.md`. Não use os números do modo `--demo`. Mostre no vídeo o PDF do relatório ou cinco slides simples com as imagens indicadas.

## 0:00-0:35 - Abertura e problema

**Tela:** título do projeto e imagem `00_panorama_nacional.png`.

> Olá. Este projeto usa Machine Learning e inteligência analítica para apoiar a alfabetização no Brasil. O problema é que o resultado oficial mostra quem atingiu o padrão depois da avaliação. Para apoiar uma ação preventiva, construímos uma solução que estima o risco de não alfabetização e transforma esse risco em uma priorização de municípios.

## 0:35-1:15 - Evidências da base

**Tela:** imagem `00_qualidade_base.png`.

> A base da Fase 2 possui 3 milhões 867 mil 999 registros de estudantes de 2023 e 2024. Cerca de 3,35 milhões estavam aptos à análise de desempenho. No Brasil, a taxa observada aumentou de 55,9% em 2023 para 59,2% em 2024, mas ainda ficou 0,7 ponto percentual abaixo da meta daquele ano. Nas comparações municipais válidas, 46,7% ficaram abaixo da meta. Portanto, existe avanço agregado, mas também uma necessidade clara de priorização territorial.

## 1:15-2:05 - Desenho sem vazamento

**Tela:** imagem `00_fluxo_metodologico.png`.

> A decisão técnica mais importante foi não usar proficiência nem indicadores calculados do próprio resultado de 2024. A proficiência define o rótulo de alfabetização; usá-la criaria uma previsão circular e inútil antes da prova. O modelo principal usa o histórico municipal de 2023, participação anterior, UF, região, população, PIB per capita e a meta conhecida para 2025. Todo o pré-processamento está dentro de um pipeline, com imputação, padronização e codificação de categorias.

## 2:05-2:50 - Treino e avaliação

**Tela:** `05_avaliacao_modelo.png` e tabela de métricas.

> Os estudantes foram separados em treino, validação e teste na proporção aproximada de 60, 20 e 20 por cento. A separação foi feita por município, então uma localidade não aparece em mais de uma partição. Comparamos um baseline, duas regressões logísticas e duas configurações de Random Forest. O modelo selecionado foi [MODELO], com limiar [LIMIAR]. No teste, a PR-AUC foi [PR_AUC], o recall da classe de risco foi [RECALL], a precisão foi [PRECISAO] e o Brier score foi [BRIER]. Em relação ao baseline, [RESUMIR GANHO].

## 2:50-3:35 - Interpretação

**Tela:** `06_importancia_variaveis.png`.

> As variáveis com maior importância preditiva foram [VARIAVEL 1], [VARIAVEL 2] e [VARIAVEL 3]. A importância foi calculada por permutação no conjunto de teste: quanto mais a PR-AUC cai ao embaralhar uma variável, maior sua contribuição. Esses resultados mostram associação, não causalidade. Também monitoramos a diferença entre treino e validação para identificar sobreajuste.

## 3:35-4:20 - Inteligência municipal

**Tela:** `07_ranking_municipios.png` e primeiras linhas do ranking.

> Depois da previsão individual, agregamos as probabilidades por município. O ranking inclui risco médio, número de estudantes, intervalo de incerteza, taxa prevista de alfabetização e distância para a meta de 2025. Os municípios mais prioritários no conjunto de teste foram [MUNICIPIO 1], [MUNICIPIO 2] e [MUNICIPIO 3]. Também agrupamos municípios de contexto semelhante por clustering, permitindo desenhar carteiras de apoio com características próximas.

## 4:20-4:55 - Valor público e limites

**Tela:** resumo de recomendações.

> A aplicação recomendada é usar o ranking para iniciar diagnóstico pedagógico, direcionar formação, materiais e acompanhamento, sempre com decisão humana. O modelo não deve reprovar alunos, punir escolas ou retirar recursos. Entre as limitações estão apenas dois anos de dados, atributos socioeconômicos agregados e possível viés de ausência na avaliação. A próxima validação deve ser temporal, usando 2025 como teste externo.

## 4:55-5:00 - Encerramento

> Assim, a solução transforma dados históricos em uma fila transparente de investigação e apoio, com controle de vazamento, incerteza e reprodutibilidade. Obrigado.

## Checklist de gravação

- Duração alvo: 4min30s a 4min50s.
- Falar os números sem excesso de casas decimais.
- Mostrar o repositório por cinco segundos, incluindo `src`, `sql`, `reports` e testes.
- Não mostrar microdados, credenciais ou identificadores individuais.
- Inserir o link do GitHub na descrição ou tela final.

