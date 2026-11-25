# Revisão da D4, do resumo AERO2027 e da coerência com D2 e D3 (Claude), 25/11/2026

**Objeto.** Estado do repositório no commit `bb00635`, que é igual a `origin/main`. Os cinco pontos vêm de `claude/contexto.md`; o autor pediu também a revisão da D2 e da D3. Trabalhei em modo de revisão: nenhum arquivo do projeto foi alterado além deste parecer. As variantes contrafactuais rodaram em cópia temporária e importaram o código do repositório sem modificá-lo. O código delas está no Apêndice.

**Gravidade**
- **Alta:** muda uma conclusão do manuscrito ou do resumo, ou impede a submissão.
- **Média:** exige reanálise, novo indicador ou ajuste de texto com consequência na interpretação.
- **Baixa:** redação, rótulo ou rastreabilidade.

## Verificações executadas

| Verificação | Resultado |
|---|---|
| `git pull --ff-only` | Já atualizado. O local é igual a `origin/main` (`bb00635`), e os commits da D2 e da D3 (`0bcc7fe`, `978beff`) estão no histórico. |
| Testes, `cd scripts && python -m unittest` (Conda `ih214`) | 70 testes OK. |
| Reexecução de `d4_analise.py` sobre `resultados_d4_4.csv` | Os 1.632 resumos e os 82 contrastes não diferem dos arquivados (0 diferenças). A síntese é idêntica. |
| Reexecução de `d4_experimento.py`, sementes 20001–20003 | Das 144 células, nenhum campo diverge do CSV arquivado. O código das rodadas (`954995e`) é igual ao atual nos módulos d4. |
| Pareamento | 30 sementes, com um `day_id` por semente. Nenhuma semente do piloto se repete nas rodadas finais. |
| Balanço dos pedidos | `oferecidos = cancelados vazios + recusados + desviados + decolados + pendentes` fecha nas 1.440 linhas. |
| Números de `sections/results.tex` e do resumo | Todos coincidem com `resumo_celulas_d4_5.csv` e `contrastes_d4_5.csv`, com arredondamento correto. |
| IC t | Para gl = 29, t = 2,045 (correto). O sentido das subtrações confere com os rótulos. |
| Compilação | O manuscrito tem 10 páginas, sem citações indefinidas; a D3 ocupa as pp. 4–5 (até duas páginas). O resumo tem 1 página em LaTeX. |
| Variantes da regra de agenda (Apêndice) | Ver A1. |

---

## 1. Regra de agenda e interpretação do efeito

### A1 · Alta · Cerca de 70% do efeito agenda − FCFS vem da regra de execução, não da admissão antecipada

**Onde está a regra.**
- `scripts/d4_sim.py:217-218`: a partida da agenda usa `eligible_from=planned_exit_ms`, ou seja, a saída planejada funciona como horário mínimo.
- `scripts/d4_agenda.py:79`: o calendário nunca antecipa uma saída já planejada, por causa de `max(projected, planned_exit_ms, now)`.
- A saída planejada nasce da previsão mais tardia do grupo: quem ainda não chegou é previsto para chegar no fechamento do manifesto (`d4_agenda.py:63-64`).

**Evidência reproduzível.** Contraste agenda − FCFS na Base, 30 réplicas, mesmos dias:

| Execução da agenda | Referência (6/h, 30 min) | Demanda alta (8/h) | Sem recarga |
|---|---:|---:|---:|
| Regra verificada (arquivada) | −0,129 [−0,179; −0,079] | −0,142 [−0,189; −0,095] | −0,050 [−0,084; −0,016] |
| Sem horário mínimo de saída | −0,079 [−0,119; −0,039] | −0,092 [−0,134; −0,049] | −0,050 [−0,084; −0,016] |
| Sem horário mínimo e com calendário atualizado pela previsão | −0,037 [−0,070; −0,005] | −0,033 [−0,076; +0,009] | — |

