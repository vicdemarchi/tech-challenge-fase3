# Predicao e Inteligencia Analitica para Alfabetizacao no Brasil

**Tech Challenge - Fase 3**  
**Curso:** Pós-graduação em Inteligência Artificial  
**Equipe:** [preencher nomes e RM]  
**Data:** [preencher]

> Nota de integridade: a metodologia, o código e as evidências agregadas da Fase 2 estão concluídos. As métricas preditivas indicadas como "gerar com a base real" não foram inventadas; serão produzidas automaticamente após a exportação de `gold.ml_alfabetizacao_fase3` pelo SQL entregue no repositório. Resultados do modo sintético são bloqueados para uso acadêmico.

## Resumo executivo

O objetivo deste trabalho é antecipar o risco de não alfabetização de estudantes do 2º ano do Ensino Fundamental e transformar as probabilidades individuais em inteligência territorial para priorização de municípios. A solução reutiliza a arquitetura Bronze, Silver e Gold da Fase 2, incorpora contexto educacional defasado e atributos socioeconômicos do IBGE, compara modelos supervisionados e produz um ranking municipal interpretável.

A principal decisão metodológica foi excluir do modelo acionável a proficiência e qualquer indicador agregado do próprio resultado de 2024. Como a classificação oficial de alfabetização é definida pela proficiência, utilizar essa variável produziria um atalho circular, com aparência de excelente desempenho mas sem utilidade antes da avaliação. O modelo principal utiliza apenas informações de 2023, características territoriais estáveis e a meta de 2025.

A auditoria herdada da Fase 2 registra 3.867.999 linhas de estudantes, das quais 513.338 não estavam aptas à análise de desempenho. Restaram aproximadamente 3,35 milhões de registros aptos. A taxa nacional observada avançou de 55,9% em 2023 para 59,2% em 2024, aumento de 3,3 pontos percentuais, mas ficou 0,7 ponto abaixo da meta de 59,9%. Entre 5.232 comparações município-ano com meta, 2.788 (53,3%) atingiram ou superaram a referência e 2.444 (46,7%) ficaram abaixo. Esse quadro justifica uma ferramenta de triagem antecipada e territorial.

## 1. Contexto e problema de negócio

O Indicador Criança Alfabetizada considera alfabetizado o estudante que atinge o padrão de desempenho definido para a avaliação nacional. Na base utilizada, o corte corresponde a 743 pontos na escala do Saeb. Embora o indicador observado seja indispensável para monitoramento, ele chega depois da aplicação da avaliação. Para uma política pública ser preventiva, é necessário estimar risco antes que o resultado corrente seja conhecido.

Este trabalho responde a cinco perguntas:

1. Quais fatores disponíveis antes da avaliação estão mais associados ao risco de não alfabetização?
2. Quais municípios devem ser priorizados para diagnóstico e apoio?
3. Quais municípios possuem perfis contextuais semelhantes?
4. Qual é a distância entre a alfabetização prevista e a meta de 2025?
5. Como transformar o modelo em um instrumento de apoio, sem automatizar decisões sensíveis?

O produto analítico não substitui avaliação pedagógica, visita técnica ou decisão humana. Seu papel é ordenar prioridades sob restrição de recursos.

## 2. Dados, escopo e proveniência

### 2.1 Origem

A fonte principal é a Avaliação da Alfabetização do Inep, disponibilizada em formato tratado pela Base dos Dados. A Fase 2 integrou as tabelas no projeto GCP `tech-alfabetizacao-vdemarchi`, com as camadas:

- `silver.alunos`, contendo registros por estudante;
- `gold.indicador_municipio`, contendo metas, resultados e auditorias municipais;
- `gold.indicador_uf`, `gold.indicador_brasil` e `gold.evolucao_alfabetizacao`, utilizadas no contexto agregado;
- `quality.resumo_validacao_final`, com regras de qualidade.

O enriquecimento usa as tabelas públicas de população e PIB municipal do IBGE mantidas pela Base dos Dados. Todas as variáveis de contexto foram limitadas a 2023 para prever o desfecho de 2024.

### 2.2 Recorte analítico

