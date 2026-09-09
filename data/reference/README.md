# Evidencias agregadas herdadas da Fase 2

Estes arquivos pequenos reproduzem exclusivamente resultados de auditoria ja obtidos no BigQuery da Fase 2. Eles permitem documentar a base e gerar o panorama inicial sem publicar microdados.

- `fase2_brasil.csv`: resultados nacionais de 2023 e 2024.
- `metas_brasil.csv`: trajetoria nacional de metas presente na fonte da Fase 2.
- `auditoria_fase2.csv`: volumes e controles das camadas Silver, Gold e Quality.

Proveniencia: saidas das consultas `perfil_bronze.sql`, `indicador_municipio.sql`, `evolucao_alfabetizacao.sql` e `resumo_validacao_final.sql` do repositorio da Fase 2, executadas no projeto `tech-alfabetizacao-vdemarchi`.

Esses dados nao sao metricas do modelo de Machine Learning. As metricas preditivas so podem ser geradas apos a execucao com `data/raw/ml_alfabetizacao.csv`.