Na agenda arquivada da referência, o bloqueio do stand após a prontidão para partir tem média de 75,3 s nos 985 voos que deixaram o stand:
- **74,9 s** são espera pelo horário mínimo, `max(0, saída planejada − pronta)`, em 620 voos;
- **0,4 s** são disputa de rota ou TLOF, em 9 voos.

A informação perfeita produz o mesmo efeito por outro caminho. Ela reduz o bloqueio em −75,6 s [−81,5; −69,8] e eleva a vazão em +0,092. Com ela, a agenda fica a −0,129 + 0,092 ≈ −0,037 decolagem/h do FCFS, o mesmo valor da variante com calendário atualizado.

**Os dados arquivados não distinguem as duas esperas.** O CSV guarda apenas `mean_stand_blocked_s`, que soma a espera pelo horário mínimo à espera por rota ou TLOF. O critério da D4.5 em `deliverables/D4_plano.md:15` manda acrescentar os eventos que façam essa distinção.

**Consequências**
- `results.tex:84-89` diz que "a reserva antecipada reduziu admissões, mas o horário mínimo também impediu algumas saídas antecipadas". Pela decomposição, o horário mínimo e o piso do calendário respondem pela maior parte do efeito; a parte atribuível à recusa pessimista é de cerca de −0,04 decolagem/h. Na demanda alta, o intervalo dessa parte inclui zero.
- O resumo diz que a admissão antecipada "did not outperform FCFS with the tested minimum-time commitments and forecasts". A ressalva está certa, mas o leitor entende que a política, e não a regra de execução, explica o déficit.
- O texto não atribui causalidade além do contraste observado: usa "consistente com". Falta quantificar a decomposição.

**Decisão do autor**, já pendente na D4.1 v2.1 (`deliverables/D4_1_cenarios.md:213`, "a revisar pelo autor"): qual execução representa a política agendada?
- (a) A saída planejada é horário mínimo, como na regra atual. Equivale a um compromisso rígido com o slot.
- (b) A aeronave pronta sai assim que houver rota e TLOF, e o plano serve apenas de prioridade.
- (c) Como (b), e o calendário também é atualizado pela previsão.

A escolha muda o sinal operacional da comparação: de "a agenda perde 3% da vazão" para "a agenda empata com o FCFS dentro do erro" (na demanda alta, em c).

**Correção proposta**
1. Registrar a decisão do autor na D4.1 (versão 2.2).
2. Arquivar, por voo, `planned_exit_s`, `ready_depart_s` e `stand_exit_s`, ou ao menos a decomposição do bloqueio.
3. Rodar as variantes (b) e (c) como sensibilidade declarada, com versão do código, nas 30 sementes da D4.4. Leva poucos minutos.
4. Reescrever `results.tex:84-89` e a frase do resumo com a decomposição. Os números das variantes deste parecer não podem entrar no texto antes dessa rodada versionada, pela regra do `AGENTS.md`.

---

## 2. Pareamento, classificação e precisão

### A2 · Alta · O contraste da inspeção (I2 − Base) é nulo por construção, não por observação

**Evidência**
- Nas 360 linhas I2 de `resultados_d4_4.csv` (todas as famílias, políticas e sementes), **todas as colunas são idênticas às da Base**, exceto a configuração.
- Nas 1.080 linhas com um balcão, a espera média na inspeção é sempre 0.

**Por que é zero.** O balcão (180 s, PAR-046) e a inspeção (90 s, PAR-047) são determinísticos (`d4_terminal.py`, `SERVICE_S`).
- Com um balcão FCFS, duas saídas consecutivas distam ≥ 180 s.
- Com a bagagem entre 30 e 60 s, as chegadas à inspeção distam ≥ 180 − 30 = 150 s, mais que os 90 s de serviço.
- Logo, nunca se forma fila na inspeção (nem na bagagem). O segundo posto nunca é usado, porque o servidor de menor índice está sempre livre.