- População-alvo: estudantes da rede municipal, 2º ano do Ensino Fundamental, presentes, com prova preenchida e registro apto.
- Unidade de modelagem: estudante.
- Unidade de decisão: município.
- Período do desfecho: 2024.
- Classe positiva: `nao_alfabetizado = 1`.
- Chave de separação: `id_municipio`.

A opção pela rede municipal mantém coerência com as metas e resultados de `gold.indicador_municipio`, que foram construídos para `rede_codigo = 3` na Fase 2.

### 2.3 Proteção de dados

O identificador do aluno é utilizado dentro do BigQuery apenas para construir uma amostra determinística e não é exportado. O repositório ignora microdados, credenciais, modelos e predições individuais. Apenas resultados agregados podem ser publicados.

## 3. Análise exploratória e qualidade

### 3.1 Volume e elegibilidade

A Silver contém 3.867.999 registros de estudantes em 2023 e 2024. A regra `apto_analise_desempenho` exclui 513.338 registros relacionados principalmente a ausência ou prova não preenchida. O conjunto potencialmente elegível tem 3.354.661 registros, ou 86,7% do total.

![Qualidade da base](../images/00_qualidade_base.png)

Essa exclusão não deve ser interpretada como erro de engenharia. Entretanto, pode produzir viés de seleção se a ausência estiver relacionada ao próprio risco de não alfabetização. Por isso, participação anterior entra como atributo e o relatório recomenda monitoramento separado dos não participantes.

### 3.2 Evolução nacional e metas

O resultado nacional aumentou de 55,9% para 59,2% entre 2023 e 2024. O avanço de 3,3 pontos percentuais não foi suficiente para alcançar a meta de 2024, de 59,9%. A trajetória registrada na fonte chega a 80% em 2030.

![Panorama nacional](../images/00_panorama_nacional.png)

O ganho nacional pode coexistir com forte heterogeneidade. Nas 5.232 linhas município-ano com comparação válida, 46,7% permaneceram abaixo da meta. Portanto, a média nacional não é suficiente para orientar alocação territorial.

### 3.3 Consistência e ausências

A tabela Gold municipal possui 10.951 chaves distintas e nenhuma duplicidade. Foram executadas 59 regras de qualidade. A auditoria de relacionamento identificou, em 2023, 4.596 pares correspondentes com diferenças entre taxas provenientes das tabelas de meta e de resultado; em 2024, as 5.352 chaves correspondentes apresentaram taxas iguais. O modelo utiliza explicitamente `taxa_alfabetizacao_resultado` de 2023, mantendo uma única definição documentada.

Também foram observadas 120 ausências de taxa ou participação municipal em 2023. O pipeline preserva os nulos e realiza imputação da mediana dentro de cada ajuste, evitando que estatísticas do teste contaminem o treino.

### 3.4 Hipóteses analíticas

- H1: municípios com menor taxa e menor média de Português em 2023 apresentam maior risco em 2024.
- H2: menor participação em 2023 está associada a maior incerteza e possível viés de seleção.
- H3: população e PIB per capita capturam diferenças de escala e capacidade socioeconômica, mas não representam renda individual.
- H4: persistem padrões regionais após controlar pelo histórico municipal.
- H5: um modelo não linear pode capturar interações, mas terá maior risco de sobreajuste que a regressão logística.

As hipóteses são preditivas. A confirmação de associação não constitui evidência causal.

## 4. Engenharia de atributos e vazamento

### 4.1 Atributos do modelo principal

| Grupo | Atributos |
|---|---|
| Educacional | taxa de alfabetização anterior, média de Português anterior, participação anterior, estudantes avaliados no ano anterior |
| Territorial | código da UF e região |
| Socioeconômico | população anterior e PIB per capita anterior |
| Planejamento | meta de alfabetização de 2025 |

### 4.2 Variáveis proibidas

`proficiencia`, `alfabetizado_codigo`, `alfabetizado_descricao`, taxas de alfabetização de 2024, média de Português de 2024 e proporções dos níveis 0 a 8 são bloqueadas. A proficiência não é apenas correlacionada ao alvo: ela participa de sua definição. Identificadores de estudante, escola e município também não são preditores, evitando memorização e alta cardinalidade; o município é somente o grupo do split.

