# D3 — auditoria final da base teórica

**Data:** 20/11/2026. **Objeto:** `sections/theoretical_basis.tex`, à luz do protocolo `deliverables/D3_protocolo_escopo.md`. O arquivo `data/d3/extracao.md` guarda versões, páginas e limites das fontes; `sintese_mecanismos.md` articula os quatro eixos. O ranking ordenou a leitura e não foi usado como prova de pertinência ou efeito.

| Afirmação ou decisão da seção | Evidência rastreável | Resultado da auditoria |
|---|---|---|
| Unidade e fronteira da espera; (L=\lambda W) | Little 1961, pp. 383–387; D2 define entrada e saída da fila/estação | A identidade é apresentada para regime estável; a janela terminante da D2 exige observar pendências e recusas separadamente. |
| Bloqueio de TLOF por estacionamento | D001, preprint, PDF pp. 1–4 | Redação especifica que o TLOF fica impedido de aceitar nova chegada; não afirma ocupação física contínua durante toda a espera. |
| Contagem de recursos, vazão e capacidade prática são grandezas diferentes | D005, §2 e §5.3; D023, §§3.1 e 3.4; D026, pp. 3–4 e 9–10; D002 publicado, §3.3 | Quantidade de posições é entrada; movimento/h e limite de atraso são resultado/critério. A hipótese de pico estacionário de D002 não foi aplicada à D2. |
| Comparação prévia de políticas sob recursos fixos | D029, manuscrito integral disponibilizado pelo autor, pp. 3–8 e 13–16 | Inserida como evidência contrária à reivindicação ampla de novidade. Reordenação de partidas e admissão antecipada têm decisões diferentes; os números de D029 não foram transferidos. |
| Ligação prévia entre operações do lado ar e atraso do passageiro | D036, §§3.2–3.4; D023, §§2–4 | A seção reconhece o acoplamento anterior. O recorte da D2 exige fila por estação do terminal e prontidão do grupo. |
| Sincronização do gate, aeronave e grupo | LIT-008, ConOps §5.1.1; D021, PDF pp. 7 e 12; S4382766441, PDF pp. 2–3 e 10 | Condições e premissas de recarga da D2 aparecem como hipótese do modelo sintético, sem atribuir duração numérica a essas fontes. |
| LoS temporal, percurso e satisfação | Feldhoff, PDF pp. 8–10, Tabelas 5–6; D052, PDF pp. 7–9; D040/D044, textos abertos | A seção distingue denominador e marcos das esperas. Satisfação declarada permanece fora dos resultados simulados. |
| Capacidade, congestionamento e horário | Qin W7171717774, resumo e destaques do editor | Texto integral indisponível; a seção atribui explicitamente a afirmação ao resumo e evita detalhes de equação ou resultado. |
| Dois contrastes da D2 e interpretação dos resultados | `deliverables/D3_protocolo_escopo.md` e `data/scenario_protocol.md` | Mantidos separadamente: quantidade de recurso sob política fixa; regra de admissão/alocação sob recursos fixos. Recusas, pendências e composição do grupo acompanham partidas e espera. |

**Limites da cobertura:** D004 e Qin entram apenas no alcance de seus resumos; D012 e D045 ficam `texto_indisponivel`, sem conclusão temática extraída; estudos de programação em rede sem fila local verificada não sustentam afirmações sobre as estações do terminal. A revisão não estabelece que o contraste da D2 será superior; essa é pergunta experimental posterior.

**Verificação técnica:** compilação isolada com pdfLaTeX → BibTeX → duas passagens de pdfLaTeX: corpo da base teórica nas páginas 1–2 e referências na página 3, sem citações indefinidas. Em 21/11/2026, o manuscrito incremental passou a conter somente D2 e D3; compilou em 6 páginas, sem avisos de referência ou citação. `python3 -m pytest -q scripts/test_phase_a.py scripts/test_phase_b.py scripts/test_phase_c.py scripts/test_phase_d.py`: 18 testes e 5 subtestes passaram na auditoria original. Busca no manuscrito e na síntese não encontrou menção ao sítio excluído por decisão do autor.

**Estado:** passos 7–9 concluídos para a versão atual da D3. A calibração empírica e o experimento com réplicas pertencem à execução futura do modelo, não são resultados desta revisão.

**Correção de 21/11/2026 (segundo leitor, Claude).** A frase sobre critério de atraso citava a chave `preisHornung2022`, que corresponde a D036 (*Electronics*), enquanto esta auditoria atribuía a afirmação a D023 (*Applied Sciences*), ausente do `.bib`. Foram incluídas as entradas `preisHornung2022heuristic` (D023) e `zhang2023capacity` (D005), conferidas no texto integral da MDPI em 21/11/2026, e a frase passou a citá-las. A frase sobre posto adicional na inspeção foi marcada como hipótese da D2.
