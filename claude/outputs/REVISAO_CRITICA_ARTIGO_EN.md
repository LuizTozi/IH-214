# Revisão crítica do artigo em inglês (Claude), 25/11/2026

**Objeto.** `aero2027/artigo_en/artigo_aero2027_en.tex`, commit `2743b34`.

**Skills.**
- `peer-review`: formato do parecer e auditoria das referências.
- `rigor-reviewer`: seis dimensões epistêmicas, D1 a D6.

A `rigor-reviewer` foi feita para um "Agent-Native Research Artifact" (diretório com `logic/claims.md`, `trace/exploration_tree.yaml`), que este projeto não tem. Apliquei as dimensões ao artigo e às evidências do repositório:
- as afirmações vêm do texto;
- os experimentos são as células da D4;
- o "rastro de exploração" é o histórico v2.1 → v2.2 registrado no Git e na D4.1.

O parecer está em Markdown, não em `level2_report.json`, pela mesma razão.

**Modo.** Somente revisão: nenhum arquivo do artigo foi alterado.

## Verificações executadas

| Verificação | Resultado |
|---|---|
| Auditoria de referências (Crossref e DataCite) | As 10 referências centrais conferem em título, autores, veículo, volume, páginas e ano: Little, Escribano Macias, Bennaceur, Guerreiro, Feldhoff, Halder e Gandhi, Vascik e Hansman, Preis e Hornung (Electronics), Preis (CEAS) e Feldhoff e Soares Roque (CEAS). Onat 2026 resolve na DataCite. Zhang (D005) e Preis e Hornung (D023) foram conferidos em texto integral em 21/11. |
| Números do texto contra os CSVs da v2.2 | Conferidos ao redigir; o polimento manteve números e citações idênticos. |
| Reprodução | 108 células da v2.2 reexecutadas coincidem com o arquivado. |
| Testes nos dados (abaixo) | Retenção por voo retido, multiplicidade e monotonicidade do ganho do stand. |

---

## Peer Review Report: *Coupling Terminal Station Queues And Stand Retention At Vertiports*

**Recomendação:** revisão menor para a forma de resumo e de pôster do AERO2027; revisão maior se o alvo for um periódico.

**Síntese.** O artigo responde com clareza a uma pergunta operacional (stand ou balcão; admissão antecipada ou FCFS). Usa simulação pareada verificada, indicadores principais declarados antes das rodadas e contabilidade honesta de populações, recusas e voos vazios. Há três problemas de calibragem que precisam de correção antes de qualquer envio:
- **Erro factual:** a retenção média é descrita como "por voo retido", mas é a média sobre todos os voos.
- **Generalização além dos dados:** o ganho do stand é dito crescente com o tempo de recarga.
- **Equivalência sem margem:** o contraste de política é apresentado como equivalência, sem margem declarada e sem correção para cinco contrastes principais.

A principal limitação de mérito é que os resultados do terminal dependem de durações estipuladas e determinísticas, sem análise de sensibilidade.

**Notas (1–5):** Novidade 3 | Rigor 3 | Impacto 3 | Clareza 4.

### Pontos maiores

1. **Retenção média descrita de forma errada (erro factual).**
   - **Trecho:** "*passengers were retained by their group, for 18.1~s on average; in B2, 2.3\% and 2.1~s*" (linha 436). Em `d4_sim.py`, `mean_await_s` é a média sobre **todos** os voos com passageiros, inclusive os de retenção zero.
   - **Média por voo retido:**

     | Configuração | FCFS | Agenda |
     |---|---|---|
     | Base | 196,5 s (92 voos) | 167,7 s (78 voos) |
     | B2 | 88,3 s (24 voos) | 94,3 s (18 voos) |

   - **Correção:** escrever "a mean retention of 18.1 s over all departures with passengers (196.5 s per retained flight)", ou relatar a média condicional ao lado. O mesmo erro está em `sections/results.tex`, herdado da versão anterior, e deve ser corrigido nas duas línguas.

