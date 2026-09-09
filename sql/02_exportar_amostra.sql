-- Amostra deterministica aproximada de 10% para treinamento local.
-- A prevalencia original e preservada; nao ha balanceamento artificial.
-- Se o arquivo ficar muito grande, troque 10 por 20 (aprox. 5%).

SELECT
  ano,
  id_municipio,
  rede_nome,
  codigo_uf,
  sigla_uf,
  regiao,
  taxa_alfabetizacao_anterior,
  media_portugues_anterior,
  percentual_participacao_anterior,
  total_alunos_avaliados_anterior,
  populacao_anterior,
  pib_per_capita_anterior,
  meta_alfabetizacao_2025,
  peso_aluno,
  alfabetizado_bool,
  proficiencia
FROM `tech-alfabetizacao-vdemarchi.gold.ml_alfabetizacao_fase3`
WHERE MOD(id_registro_hash, 10) = 0;