Um teste automatizado falha caso uma coluna proibida seja incluída no conjunto de atributos. Um experimento diagnóstico opcional mostra a diferença entre um modelo circular com proficiência e o modelo acionável, sem permitir que o primeiro seja selecionado.

![Fluxo metodológico](../images/00_fluxo_metodologico.png)

## 5. Pipeline de Machine Learning

### 5.1 Pré-processamento integrado

O `ColumnTransformer` contém:

- mediana para valores numéricos ausentes;
- moda para categorias ausentes;
- padronização dos atributos numéricos;
- one-hot encoding com tratamento de categorias desconhecidas;
- exclusão de todas as colunas não aprovadas.

O transformador e o estimador são serializados juntos. Isso garante que treinamento e inferência executem as mesmas regras.

### 5.2 Particionamento

Foi adotada a proporção aproximada 60/20/20 para treino, validação e teste. `GroupShuffleSplit` mantém todos os estudantes de um município na mesma partição. Essa decisão produz uma avaliação mais exigente: o teste mede capacidade de generalizar para municípios não vistos, e não apenas para novos alunos de localidades já memorizadas.

Com apenas 2023 e 2024, e usando 2023 como histórico, não existe um terceiro ano para teste temporal completo. Quando o desfecho de 2025 estiver disponível, recomenda-se treinar até 2024 e testar exclusivamente em 2025.

### 5.3 Modelos e otimização

Foram preparados cinco candidatos:

1. `DummyClassifier` como baseline de prevalência;
2. regressão logística com `C = 0,3`;
3. regressão logística com `C = 1,0`;
4. Random Forest com profundidade máxima 16 e folha mínima 10;
5. Random Forest sem limite explícito de profundidade e folha mínima 20.

A comparação de hiperparâmetros ocorre somente na validação. O modelo com maior PR-AUC, excluído o baseline, é reajustado em treino mais validação. O limiar é escolhido na validação pelo maior F2, que atribui peso maior ao recall da classe de risco. O teste é acessado uma única vez.

### 5.4 Métricas

- PR-AUC: qualidade do ranking da classe de risco e critério principal.
- ROC-AUC: discriminação global.
- Recall: proporção de estudantes em risco identificados.
- Precisão: proporção dos alertas que corresponde ao evento observado.
- F2: síntese com prioridade para recall.
- Balanced accuracy: desempenho equilibrado entre classes.
- Brier score: qualidade probabilística e calibração.

O `gap_pr_auc` entre treino e validação é monitorado como sinal de sobreajuste.

## 6. Resultados do modelo

### 6.1 Comparação na validação

**Gerar com a base real:** copiar a tabela de `reports/resultados_automaticos.md` após executar o pipeline.

| Modelo | PR-AUC | ROC-AUC | Recall | Precisão | F2 | Gap treino-validação |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | a gerar | a gerar | a gerar | a gerar | a gerar | a gerar |
| Melhor candidato | a gerar | a gerar | a gerar | a gerar | a gerar | a gerar |

### 6.2 Avaliação final no teste

**Gerar com a base real:** inserir o modelo selecionado, o limiar e as métricas de `data/processed/metricas_teste.csv`.

Nenhuma métrica sintética foi transcrita para este documento. Essa escolha preserva a validade do trabalho e permite rastrear cada número até o arquivo real de entrada.

### 6.3 Interpretação

A importância por permutação mede a queda de PR-AUC quando cada atributo é embaralhado no teste. Valores maiores indicam maior contribuição preditiva. A interpretação deve observar duas regras:

1. importância não prova causalidade;
2. atributos correlacionados podem dividir importância entre si.

**Gerar com a base real:** inserir `images/06_importancia_variaveis.png` e discutir as cinco primeiras variáveis.

## 7. Inteligência municipal

### 7.1 Ranking de risco

As probabilidades individuais do teste são agregadas por município. Para cada localidade, a solução entrega risco médio, taxa prevista de alfabetização, intervalo aproximado de 95%, número de estudantes e déficit para a meta de 2025. O ranking prioriza o maior risco, mas o tamanho amostral e a incerteza devem ser considerados antes da ação.