2. **O ganho do stand não cresce com o tempo de recarga.**
   - **Trechos:** "*the stand pays off as demand and charging time grow*" (resumo, l. 82); "*Its value rises with demand and with charging time*" (l. 481); "*its value grew with demand and charging time*" (l. 516).
   - **Dados (Tabela 4):** 0,025 sem recarga, 0,487 com 30 min e 0,458 com 60 min. Os ICs de 30 e 60 min se sobrepõem, e a estimativa de 60 min é menor.
   - **Correção:** dizer que o ganho cresce com a demanda e é desprezível sem recarga, ficando entre 0,46 e 0,49 decolagem/h com 30 ou 60 min.

3. **Contraste de política apresentado como equivalência, sem margem nem correção para comparações múltiplas.**
   - **Trechos:** "*Advance admission matched FCFS in throughput*" (l. 519); "*delivered nearly the same throughput*" (l. 490).
   - **Dados:** o IC 95% (−0,066; −0,001) exclui zero por pouco. Com Bonferroni para os cinco contrastes principais (99%, t₀,₉₉₅;₂₉ = 2,756), passa a (−0,077; 0,010) e inclui zero.

     | Contraste | IC 95% | Bonferroni 99% | Resultado |
     |---|---|---|---|
     | Agenda − FCFS, Base | (−0,066; −0,001) | (−0,077; 0,010) | passa a incluir zero |
     | Base − S4, FCFS | (0,439; 0,536) | (0,423; 0,552) | robusto |
     | B2 − Base, FCFS (balcão) | (−158,4; −124,7) | (−164,2; −118,8) | robusto |

     "Matched" é uma alegação de equivalência que exige uma margem declarada antes da análise. A skill `scientific-writing` também proíbe converter um resultado não significativo em equivalência.
   - **Correção:**
     - Relatar a diferença como "a small negative difference (−0.033 departures/h, 0.8%), whose 95% CI excludes zero but whose multiplicity-adjusted interval does not".
     - Trocar "matched" por "differed by less than 1%".
     - Se o autor quiser afirmar equivalência, declarar uma margem operacional com justificativa. A semilargura-alvo de 0,25 do piloto foi critério de precisão, não margem de equivalência.

4. **Mudanças posteriores aos primeiros resultados não aparecem no Método.**
   - **Trecho:** "*Before the runs, we fixed one primary indicator per contrast*" (l. 292). Mas a definição do indicador mudou (decolagens → decolagens com passageiros) e a regra de execução da agenda também, ambas **depois** das rodadas da v2.1.
   - **Onde aparece:** a mudança da regra só surge na Discussão ("*In an earlier version of this experiment*"); a do indicador não aparece.
   - **Por que pesa:** mudanças pós-resultado são "caminhos que se bifurcam" e precisam ser declaradas onde o leitor avalia o desenho. A justificativa existe (LIT-008 §5.2.1.2; VAR-016 já definia voos com passageiros), e as duas versões estão arquivadas (`5decc6f`, `cf8ee2c`).
   - **Correção:** um parágrafo "Deviations from the initial plan" no Método, com motivo, data, células afetadas e o resultado da v2.1 (−0,129).

5. **Os resultados do terminal dependem de durações estipuladas e determinísticas, sem sensibilidade.**
   - **Trecho:** "*Check-in; security (deterministic) & 180 s; 90 s & author*" (Tabela 1).
   - **O que depende disso:**
     - o efeito do segundo balcão (−141,5 s; conformidade de 68% para 99%);
     - o deslocamento para a inspeção;
     - a ausência estrutural de fila na inspeção.
   - **Por que pesa:** com serviço constante, a fila do balcão é uma fila D com chegadas uniformes. Variabilidade de serviço tende a aumentar a espera e a cauda, e o efeito do segundo balcão pode mudar de magnitude. O texto declara o limite, mas um leitor de engenharia vai perguntar pela robustez.
   - **Correção:**
     - Pelo menos uma família de sensibilidade com serviço variável no balcão e na inspeção. Hoje, os parâmetros dessa variabilidade não têm fonte no cadastro e teriam de ser marcados como **supostos**.
     - Ou restringir explicitamente as conclusões do terminal ao serviço determinístico.

