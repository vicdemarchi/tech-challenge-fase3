# Checklist final de entrega

## Concluído no pacote

- [x] Estrutura de repositório organizada.
- [x] SQL de criação, auditoria e exportação da base ML.
- [x] Enriquecimento com população e PIB municipal do IBGE.
- [x] Pipeline com imputação, escala e encoding.
- [x] Bloqueio automatizado de vazamento.
- [x] Treino, validação e teste sem sobreposição de município.
- [x] Baseline e múltiplos modelos/hiperparâmetros.
- [x] Métricas adequadas à classe de risco.
- [x] Importância por permutação.
- [x] Ranking e clusterização municipal.
- [x] Testes unitários.
- [x] README, relatório, model card, roteiro e guia de defesa.
- [x] Evidências agregadas reais da Fase 2.

## Necessário antes da submissão

- [ ] Preencher nomes, RM e data na capa.
- [ ] Executar `sql/01_criar_tabela_ml.sql` no BigQuery.
- [ ] Confirmar zero falhas em `sql/03_auditar_tabela_ml.sql`.
- [ ] Exportar `ml_alfabetizacao.csv` e executar o pipeline real.
- [ ] Substituir as tabelas "a gerar" no relatório pelas métricas reais.
- [ ] Inserir os gráficos reais de avaliação, importância e ranking.
- [ ] Atualizar o PDF do relatório.
- [ ] Gravar o vídeo com duração máxima de cinco minutos.
- [ ] Criar o repositório remoto, branch e pull request.
- [ ] Confirmar que nenhum microdado, identificador ou segredo foi publicado.
- [ ] Abrir o ZIP final em outro diretório e repetir os testes.

