# Guia rápido para defender o trabalho

## Qual é o problema que o modelo resolve?

Ele estima risco antes do resultado corrente estar disponível e agrega esse risco para orientar quais municípios merecem diagnóstico primeiro. Não substitui avaliação pedagógica.

## Por que a classe positiva é "não alfabetizado"?

Porque a pergunta operacional é quem pode precisar de apoio. Assim, recall significa diretamente a proporção de casos de risco identificados.

## Por que não usar proficiência?

Porque o rótulo de alfabetização é definido pelo corte da proficiência. Usá-la seria fornecer a resposta ao modelo, causando vazamento e inviabilizando a aplicação preventiva.

## Por que usar variáveis de 2023 para prever 2024?

Para respeitar o tempo da decisão. Um atributo precisa existir no momento da previsão; indicadores do próprio 2024 só seriam conhecidos depois do desfecho.

## Por que separar por município?

Uma divisão aleatória por estudante deixaria alunos do mesmo município em treino e teste. O modelo poderia explorar características locais já vistas. O split por grupos mede generalização territorial com maior rigor.

## Por que PR-AUC como métrica principal?

Ela avalia a qualidade do ranking da classe positiva e é mais informativa que acurácia quando o evento de interesse é menos frequente. Acurácia alta pode ocorrer simplesmente ao prever a classe majoritária.

## Por que F2 para o limiar?

F2 dá mais peso ao recall. Em triagem para apoio, deixar um caso de risco sem alerta pode ser mais custoso que investigar um falso positivo. Como o maior F2 sinalizou 88,8% do teste, o projeto também fornece um limiar equilibrado de 0,515; a gestão escolhe o ponto conforme sua capacidade.

## O resultado do modelo foi bom?

Foi moderado e melhor que o acaso: ROC-AUC de 0,661 e PR-AUC de 0,542 contra prevalência de 0,397 no teste. Isso sustenta ranking territorial, mas não decisão individual automática. A honestidade dessa conclusão é uma força metodológica.

## Quais fatores e municípios se destacaram?

Código da UF, média de Português anterior e taxa de alfabetização anterior lideraram a importância. Com ao menos 30 registros no teste, Senhor do Bonfim, Paulo Afonso, Pilão Arcado, Santa Cruz e Remanso lideraram o risco previsto.

## Por que estudantes do mesmo município recebem o mesmo escore?

Os atributos seguros disponíveis são municipais. A linha é de estudante, mas não há variáveis individuais anteriores à prova. Por isso, esta versão deve ser defendida como triagem territorial; uma evolução incorporaria frequência, trajetória e contexto individual com governança adequada.

## O modelo mostra causas?

Não. O estudo é preditivo e observacional. Importância por permutação e coeficientes indicam associação útil para previsão. Uma política causal exigiria outro desenho, como experimento ou método quase-experimental.

## Como os dados ausentes foram tratados?

Numéricos recebem a mediana e categorias recebem a moda, sempre dentro do pipeline ajustado apenas no treino. Assim, estatísticas do teste não vazam para o modelo.

## Como foi controlado o sobreajuste?

Por separação treino/validação/teste, agrupamento por município, regularização/folhas mínimas, comparação do gap de PR-AUC e uso único do teste após seleção.

## Como usar o ranking com responsabilidade?

Combinar risco, incerteza, tamanho da amostra e contexto local; revisar por UF e região; usar o resultado para ampliar apoio, não para retirar direitos ou punir pessoas.

## Qual é o próximo passo técnico?

Quando o resultado de 2025 estiver disponível, executar validação temporal externa, recalibrar probabilidades e comparar estabilidade dos atributos.
