# Registro de decisões analíticas

## DA-01 - Evento positivo orientado ao risco

- Decisão: `1 = não alfabetizado`.
- Motivo: torna recall e priorização coerentes com a política de apoio.
- Consequência: métricas e limiar devem sempre ser lidos para a classe de risco.

## DA-02 - Recorte da rede municipal

- Decisão: modelar estudantes municipais.
- Motivo: `gold.indicador_municipio` e as metas municipais da Fase 2 usam `rede_codigo = 3`.
- Consequência: conclusões não devem ser generalizadas automaticamente às redes estadual ou privada.

## DA-03 - Atributos defasados

- Decisão: contexto educacional, população e PIB de 2023 para o desfecho de 2024.
- Motivo: simular informação disponível antes da avaliação.
- Consequência: municípios sem histórico terão valores imputados e maior cautela interpretativa.

## DA-04 - Proficiência bloqueada

- Decisão: excluir proficiência e agregações de 2024 do modelo principal.
- Motivo: o corte de proficiência define o rótulo; sua inclusão é vazamento.
- Consequência: desempenho menor, porém aplicabilidade maior.

## DA-05 - Split por município

- Decisão: treino, validação e teste sem sobreposição municipal.
- Motivo: evitar memorização contextual e testar generalização territorial.
- Consequência: a tarefa é mais difícil e representa municípios não vistos.

## DA-06 - Seleção por PR-AUC e limiar por F2

- Decisão: PR-AUC escolhe o modelo; F2 escolhe o limiar na validação.
- Motivo: qualidade do ranking e prioridade de recall.
- Consequência: o limiar pode ser ajustado futuramente à capacidade operacional, sem retreinar.

## DA-07 - Importância não causal

- Decisão: usar importância por permutação e comunicar associação.
- Motivo: funciona com qualquer candidato e é calculada fora do treino.
- Consequência: variáveis correlacionadas podem dividir importância; não inferir política causal.

## DA-08 - Dados sintéticos somente para teste

- Decisão: isolar saídas sintéticas em `demo_outputs/` e marcar o relatório.
- Motivo: testar reprodutibilidade sem falsificar resultado acadêmico.
- Consequência: a entrega final precisa dos arquivos produzidos com a exportação real.

