# Dicionario da base analitica

| Variavel | Tipo | Papel | Origem / regra |
|---|---|---|---|
| `ano` | inteiro | referencia | 2024 no primeiro ciclo |
| `id_municipio` | texto | grupo e agregacao | codigo IBGE; nao e preditor |
| `rede_nome` | categoria | educacional | rede municipal no escopo principal |
| `codigo_uf` | categoria | territorial | dois primeiros digitos do codigo municipal |
| `sigla_uf` | categoria | exibicao | diretorio de municipios |
| `regiao` | categoria | territorial | diretorio de municipios |
| `taxa_alfabetizacao_anterior` | decimal | preditor | resultado municipal de 2023 |
| `media_portugues_anterior` | decimal | preditor | media municipal de 2023 |
| `percentual_participacao_anterior` | decimal | preditor | participacao municipal de 2023 |
| `total_alunos_avaliados_anterior` | inteiro | preditor | aptos do municipio em 2023 |
| `populacao_anterior` | inteiro | preditor | estimativa municipal IBGE de 2023 |
| `pib_per_capita_anterior` | decimal | preditor | PIB 2023 em mil reais x 1.000 / populacao |
| `meta_alfabetizacao_2025` | decimal | contexto | meta oficial conhecida; usada tambem no deficit |
| `peso_aluno` | decimal | auditoria | peso amostral; nao e preditor nesta versao |
| `alfabetizado_bool` | booleano | alvo original | classificacao oficial do estudante |
| `nao_alfabetizado` | binario | alvo do modelo | `1 - alfabetizado_bool` |
| `proficiencia` | decimal | vazamento | define o rotulo; proibida no modelo principal |

## Colunas deliberadamente excluidas

- Identificadores de aluno e escola: alta cardinalidade, privacidade e risco de memorizacao.
- Caderno, presenca e preenchimento: informacoes ligadas ao processo da avaliacao, pouco acionaveis antes da prova.
- Proficiencia e descricao/codigo de alfabetizado: revelam diretamente o alvo.
- Taxa, media e proporcoes de nivel de 2024: agregacoes do mesmo desfecho, portanto vazamento.

