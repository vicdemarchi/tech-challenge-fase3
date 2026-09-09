# Roteiro do vídeo executivo - até 5 minutos

## Antes de gravar

Use o PDF do relatório ou cinco slides simples com as imagens indicadas. Os números abaixo já correspondem à execução real; só falta adaptar a saudação aos integrantes do grupo.

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

> Os estudantes foram separados em treino, validação e teste na proporção aproximada de 60, 20 e 20 por cento. A separação foi feita por município, então uma localidade não aparece em mais de uma partição. Comparamos um baseline, duas regressões logísticas e duas configurações de Random Forest. A regressão logística regularizada venceu. Em municípios nunca vistos, a ROC-AUC foi 0,661 e a PR-AUC foi 0,542, ganho relativo de 36,5% sobre a prevalência de risco. No limiar equilibrado de 0,515, a precisão foi 53,5% e o recall, 49,4%. Uma triagem de alta sensibilidade chega a 95% de recall, mas sinaliza quase 89% da base; por isso o escore contínuo é mais útil para ordenar prioridades.

## 2:50-3:35 - Interpretação

**Tela:** `06_importancia_variaveis.png`.

> As variáveis com maior importância preditiva foram código da UF, média de Português de 2023 e taxa de alfabetização de 2023. Depois aparecem participação anterior e região. A importância foi calculada por permutação no conjunto de teste: quanto mais a PR-AUC cai ao embaralhar uma variável, maior sua contribuição. Isso mostra associação, não causalidade. Um diagnóstico que usou proficiência atingiu resultado perfeito justamente porque essa variável define o rótulo; ele demonstra o vazamento e foi excluído da solução.

## 3:35-4:20 - Inteligência municipal

**Tela:** `07_ranking_municipios.png` e primeiras linhas do ranking.

> Depois da previsão, agregamos as probabilidades por município. O ranking inclui risco médio, número de estudantes, intervalo de incerteza, taxa prevista de alfabetização e distância para a meta de 2025. Para reduzir instabilidade, destacamos apenas localidades com pelo menos 30 registros no teste. As primeiras foram Senhor do Bonfim, Paulo Afonso e Pilão Arcado, na Bahia, seguidas de Santa Cruz, no Rio Grande do Norte, e Remanso, na Bahia. Também obtivemos três clusters de contexto, separando municípios com melhor histórico, histórico mais frágil e grandes centros.

## 4:20-4:55 - Valor público e limites

**Tela:** resumo de recomendações.

> A aplicação recomendada é usar o ranking para iniciar diagnóstico pedagógico, direcionar formação, materiais e acompanhamento, sempre com decisão humana. Como os atributos são municipais, alunos da mesma localidade recebem o mesmo escore: ele não deve reprovar alunos, punir escolas ou retirar recursos. Entre as limitações estão apenas dois anos de dados, atributos agregados e possível viés de ausência. A próxima validação deve ser temporal, usando 2025 como teste externo.

## 4:55-5:00 - Encerramento

> Assim, a solução transforma dados históricos em uma fila transparente de investigação e apoio, com controle de vazamento, incerteza e reprodutibilidade. Obrigado.

## Checklist de gravação

- Duração alvo: 4min30s a 4min50s.
- Falar os números sem excesso de casas decimais.
- Mostrar o repositório por cinco segundos, incluindo `src`, `sql`, `reports` e testes.
- Não mostrar microdados, credenciais ou identificadores individuais.
- Inserir o link do GitHub na descrição ou tela final.