**Consequências**
- O "IC 95% (0,0; 0,0)" não é um intervalo amostral, é uma identidade.
- `results.tex:126-128` chama o zero de "resultado observado no cenário".
- O resumo ("a second security post had no queue to remove") apresenta como achado uma consequência das durações sintéticas.
- O contraste I2 **não testa** a hipótese da D3 sobre o servidor adicional na inspeção.
- O piloto já mostrava DP pareado 0 (`resultado_piloto_d4_3.md`), e isso deveria ter sido examinado antes da D4.4.

**Correção proposta**
- Declarar no texto que o zero decorre de serviços determinísticos com balcão mais lento que a inspeção, e retirar o IC.
- No resumo, trocar por uma formulação condicional, ou omitir.
- Decisão do autor: manter I2 como verificação, ou introduzir variabilidade de serviço com fonte (o cadastro não a tem). Sem fonte, ela seria **suposta**.

### A3 · Média · O analisador rotula como principais 28 contrastes que o protocolo chama de exploratórios

**Evidência.** `scripts/d4_analise.py:195-205` atribui `primary` a `stands_*`, `counter_*` e `security_*` em **todas** as famílias regulares, e a `policy_Base` em todas. O protocolo diz outra coisa (`D4_1_cenarios.md:247-256`): o indicador principal é "estimado na família de referência", e as famílias de sensibilidade são exploratórias. Em `contrastes_d4_5.csv`, 4 famílias × 7 contrastes = 28 linhas trazem o rótulo `primary` indevidamente (por exemplo, `demanda_alta, policy_Base`).

**Consequência.** O texto acerta ("sensibilidades planejadas", `results.tex:142`), mas a tabela de máquina, citada como fonte quantitativa, diverge do protocolo.

**Correção.** Usar `primary` só quando `family == "referencia"`, e regenerar os CSVs.

### A4 · Baixa · Pareamento descrito de forma ampla demais

`results.tex:12-13` diz: "todas as células receberam os mesmos pedidos, manifestos, chegadas e durações". Isso vale dentro de uma família, não entre famílias:
- **Demanda:** as famílias de 4, 6 e 8/h são subconjuntos aninhados de um fluxo a 8/h, afinado por marca (`d4_dia.py:96-101`).
- **Recarga:** mudar a recarga desloca a STD (t + 900 + R) e, com ela, todas as chegadas (`chegada = STD − antecedência`) e o fechamento do manifesto.

O texto não descreve nem o afinamento aninhado nem esse deslocamento.

**Correção.** Uma frase sobre cada mecanismo, e "dentro de cada família" na frase do pareamento.

### A5 · Baixa · Precisão-alvo escolhida pelo Codex

A semilargura-alvo de 0,25 decolagem/h é quase o dobro do efeito de política observado (0,129). Não houve consequência, porque o mínimo de 30 réplicas deu 0,050. Mas o critério não teve justificativa operacional, e cabe ao autor registrá-lo ou revê-lo.

### A6 · Baixa · O texto da síntese está escrito à mão no código

`d4_analise.py:322-340` contém frases e números fixos ("0,129", "mais de 120 s", "cerca de 8 s", "2.529 atendimentos"). Uma reexecução com dados novos reproduziria o texto antigo.

**Correção.** Gerar esses números a partir dos índices, ou mover o texto para fora do script.

---

## 3. Denominadores e seleção

### A7 · Média · Voos sem passageiros entram na vazão e na cobertura

**Evidência.** Com recarga de 30 ou 60 min, o fechamento do manifesto (t + R) é sempre posterior à decisão em t. Um grupo totalmente ausente, portanto, nunca é cancelado antes da alocação (`d4_sim.py:144`) e decola vazio. Valores na Base de referência:

| Política | Decolagens vazias por réplica | Equivalente em decolagens/h |
|---|---:|---:|
| FCFS | 0,87 | 0,108 |
| Agenda | 0,83 | 0,104 |

Sem recarga, os grupos vazios são cancelados (1,37 por réplica) e não decolam.

**Consequências**
- A VAR-016 da D2 define a vazão como "**Passenger** eVTOL liftoffs", mas a D4 conta decolagens vazias.
- A cobertura trata como atendido um pedido sem nenhum passageiro.
- Os níveis absolutos de decolagens/h não são comparáveis entre a família sem recarga e as demais. Os contrastes dentro da família quase não mudam.

**Correção**
- Relatar decolagens/h com e sem voos vazios. Sem vazios, a Base de referência fica em 4,11 (FCFS) e 3,99 (agenda) decolagens/h, contra 4,22 e 4,09 com vazios.
- Ou alinhar a VAR-016 à regra da D4.1, que já prevê "decola sem passageiros". A decisão é do autor.

### A8 · Baixa · Média de proporções por réplica apresentada como proporção agregada

| Indicador | Texto | Base do texto | Proporção agregada |
|---|---|---|---|
| Cobertura (FCFS / agenda) | 77,7% e 75,4% "em 1.313 pedidos" | média de razões por réplica | 77,2% (1.013/1.313) e 74,8% (982/1.313) |
| Fração retida, Base (FCFS / agenda) | 9,2% "dos 987 voos" e 7,8% "de 957" | média de razões por réplica | 9,3% e 7,9% |

A Tabela 3 declara corretamente que a cobertura é "dentro de cada réplica"; a prosa mistura as duas leituras.

**Correção.** Escrever "média por réplica" ou usar a razão agregada.

### Verificado sem achado

- **Início do embarque.** É a entrada na aeronave, depois da caminhada e da porta (`d4_sim.py:208-209`), conforme a VAR-012 ("starts on entering aircraft", Preis e Hornung, Tab. A1).
- **Retenção pelo grupo** (`await_s`) e **bloqueio do stand após a prontidão para partir** (`stand_blocked_s`) são medidas disjuntas.
- **Prontidão da aeronave.** Ocorre sempre depois do fechamento do manifesto (pronta ≥ t + 180 s + R > t + R), de modo que a retenção não inclui a espera pelo fechamento.
- **Censura.** A população das esperas são as visitas com início observado, e a censura é contada à parte.

---

## 4. Mecanismos e completude da D4

### A9 · Média · O indicador de LoS da D2 não aparece nos resultados nem no resumo

A conformidade ao limite da IATA por estação (VAR-015) está calculada no CSV (`counter_within_limit_fraction`), mas `results.tex` e o resumo não a citam, embora "Level of Service" seja palavra-chave do resumo. Na referência (média por réplica, IC 95%):

| Configuração | FCFS | Agenda |
|---|---|---|
| Base | 67,7% (63,9–71,5) | 70,8% (67,1–74,5) |
| B2 | 99,2% (98,7–99,6) | 99,2% (98,7–99,6) |

O contraste de conformidade é exploratório pelo protocolo. Ainda assim, é a métrica operacional de LoS do projeto.

**Correção.** Relatar a conformidade como resultado explicativo, ao lado da espera média.

### A10 · Média · O P95 do tempo até o embarque quase só mede a antecedência de chegada

O `terminal_to_board_p95_s` fica em torno de 2.820 s em todas as configurações:

| Configuração | FCFS | Agenda |
|---|---:|---:|
| Base | 2.819 s | 2.833 s |
| B2 | 2.820 s | 2.833 s |

A diferença entre Base e B2 é de cerca de 1 s, porque a chegada é sorteada entre 15 e 60 min antes da STD. Com o desenho de chegadas da D4.1, a métrica de percurso da D2 é dominada pela antecedência programada.

