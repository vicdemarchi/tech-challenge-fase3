# Evidências de validação técnica

Data da validação: 09/09/2026.

## Testes automatizados

Comando:

```bash
python -m unittest discover -s tests -v
```

Resultado: sete testes aprovados.

- criação correta da classe positiva de risco;
- exclusão de proficiência e alvo dos preditores;
- falha explícita ao tentar incluir vazamento;
- ausência de município em mais de uma partição;
- treino dos cinco candidatos e seleção fora do baseline.
- seleção reproduzível do limiar de acurácia balanceada e consistência da matriz de confusão.
- correção automática da unidade conhecida do PIB per capita.

## Teste ponta a ponta

Comando:

```bash
python run_pipeline.py --input data/raw/ml_alfabetizacao.csv --leakage-demo
```

Resultado: geração bem-sucedida de modelo, métricas, dois pontos de operação, ranking completo, ranking com amostra mínima, clusters, figuras e relatório automático. A entrada real contém 160.978 linhas e 5.350 municípios; o SHA-256 foi registrado nos metadados.

O teste final contém 33.032 registros de 1.070 municípios nunca vistos no treino. A regressão logística com `C=0,3` obteve ROC-AUC de 0,661, PR-AUC de 0,542 e Brier de 0,225. O diagnóstico deliberado com proficiência obteve métricas perfeitas e confirmou o vazamento que o contrato bloqueia.

## Documento

O PDF técnico foi renderizado em A4 e revisado visualmente após a conversão de cada página em PNG. Não foram observados cortes, sobreposições, tabelas fora da margem ou caracteres ausentes.

## Validação manual restante

Gravar o vídeo executivo e publicar o repositório por uma conta GitHub escolhida pela integrante.
