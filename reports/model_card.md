# Model Card - Risco de não alfabetização

## Identificação

- Nome: Modelo de risco de não alfabetização - Fase 3
- Versão: 1.0
- Status: pipeline validado; estimador final depende da execução com dados reais
- Classe positiva: estudante não alfabetizado
- Unidade de inferência: estudante da rede municipal
- Unidade de decisão recomendada: município

## Uso pretendido

Priorizar municípios para diagnóstico pedagógico e oferta de apoio. O escore deve ser combinado com cobertura, tamanho amostral, conhecimento local e análise humana.

## Usos não permitidos

- reprovar, promover ou rotular individualmente um estudante;
- reduzir ou bloquear recursos;
- avaliar desempenho de professor ou escola isoladamente;
- inferir causa a partir da importância de atributos;
- publicar identificadores ou probabilidades individuais.

## Dados

Desfecho de 2024 e contexto educacional, territorial e socioeconômico de 2023, além da meta conhecida para 2025. A amostra de exportação é determinística e preserva a prevalência natural.

## Avaliação

Separação 60/20/20 por município. Seleção por PR-AUC na validação, limiar por F2 e avaliação única no teste. Métricas complementares: ROC-AUC, recall, precisão, balanced accuracy e Brier score.

## Riscos

- viés de seleção associado à ausência na avaliação;
- proxy territorial de desigualdades históricas;
- menor estabilidade em municípios com poucos registros;
- drift entre edições;
- interpretação causal indevida.

## Salvaguardas

- bloqueio automatizado de proficiência e agregações do próprio desfecho;
- split por município;
- intervalos de incerteza no ranking;
- revisão humana;
- auditoria periódica por região e UF;
- revalidação temporal assim que 2025 estiver disponível.

## Monitoramento recomendado

Registrar por versão: período dos dados, cobertura, prevalência, modelo, limiar, PR-AUC, recall, Brier, taxa de alertas, diferenças por UF/região e distribuição dos atributos. Recalibrar quando houver degradação relevante ou mudança na avaliação.

