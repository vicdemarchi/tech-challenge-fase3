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

## DA-06 - Seleção por PR-AUC e dois pontos de operação

- Decisão: PR-AUC escolhe o modelo; F2 define a triagem ampla e acurácia balanceada define o ponto recomendado.
- Motivo: separar a qualidade do ranking da capacidade operacional de atendimento.
- Consequência: o limiar de 0,230 maximiza sensibilidade, mas sinaliza 88,8% do teste; o limiar de 0,515 oferece uso mais seletivo.

## DA-07 - Importância não causal

- Decisão: usar importância por permutação e comunicar associação.
- Motivo: funciona com qualquer candidato e é calculada fora do treino.
- Consequência: variáveis correlacionadas podem dividir importância; não inferir política causal.

## DA-08 - Dados sintéticos somente para teste

- Decisão: isolar saídas sintéticas em `demo_outputs/` e marcar o relatório.
- Motivo: testar reprodutibilidade sem falsificar resultado acadêmico.
- Consequência: a entrega final usa somente os arquivos produzidos com a exportação real.

## DA-09 - Correção da unidade do PIB per capita

- Decisão: remover a multiplicação por mil do SQL e normalizar exportações antigas quando a mediana superar R$ 1 milhão.
- Motivo: o valor municipal de PIB já está na unidade necessária para a divisão pela população.
- Consequência: a correção aplicada ao arquivo desta entrega ficou registrada nos metadados.

## DA-10 - Ranking municipal com amostra mínima

- Decisão: manter o ranking completo e publicar como prioritários apenas municípios com 30 ou mais registros no teste.
- Motivo: reduzir destaque indevido a probabilidades baseadas em amostras muito pequenas.
- Consequência: 215 dos 1.070 municípios de teste compõem a lista principal.