**Correção.** Declarar essa limitação. Se o autor quiser, acrescentar um indicador do fim da inspeção ao início do embarque, que isola a espera depois do processamento; isso exige definição na D2.

### A11 · Média · Critérios da D4.5 e da D4.6 não cumpridos

Exigências de `deliverables/D4_plano.md`:

| Linha | Exigência | Estado |
|---|---|---|
| 15 (D4.5) | Sequência de eventos para examinar o gargalo | Ausente (ver A1) |
| 148 (D4.6, item 2) | Tabela que acompanhe a figura nas **mesmas** taxas de demanda, com recusas, pendências e espera no terminal | A Tabela 3 cobre só a família de referência |
| 148 (D4.6, item 2) | Traço de eventos que explique um bloqueio | Ausente |
| 149 (D4.6, item 3) | Confronto com D029 (Halder e Gandhi, 2025) | Ausente de `results.tex` |

D029 é central para a interpretação. Ali, com recursos fixos, o sequenciamento por regras superou o FCFS em voos concluídos; aqui, a agenda perdeu. A divergência se explica por regras distintas (reordenação de partidas contra admissão antecipada com horário mínimo), e o texto precisa dizer isso.

**Correção**
- Tabela por demanda (4, 6 e 8/h), com recusas, desvios, pendências e espera no balcão, a partir de `resumo_celulas_d4_5.csv`.
- Um traço de voo com espera pelo horário mínimo.
- Um parágrafo sobre D029.

### Mecanismos que a evidência sustenta

| Afirmação | Situação |
|---|---|
| Quinto stand: +0,50 decolagem/h nas duas políticas | **Sustentado.** Desvios sob FCFS passam de 11,27 para 6,77 por réplica e recusas sob agenda de 12,27 para 7,90; ocupação física de 60% contra 55%. O efeito vale para a topologia e as durações sintéticas. |
| Deslocamento da espera do balcão para a inspeção | **Sustentado, com ressalvas (A12).** A inspeção passa de 0 para 8,0 s (FCFS) e 7,8 s (agenda). |
| Informação perfeita: +0,092 com recarga, cerca de 0 sem recarga | **Sustentado, com ressalvas (A13).** |

### A12 · Baixa · O deslocamento também acontece na bagagem e é garantido pela construção

A espera na bagagem também surge em B2 (de 0 para 2,4 s sob FCFS e 2,5 s sob agenda), e o texto omite isso. Além disso, pelo argumento de A2, só com dois balcões pode haver fila depois do balcão. Que surja alguma espera a jusante em B2 é, portanto, consequência estrutural; o que o experimento mede é a magnitude.

### A13 · Baixa · O efeito da informação perfeita contraria a expectativa da D4.1, e o texto não diz isso

A D4.1 (`D4_1_cenarios.md:70`) esperava um valor da informação **maior** sem recarga; ocorreu o oposto. O mecanismo é o de A1: a informação perfeita elimina a espera pelo horário mínimo (bloqueio de −75,6 s com recarga e −0,7 s sem recarga). Sem recarga, a agenda quase não recusa (0,57 por réplica) nem bloqueia.

**Correção.** Registrar que a hipótese da D4.1 não se confirmou e indicar o mecanismo.

---

## 5. Resumo AERO2027

### R1 · Alta · Risco de não caber em uma página no Word

O `.tex` usa `\fontsize{12}{14}` com `\onehalfspacing`, o que dá cerca de 17,5 pt por linha. O espaçamento 1,5 do Word para Times de 12 pt dá cerca de 20,7 pt.

Estimativa grosseira, a confirmar na transposição:

| Item | Linhas |
|---|---:|
| Texto do abstract (243 palavras, 1.665 caracteres) | ≈ 21 |
| Biografia de 150 palavras | ≈ 11 |
| Título, autores, afiliações, keywords e referências | ≈ 16 |
| **Total** | **≈ 48** |

