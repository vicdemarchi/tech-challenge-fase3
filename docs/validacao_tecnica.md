# Evidências de validação técnica

Data da validação: 09/09/2026.

## Testes automatizados

Comando:

```bash
python -m unittest discover -s tests -v
```

Resultado: cinco testes aprovados.

- criação correta da classe positiva de risco;
- exclusão de proficiência e alvo dos preditores;
- falha explícita ao tentar incluir vazamento;
- ausência de município em mais de uma partição;
- treino dos cinco candidatos e seleção fora do baseline.

## Teste ponta a ponta

Comando:

```bash
python run_pipeline.py --input tests/fixtures/amostra_teste_sintetica.csv --demo --leakage-demo
```

Resultado: geração bem-sucedida de modelo, métricas, ranking, clusters, figuras e relatório automático. Todas as saídas foram isoladas em `demo_outputs/` e marcadas como sintéticas. Nenhum valor dessa execução foi utilizado no relatório acadêmico.

## Documento

O PDF técnico foi renderizado em oito páginas A4 e revisado visualmente após a conversão de cada página em PNG. Não foram observados cortes, sobreposições, tabelas fora da margem ou caracteres ausentes.

## Validação ainda necessária

Executar as três consultas SQL no projeto GCP, exportar a amostra real e repetir o pipeline. Essa etapa produzirá as métricas preditivas e os nomes dos municípios; sem ela, qualquer número de modelo seria fabricação.

