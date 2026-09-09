# Estratégia de versionamento e entrega no GitHub

## Histórico local preparado

O pacote inclui um repositório Git com commits separados por finalidade e merges das branches `feature/validacao-entrega` e `feature/resultados-reais`. Para a versão remota, crie um repositório vazio no GitHub e execute:

```bash
git remote add origin URL_DO_REPOSITORIO
git push -u origin main
```

Nunca execute `git add data/raw`, `git add data/processed` ou adicione credenciais. O `.gitignore` já protege esses caminhos.

## Fluxo recomendado para demonstrar branch e pull request

```bash
git checkout -b feature/resultados-modelo
python run_pipeline.py --input data/raw/ml_alfabetizacao.csv --leakage-demo
git add reports/resultados_automaticos.md images/ data/processed/
```

Como os resultados derivados estão ignorados por padrão, publique apenas tabelas agregadas e figuras revisadas. Se decidir versioná-las, use `git add -f` somente nos arquivos agregados autorizados, nunca em predições individuais.

Depois:

```bash
git commit -m "feat: adiciona resultados reais e interpretacao"
git push -u origin feature/resultados-modelo
```

No GitHub, abra um pull request para `main` com:

- tamanho e período da amostra;
- auditorias executadas;
- modelo selecionado e critério;
- métricas de validação e teste;
- confirmação de que não há microdados ou segredos;
- limitações identificadas.

## Padrão de mensagens

- `feat:` nova funcionalidade;
- `docs:` documentação;
- `test:` testes;
- `fix:` correção;
- `chore:` manutenção.