A capacidade é de cerca de 33 linhas (A4, margens de 2,54 cm, espaçamento 1,5). O PDF de 1 página do LaTeX é otimista; o texto e a biografia precisarão de cortes.

**Correção**
- No `.tex`, usar `\fontsize{12}{20.7}` sem `\onehalfspacing` (ou equivalente) para simular o Word.
- Cortar o abstract para cerca de 170 palavras e a biografia para o necessário.
- Validar no `.docx`.

### R2 · Média · O modelo oficial se contradiz

| Aspecto | Texto de instrução do modelo | Configuração do arquivo `.docx` |
|---|---|---|
| Página | "A4 with margins in normal and 1.5 spacing" | Carta (12240 × 15840 twips) |
| Espaçamento | 1,5 | Simples (`w:line="240"`) |

O mesmo texto pede "Please do not change the styles". O `AGENTS.md` segue o texto (A4 e 1,5).

**Decisão do autor:** seguir o texto, ajustando página e espaçamento, ou perguntar aos organizadores. Com o espaçamento simples do arquivo, o problema de R1 desaparece.

### R3 · Média · Afirmações do resumo afetadas pelos achados acima

| Afirmação do resumo | Achado | Situação |
|---|---|---|
| Política | A1 | A conclusão depende da regra de execução. |
| "Second security post had no queue to remove" | A2 | O zero é estrutural. |
| Palavra-chave "Level of Service" | A9 | Nenhum resultado de LoS é relatado. |
| Fechamento: "stand was the throughput intervention, counter the terminal-service intervention" | — | Sustentado. |
| Limite: "compare designs rather than predict a site" | — | Correto. |
| Estrutura do `AGENTS.md` (decisão → lacuna com fonte → método → resultados com IC → implicação → limite) | — | Respeitada. |

Os efeitos, ICs, unidades e condições citados no resumo coincidem com os CSVs.

### R4 · Baixa · Formato das referências e metadados

- **Volume em negrito.** No exemplo do modelo, o volume aparece em negrito ("23"). Em [3], o "11" deve ir em negrito.
- **Conferência sem páginas.** [1] e [2] são anais de congresso sem volume nem páginas; manter o DOI é razoável. As iniciais vêm de `references/references.bib`, que confere.
- **Coerência das referências.** As três sustentam o que o resumo afirma:
  - Guerreiro trata do agendamento do lado ar;
  - Feldhoff trata do terminal sem o lado ar (D4.1:180);
  - Preis e Hornung (2022, Electronics) relatam atraso agregado do passageiro (extração D3, D036).
- **Atenção a D029.** Halder e Gandhi já comparam FCFS e sequenciamento. O resumo não reivindica novidade de política, e isso deve se manter.

### R5 · Depende do autor

- Coautores e orientador.
- Endereço da afiliação e e-mail do autor correspondente.
- Biografia de até 150 palavras.
- Confirmação do apresentador (sublinhado).
- Decisões de A1, A2, A7 e R2.

---

## D2 · Coerência com a implementação da D4

| # | Gravidade | Achado | Correção |
|---|---|---|---|
| D2-1 | Média | VAR-016 ("Passenger eVTOL liftoffs") contra as decolagens vazias contadas na D4 (A7). | Alinhar a definição ou separar o indicador. |
| D2-2 | Média | VAR-015 (conformidade de LoS) e VAR-012 (tempo até o embarque) foram calculadas, mas uma não é relatada (A9) e a outra é dominada pela antecedência de chegada (A10). | Relatar a VAR-015 e anotar o alcance da VAR-012 sob as chegadas da D4.1. |
| D2-3 | Baixa | VAR-018 e o protocolo de cenários tratam a agenda como admissão antecipada, mas não registram a regra de execução (horário mínimo, piso do calendário), que decide o efeito (A1). | Registrar a regra escolhida pelo autor na VAR-039 (parâmetros de coordenação). |
| ✓ | — | VAR-012 (início do embarque), PAR-026 (180 s no balcão e na inspeção; bagagem sem limite), um TLOF e expansões tratadas como cenários posteriores. | Coerentes com a D4. |