**Gerar com a base real:** inserir `images/07_ranking_municipios.png` e os primeiros municípios de `ranking_municipios.csv`.

### 7.2 Municípios semelhantes

O módulo não supervisionado agrega atributos contextuais por município, padroniza as variáveis e testa de dois a cinco clusters. O número de grupos é escolhido pelo maior silhouette score. Como o alvo de 2024 não entra nessa etapa, os clusters descrevem contexto, não desempenho corrente.

O uso sugerido é criar carteiras de intervenção: municípios de um mesmo perfil podem compartilhar diagnóstico e desenho de apoio, desde que análises locais confirmem a semelhança.

### 7.3 Previsão de metas futuras

A taxa prevista é calculada como `100 x (1 - risco_medio)`. O déficit é `meta_2025 - taxa_prevista`. Valores positivos indicam necessidade estimada de avanço. Trata-se de previsão de cenário, não de garantia sobre o resultado futuro.

## 8. Respostas às perguntas de negócio

| Pergunta | Resposta entregue pela solução |
|---|---|
| Fatores de maior impacto | ranking de importância por permutação, acompanhado de direção da regressão logística e análise de SHAP opcional |
| Municípios em risco | ranking probabilístico agregado com tamanho amostral e intervalo de incerteza |
| Regiões com padrões semelhantes | clusters contextuais e perfis médios por grupo |
| Municípios sem resultado futuro | taxa prevista e déficit em relação à meta de 2025 |
| Influência das variáveis | comparação entre importância global e desempenho do modelo sem vazamento |

Os nomes e valores concretos dependem da execução com os microdados reais. O repositório produz todas as tabelas sem edição manual.

## 9. Aplicação em políticas públicas

Propõe-se um ciclo mensal ou trimestral de uso:

1. atualizar contexto e histórico;
2. calcular risco e incerteza;
3. selecionar municípios prioritários por risco, déficit e cobertura;
4. realizar diagnóstico pedagógico local;
5. pactuar apoio, formação e materiais;
6. medir participação e resultado da edição seguinte;
7. recalibrar o modelo e auditar diferenças entre grupos.

O escore não deve decidir matrícula, promoção, sanção, transferência de recursos ou rotulação individual. Uma política responsável usa o modelo para oferecer apoio adicional, nunca para retirar direitos.

## 10. Limitações

- A base tem apenas dois anos úteis para o desenho proposto.
- Atributos socioeconômicos são municipais e podem ocultar desigualdade interna.
- Estudantes ausentes ou sem prova preenchida não possuem desfecho observado.
- O split territorial é rigoroso, mas não substitui validação temporal.
- A amostra local reduz custo computacional, embora preserve a prevalência por hash.
- Mudanças de instrumento, política ou população podem causar drift.
- As associações não identificam efeito causal de uma intervenção.

## 11. Conclusão

O projeto entrega uma arquitetura preditiva reproduzível e alinhada ao uso público: dados defasados no tempo, proteção automatizada contra vazamento, comparação de modelos, escolha de limiar orientada ao risco, teste territorial e interpretação agregada. As evidências da Fase 2 mostram melhora nacional, mas também uma parcela expressiva de municípios abaixo das metas. A contribuição do modelo é transformar esse diagnóstico retrospectivo em uma fila de investigação antecipada, com incerteza e supervisão humana explícitas.

## Referências

- BRASIL. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira. Avaliação da Alfabetização. Disponível em: https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao.
- BASE DOS DADOS. Avaliação da Alfabetização. Disponível em: https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72.
- BASE DOS DADOS. População Brasileira. Disponível em: https://basedosdados.org/dataset/d30222ad-7a5c-4778-a1ec-f0785371d1ca.
- BASE DOS DADOS. Produto Interno Bruto (PIB). Disponível em: https://basedosdados.org/dataset/fcf025ca-8b19-4131-8e2d-5ddb12492347.
- SCIKIT-LEARN DEVELOPERS. Scikit-learn User Guide. Disponível em: https://scikit-learn.org/stable/user_guide.html.