6. **"A maior parte da espera foi para a sala" compara populações diferentes.**
   - **Trecho:** "*most of the waiting saved at the counter moved to the lounge*". O −141,5 s é a média sobre visitas ao balcão (todos os presentes); o +124,7 s é a média sobre embarcados.
   - **Correção:**
     - Calcular, para os mesmos passageiros embarcados, a espera no balcão e a espera após a inspeção.
     - Ou arquivar a média da chegada ao embarque (VAR-012) entre embarcados, que mostra diretamente se o tempo total ficou constante.
     - Até lá, escrever "post-security waiting rose by 124.7 s while counter waiting fell by 141.5 s".

### Pontos menores

1. **Duas escolhas do autor sem sensibilidade:** a janela de 300 s (PAR-055) e o deslocamento da partida programada de 900 s (PAR-056). Elas controlam recusas e desvios, e portanto o efeito do stand. Uma frase no Método deveria registrar que não foram variadas.
2. **Posicionamento na literatura:** o projeto tem na matriz da D1, sem discussão no artigo:
   - Rimjha e Trani (2021), *Factors Affecting Vertiport Capacity*;
   - Kotwicz Herniczek et al. (2024), *Fleet and Vertiport Sizing*;
   - Park et al. (2022), *Vertiport Performance Analysis*;
   - Wille (2026), capacidade do lado ar por simulação de eventos discretos;
   - Schweiger, Knabe e Korn (2022).

   Convém conferir se algum acopla terminal e lado ar antes de afirmar a lacuna. Não avaliei o conteúdo deles nesta revisão.
3. **Não há validação externa.** O texto declara isso. Como verificação de plausibilidade, seria útil comparar o ciclo do stand com fontes que relatam turnaround, sem transferir valores.
4. **Referências:**
   - "arXiv preprint arXiv:2408.01152v3" repete "arXiv";
   - o Onat 2026 cita a versão "v1";
   - "AIAA AVIATION FORUM AND ASCEND 2025" está em maiúsculas, como no `.bib`.

   Padronizar no `.bib`.
5. **Grafia e símbolos:**
   - mistura de grafia britânica e americana ("synchronised" ao lado de "utilization" nos rótulos); escolher uma;
   - na Tabela 3, o sinal "---" na coluna de política aparece como traço longo; preferir "n/a" ou "both".
6. **Resumo:** "*Advance admission stayed within 0.033 departures/h of FCFS (0.001--0.066 fewer)*" está correto, mas deve acompanhar a correção do ponto maior 3.

**Justificativa da recomendação.** O desenho é sólido para o que se propõe:
- dias gerados antes da política, pareamento dentro da réplica e 30 réplicas com IC t;
- indicadores principais e exploratórios separados;
- verificação com casos calculados à mão;
- balanço completo dos pedidos e reprodução exata a partir das sementes.

A contribuição é real, mas restrita. Ela mede onde a espera ocorre e para onde vai, com os dois lados observados, e mostra sob quais condições cada recurso vale a pena. Os pontos 1 a 3 são correções de texto, rápidas e necessárias. Os pontos 4 e 6 pedem reorganização e um indicador adicional. O ponto 5 é a principal limitação de mérito para um periódico; para o AERO2027, basta delimitar as conclusões.

---

## Dimensões da `rigor-reviewer` (adaptadas)

