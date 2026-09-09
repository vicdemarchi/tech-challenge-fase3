-- Tech Challenge Fase 3
-- Cria a tabela analitica com desfecho de 2024 e atributos disponiveis antes dele.
-- O escopo principal e a rede municipal, coerente com indicador_municipio da Fase 2.
-- Revise os bytes estimados pelo BigQuery antes de executar.

CREATE OR REPLACE TABLE
  `tech-alfabetizacao-vdemarchi.gold.ml_alfabetizacao_fase3`
OPTIONS (
  description = 'Base ML da Fase 3: estudantes municipais de 2024, contexto 2023, meta 2025 e atributos socioeconomicos 2023'
)
AS
WITH alunos_2024 AS (
  SELECT
    ano,
    id_municipio,
    id_aluno,
    rede_nome,
    alfabetizado_bool,
    proficiencia,
    peso_aluno
  FROM `tech-alfabetizacao-vdemarchi.silver.alunos`
  WHERE ano = 2024
    AND rede_codigo = 3
    AND registro_estrutural_valido
    AND apto_analise_desempenho
    AND id_municipio IS NOT NULL
    AND alfabetizado_bool IS NOT NULL
),
contexto_educacional_2023 AS (
  SELECT
    id_municipio,
    taxa_alfabetizacao_resultado AS taxa_alfabetizacao_anterior,
    media_portugues AS media_portugues_anterior,
    percentual_participacao AS percentual_participacao_anterior,
    total_alunos_aptos_analise AS total_alunos_avaliados_anterior
  FROM `tech-alfabetizacao-vdemarchi.gold.indicador_municipio`
  WHERE ano = 2023
),
metas_2025 AS (
  SELECT
    id_municipio,
    ANY_VALUE(meta_alfabetizacao_2025) AS meta_alfabetizacao_2025
  FROM `tech-alfabetizacao-vdemarchi.gold.indicador_municipio`
  WHERE meta_alfabetizacao_2025 IS NOT NULL
  GROUP BY id_municipio
),
populacao_2023 AS (
  SELECT id_municipio, populacao
  FROM `basedosdados.br_ibge_populacao.municipio`
  WHERE ano = 2023
),
pib_2023 AS (
  SELECT id_municipio, pib
  FROM `basedosdados.br_ibge_pib.municipio`
  WHERE ano = 2023
),
diretorio AS (
  SELECT id_municipio, sigla_uf, nome_regiao
  FROM `basedosdados.br_bd_diretorios_brasil.municipio`
)
SELECT
  a.ano,
  a.id_municipio,
  -- Hash operacional para amostragem; o identificador original do aluno nao sai da Silver.
  FARM_FINGERPRINT(CONCAT(a.id_municipio, '|', a.id_aluno)) AS id_registro_hash,
  a.rede_nome,
  SUBSTR(a.id_municipio, 1, 2) AS codigo_uf,
  d.sigla_uf,
  d.nome_regiao AS regiao,
  h.taxa_alfabetizacao_anterior,
  h.media_portugues_anterior,
  h.percentual_participacao_anterior,
  h.total_alunos_avaliados_anterior,
  pop.populacao AS populacao_anterior,
  SAFE_DIVIDE(pib.pib * 1000, pop.populacao) AS pib_per_capita_anterior,
  m.meta_alfabetizacao_2025,
  a.peso_aluno,
  a.alfabetizado_bool,
  -- Mantida exclusivamente para o experimento diagnostico de vazamento.
  -- src/preprocessing/schema.py impede seu uso no modelo principal.
  a.proficiencia
FROM alunos_2024 a
LEFT JOIN contexto_educacional_2023 h USING (id_municipio)
LEFT JOIN metas_2025 m USING (id_municipio)
LEFT JOIN populacao_2023 pop USING (id_municipio)
LEFT JOIN pib_2023 pib USING (id_municipio)
LEFT JOIN diretorio d USING (id_municipio);

-- Auditoria minima esperada: uma linha por registro, duas classes e atributos
-- do contexto com cobertura suficiente para imputacao.
SELECT
  COUNT(*) AS total_linhas,
  COUNT(DISTINCT id_municipio) AS total_municipios,
  COUNTIF(alfabetizado_bool) AS alfabetizados,
  COUNTIF(NOT alfabetizado_bool) AS nao_alfabetizados,
  ROUND(100 * COUNTIF(taxa_alfabetizacao_anterior IS NULL) / COUNT(*), 2)
    AS percentual_sem_historico_2023,
  ROUND(100 * COUNTIF(pib_per_capita_anterior IS NULL) / COUNT(*), 2)
    AS percentual_sem_pib_2023
FROM `tech-alfabetizacao-vdemarchi.gold.ml_alfabetizacao_fase3`;

