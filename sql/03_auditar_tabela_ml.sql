-- Consultas de qualidade executadas antes de exportar ou treinar.

WITH base AS (
  SELECT *
  FROM `tech-alfabetizacao-vdemarchi.gold.ml_alfabetizacao_fase3`
)
SELECT
  'chave_nula' AS teste,
  COUNTIF(id_municipio IS NULL) AS falhas
FROM base
UNION ALL
SELECT
  'alvo_nulo',
  COUNTIF(alfabetizado_bool IS NULL)
FROM base
UNION ALL
SELECT
  'ano_diferente_2024',
  COUNTIF(ano != 2024)
FROM base
UNION ALL
SELECT
  'rede_diferente_municipal',
  COUNTIF(rede_nome != 'Municipal')
FROM base
UNION ALL
SELECT
  'proficiencia_incompativel_com_rotulo',
  COUNTIF(
    (proficiencia >= 743 AND NOT alfabetizado_bool)
    OR (proficiencia < 743 AND alfabetizado_bool)
  )
FROM base;

-- Cobertura de atributos por municipio, para diagnostico de missing.
SELECT
  COUNT(DISTINCT id_municipio) AS municipios,
  COUNT(DISTINCT IF(taxa_alfabetizacao_anterior IS NOT NULL, id_municipio, NULL))
    AS municipios_com_historico,
  COUNT(DISTINCT IF(populacao_anterior IS NOT NULL, id_municipio, NULL))
    AS municipios_com_populacao,
  COUNT(DISTINCT IF(pib_per_capita_anterior IS NOT NULL, id_municipio, NULL))
    AS municipios_com_pib,
  COUNT(DISTINCT IF(meta_alfabetizacao_2025 IS NOT NULL, id_municipio, NULL))
    AS municipios_com_meta_2025
FROM `tech-alfabetizacao-vdemarchi.gold.ml_alfabetizacao_fase3`;