| Dimensão | Nota | Forças | Fraquezas | Sugestões |
|---|---:|---|---|---|
| D1. Relevância da evidência | 4 | Cada afirmação principal tem contraste pareado com IC; mecanismos apoiados por balanço, ocupação e traço de eventos | "Most of the waiting moved to the lounge" mistura populações (P6) | Indicador emparelhado por passageiro |
| D2. Falseabilidade | 3 | Indicadores principais e sentido das diferenças fixados antes; resultado nulo da informação perfeita relatado | Sem margem de equivalência para a política; hipóteses da D3 formuladas sem critério numérico de refutação | Declarar margem; formular cada hipótese com o resultado que a refutaria |
| D3. Calibragem do escopo | 3 | Limites declarados; populações e denominadores explícitos; nenhuma alegação de ineditismo absoluto | Ganho do stand "cresce com a recarga" (P2); "matched FCFS" (P3); retenção por voo retido (P1) | Corrigir as três frases nas duas línguas |
| D4. Coerência do argumento | 4 | Decisão → lacuna → modelo → contrastes → implicação; a discussão responde às duas perguntas da introdução | Hipótese da inspeção (servidor adicional) saiu sem que a introdução de mecanismos registre isso | Uma frase na Seção 2 sobre o ramo retirado |
| D5. Integridade da exploração | 3 | Versão anterior relatada com o número (−0,129); variantes, decisões e motivos registrados no repositório | No artigo, as mudanças pós-resultado aparecem só na Discussão (P4) | Parágrafo de desvios no Método |
| D6. Rigor metodológico | 3 | Pareamento, 30 réplicas, IC t, separação principal/exploratória, reprodução exata, verificação | Sem correção para comparações múltiplas; serviços determinísticos sem sensibilidade (P5); janela e partida programada não variadas | Bonferroni ou equivalente como sensibilidade; família com serviço variável marcada como suposta |

**Média 3,33; nenhuma dimensão abaixo de 3.** Na escala da skill, é um "Weak Accept".

### Achados ordenados por gravidade

| ID | Dim. | Gravidade | Trecho literal | Ação |
|---|---|---|---|---|
| F01 | D3 | crítica | "for 18.1~s on average" | Corrigir para média sobre todos os voos e relatar 196,5 s por voo retido (FCFS, Base) |
| F02 | D3 | maior | "pays off as demand and charging time grow" | Retirar "and charging time" no resumo, na discussão e na conclusão |
| F03 | D2/D6 | maior | "Advance admission matched FCFS in throughput" | Trocar por diferença com IC e nota de multiplicidade |
| F04 | D5 | maior | "Before the runs, we fixed one primary indicator" | Declarar os desvios pós-resultado no Método |
| F05 | D6 | maior | "Check-in; security (deterministic)" | Sensibilidade com serviço variável (suposta) ou restrição explícita |
| F06 | D1 | maior | "most of the waiting saved at the" | Comparar as mesmas populações |
| F07 | D6 | menor | (ausência) | Registrar que a janela de 300 s e o deslocamento de 900 s não foram variados |
| F08 | D4 | menor | "This study targets the junction" | Conferir os cinco trabalhos da matriz D1 antes de afirmar a lacuna |
| F09 | — | menor | (referências) | Padronizar arXiv e caixa no `.bib` |
| F10 | — | sugestão | (tipografia) | Grafia única; "n/a" na Tabela 3 |

### Perguntas aos autores

1. Qual diferença de vazão seria operacionalmente irrelevante para um operador? Ela definiria a margem para a comparação entre políticas.
2. Há fonte para a variabilidade dos tempos de balcão e de inspeção, como a distribuição de Feldhoff ou do ADRM? Ela permitiria uma família de sensibilidade sem suposição.
3. A janela de 300 s representa um compromisso operacional citado em alguma fonte, ou é uma escolha de cenário?

---

## Prioridade

1. **Antes de qualquer envio, só texto:** F01, F02 e F03, no artigo e em `sections/results.tex`.
2. **Reorganização e um indicador:** F04 e F06. O F06 exige arquivar a média chegada–embarque, ou a decomposição por passageiro, e rodar de novo as 30 réplicas, o que leva menos de um minuto.
3. **Decisão do autor:** F05 (família com serviço variável e fonte dos parâmetros) e a margem de equivalência.
4. **Menores:** F07 a F10.
