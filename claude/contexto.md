# IH-214 — Contexto e pedido de revisão ao Claude

## Onde o Codex deixou o projeto

O Claude concluiu a verificação D4.2 e preparou o modelo do resumo AERO2027. O Codex retomou do commit `034cb6d` e trabalhou até `13ffc2b`. O próximo bloco do manuscrito é a D5.

| Etapa | Trabalho entregue | Onde conferir |
|---|---|---|
| D4.3 | Piloto de precisão com 30 dias, sementes 10001–10030. O mínimo de 30 réplicas prevaleceu na definição da rodada final. | `data/d4/plano_piloto_d4_3.md`, `data/d4/resultado_piloto_d4_3.md` |
| D4.4 | 30 dias independentes do piloto, sementes 20001–20030, com 48 células por dia e 1.440 execuções arquivadas. | `data/d4/dias_d4_4/`, `data/d4/resultados_d4_4.csv` |
| D4.5 | 1.632 resumos de célula e 82 contrastes pareados, com 30 pares válidos por contraste. | `scripts/d4_analise.py`, `data/d4/resumo_celulas_d4_5.csv`, `data/d4/contrastes_d4_5.csv`, `data/d4/sintese_d4_5.md` |
| D4.6 | Integração ao manuscrito, figura de vazão, resumo AERO2027 e ZIP atualizado. | `sections/results.tex`, `aero2027/resumo_aero2027.tex`, `deliverables/IH214_overleaf_estado_atual.zip` |

Na última verificação, passaram 70 testes no ambiente Conda `ih214`. O manuscrito compilou com 10 páginas e o resumo com uma página A4. O resumo ainda tem campos de autoria, endereço, e-mail e biografia em vermelho. A transposição final para Word está pendente.

O Codex conservou a interpretação de execução agendada da D4.2 para o piloto e para as rodadas finais. A especificação anterior marcava essa interpretação para revisão do autor. O Codex também escolheu, antes do piloto, semilarguras-alvo de 0,25 decolagem/h e 30 s de espera média, com mínimo de 30 réplicas finais.

## Claude, revise estes pontos em ordem de prioridade

1. **Regra de agenda e interpretação do efeito.** Confira a D4.1 v2.1 contra `scripts/d4_agenda.py` e `scripts/d4_sim.py`. Verifique o horário mínimo de saída, a prioridade entre compromissos prontos e a execução após atrasos. Avalie quanto a diferença agenda − FCFS de −0,129 decolagem/h na referência depende da regra testada. Examine se os dados e traços distinguem espera pelo horário mínimo de espera por rota ou TLOF e se o texto atribui causalidade além do contraste observado. Indique a decisão que ainda cabe ao autor.
2. **Pareamento, classificação e precisão.** Verifique correspondência por semente e dia, direção dos contrastes, cálculo do IC t e rótulos de análise principal. Confira se o analisador classifica como principais contrastes de famílias que o protocolo chama de exploratórias. Verifique se o texto descreve corretamente o afinamento dos pedidos entre níveis de demanda e o deslocamento das chegadas quando muda a recarga. Examine a interpretação dos intervalos degenerados na inspeção.
3. **Denominadores e seleção.** Reproduza os números que entraram no manuscrito e no resumo. Confira médias de proporções por réplica versus proporções agregadas, especialmente a fração de voos retidos, e a população das esperas. Verifique o balanço completo dos pedidos, incluindo grupos vazios, a censura, a definição de início de embarque e a diferença entre retenção pelo grupo e ocupação do stand após prontidão para partir.
4. **Mecanismos e completude da D4.** Confira se a evidência sustenta o ganho do quinto stand, o deslocamento da espera para a inspeção e a leitura da informação perfeita com e sem recarga. Compare o que foi entregue aos critérios de D4.5 e D4.6 em `deliverables/D4_plano.md`, em especial o traço de eventos previsto e a tabela que deve acompanhar a figura de demanda. Indique lacunas que exigem nova rodada, reanálise ou ajuste de redação.
5. **Resumo AERO2027.** Cruze os efeitos, ICs, unidades e condições com os CSVs. Confira estilo e ordem pelo modelo Word oficial e pelo `AGENTS.md`. Aponte o que falta para uma página no Word, quais metadados bibliográficos precisam de conferência e quais informações dependem do autor.

Registre o parecer em `claude/outputs/D4_REVISAO_CLAUDE.md`. Para cada achado, indique gravidade, arquivo e linha ou chave da célula, evidência reproduzível, consequência e correção proposta. Informe quais verificações executou. Trabalhe em modo de revisão, com escrita somente no arquivo do parecer.
