# Model Card - Risco de não alfabetização

## Identificação

- Nome: Modelo de risco de não alfabetização - Fase 3
- Versão: 1.0
- Status: treinado e avaliado na exportacao real de 2024
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

Separação 60/20/20 por município: 92.077 registros em treino, 35.869 em validação e 33.032 em teste, sem sobreposição territorial. A regressão logística com `C=0,3` foi selecionada por PR-AUC.

No teste, ROC-AUC = 0,661, PR-AUC = 0,542 e Brier = 0,225. O ponto equilibrado usa limiar 0,515, precisão de 53,5%, recall de 49,4% e taxa de alertas de 36,6%. O ponto de triagem ampla usa limiar 0,230, recall de 95,0% e taxa de alertas de 88,8%.

## Riscos

- viés de seleção associado à ausência na avaliação;
- proxy territorial de desigualdades históricas;
- menor estabilidade em municípios com poucos registros;
- ausência de variação individual: os atributos desta versão são municipais;
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