## D3 · Base teórica e síntese

| # | Gravidade | Achado | Correção |
|---|---|---|---|
| D3-1 | Média | `sintese_mecanismos.md` foi atualizado pela última vez após a D4.1 (23/11) e ainda trata como hipóteses o deslocamento da espera e a retenção do stand. O plano (`D4_plano.md:156`) pede revisar as implicações para a D3 ao fechar cada fase. | Acrescentar uma nota "Repercussão da D4.5": deslocamento observado em B2 (A12); inspeção não testável (A2); política dependente da regra de execução (A1); divergência em relação a D029 (A11). |
| D3-2 | Baixa | `theoretical_basis.tex` apresenta corretamente como hipótese o servidor adicional "no balcão ou na inspeção". O ramo da inspeção não pôde ser testado (A2), e a seção de resultados deve dizer isso, em vez de chamar o segundo posto de "redundante". | Ajuste em `results.tex`, não na D3. |
| D3-3 | Baixa | A frase sobre Feldhoff ("dois balcões reduzem a espera no balcão… atraso gerado na estação anterior", p. 10), acrescentada na D4.1, **não foi reverificada nesta sessão**: o PDF não está no repositório. | Conferir em Feldhoff 2022, p. 10. |
| ✓ | — | Correções da revisão anterior preservadas: citação do critério de atraso (D005 e D023) e marcação de hipótese. A D3 cabe em duas páginas. As citações resolvem. | — |

---

## Prioridade sugerida

1. **Decisões do autor:** A1 (regra de execução da agenda), A2 (I2 como verificação ou serviço estocástico), A7 (voos vazios) e R2 (A4 e 1,5 ou o arquivo do modelo).
2. **Reanálise sem nova simulação:** rótulos de A3, LoS de A9 e tabela por demanda de A11.
3. **Rodada de sensibilidade versionada** para A1 e, se o autor decidir, nova família para A2.
4. **Texto:** `results.tex` (A1, A2, A4, A8, A11–A13), resumo (R1, R3, R4) e D3-1.

---

## Apêndice · Código das variantes (reprodutível)

Rodado no ambiente `ih214`, na raiz do repositório, com o código e os dias arquivados:

```
python -I variantes.py scripts data/d4/dias_d4_4 referencia
python -I variante_calendario.py scripts data/d4/dias_d4_4 referencia
```

Núcleo das variantes. A substituição vale só durante a execução; nada é gravado no repositório.

```python
import d4_sim, d4_agenda
ORIG_REQ, ORIG_FE = d4_sim.Airside._request, d4_agenda.forecast_exit

def req_sem_minimo(self, kind, fid, key, eligible_from=0, stand=None):
    if kind == "dep" and self.policy == "agenda":
        eligible_from = 0            # variante (b): plano só como prioridade
    return ORIG_REQ(self, kind, fid, key, eligible_from, stand)

def fe_atualizada(airside, fid, entry_or_tau, now, ready_now):
    f = airside.flights[fid]; saved = f["planned_exit_ms"]; f["planned_exit_ms"] = None
    try:                             # variante (c): calendário sem o piso da saída planejada
        return ORIG_FE(airside, fid, entry_or_tau, now, ready_now)
    finally:
        f["planned_exit_ms"] = saved

# Decomposição do bloqueio na regra original, por voo que saiu do stand:
#   espera pelo horário mínimo = max(0, planned_exit_s - ready_depart_s)
#   disputa de rota ou TLOF    = (stand_exit_s - ready_depart_s) - espera pelo horário mínimo
```

O contraste é calculado contra `run_cell(..., "fcfs")` no mesmo dia e família, com IC t de 95% e gl = 29, como em `d4_analise.py`.
