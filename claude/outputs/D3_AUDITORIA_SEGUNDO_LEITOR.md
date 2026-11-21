# D3 · Auditoria do segundo leitor (Claude)

**Data:** 19/11/2026 · **Revisor:** Claude (Opus 5.5) · **Escopo:** passo 9 do plano (auditar afirmações contra as fontes), aplicado ao rascunho existente.

**Arquivos auditados (somente leitura, nenhum foi alterado):**
`sections/theoretical_basis.tex`, `data/d3/extracao.md`, `data/d3/metodo_ranking.md`, `data/d3/ranking.csv`, `scripts/d3_ranking.py`.

**Fora do escopo, para não colidir com o Codex:** a elegibilidade em texto completo da fila `verificar_integra` (passo 5), `triagem.csv`, `chain_*.csv` e `acesso.csv`.

**Fontes usadas:** os PDFs em `/tmp/ih214_open_pdfs/` (baixados pelo Codex), os PDFs locais em `IT-214/Articles/Capacity and Turnaround of Vertiport/` e o PDF de Pagani et al. (2023) em `TESE/Methodi_Ordinatio/`. As páginas abaixo contam desde a primeira página do arquivo (página do PDF).

## 1. Methodi Ordinatio 2.0: equação e cálculo

| Item | Resultado | Evidência |
|---|---|---|
| Transcrição da equação 6 | **Correta.** `Δ·IF − λ·(ResearchYear − PubYear)/CitedHalfLife + Ω·Ci/((ResearchYear+1) − PubYear)`, com CitedHalfLife = 7,6 | Pagani et al. (2023), *Quality & Quantity* 57, pp. 4575–4576 |
| Cálculo do `ranking.csv` | **Reproduzido de forma independente:** 59 linhas, 3 ponderações, 0 divergências (tolerância 1e‑4); ordem decrescente conferida | Recalculado a partir das colunas `ano`, `citacoes` e `citescore_2021` |
| Fonte das citações | **Adaptação declarada.** A fonte prevê "Ci: total number of citations found in Google Scholar" (p. 4575); o Codex usou o OpenAlex | `metodo_ranking.md` declara a troca |
| Edição do indicador | **Adaptação declarada, mas com efeito grande.** A fonte prevê "last year CiteScore" (p. 4575); o Codex usou o CiteScore 2021 da cópia local do RankIn para uma pesquisa de 2026 | Ver 1.1 |
| Pesos (1,1,1) | Coerentes com a fonte, que deixa os pesos livres de 0 a 10 e exige que a escolha seja detalhada na metodologia (p. 4576) | — |

### 1.1 Ponto de atenção: 28 de 59 obras (47%) sem indicador

Sem CiteScore 2021: D001, D003, D013, D017, D019, D024, D026, D029, D031, D038, D040, D043, S4283220962, S7163509946, W1604925605, W3035491886, W3103847337, W3168813454, W3184579278, W3186938688, W4379792557, W4379877748, W4388561569, W4391302132, W4407410884, W4410115260, W4416923351, W7127406362.

Parte dessa ausência vem da edição de 2021, e não da falta de indexação. Exemplo: Wille et al. (D003) foi publicado no *Journal of the Air Transport Research Society*, que não tem valor na edição de 2021. Como Wille sustenta um parágrafo da seção, a ordenação atual subestima justamente obras centrais e recentes.

**Opções para o autor decidir** (não apliquei nenhuma):
(a) atualizar o indicador para a edição corrente do CiteScore (Scopus Sources), seguindo "last year CiteScore";
(b) estimar o CiteScore a partir do JCR pelas equações 2–5 da fonte (p. 4574), quando houver JCR;
(c) manter a edição de 2021 e declarar no texto o percentual sem indicador.

**Decisão do autor (19/11/2026): opção (a), edição mais atual.** A edição mais recente é o **CiteScore 2025**, publicado pela Elsevier em 3/6/2026, com janela de citações 2022–2025 ([anúncio da Elsevier](https://www.elsevier.com/products/scopus/resources/introducing-citescore-2025); [MDPI, 4/6/2026](https://www.mdpi.com/news/16779)). **Situação: valores ainda não coletados.** A página pública da fonte na Scopus (`scopus.com/sourceid/…`) redireciona para login em `id.elsevier.com`, e a extensão do Chrome não estava conectada. Nenhum valor foi preenchido a partir de páginas secundárias. Faltam 23 ISSNs a coletar na lista oficial de fontes da Scopus (Sources → CiteScore 2025); os 22 trabalhos AIAA sem ISSN continuam sem indicador.

**Atualização 20/11/2026: valores coletados.** A coleta foi feita na página de cada fonte da Scopus Preview (`scopus.com/sourceid/<id>`), com a sessão do autor no Chrome e o rótulo "CiteScore 2025". O identificador de cada fonte veio do ISSN na lista oficial `ext_list_Oct_2026.xlsx`, e o ISSN exibido em cada página foi conferido. Resultado em `claude/outputs/D3_CITESCORE_2025_COLETA_NAVEGADOR.csv`: 25 de 26 fontes com valor.
- Duas correspondem só por título, com ISSN divergente do OpenAlex: IJASS (D043) e IEEE CDC (W4407949957). Confirmar pelo DOI.
- O *Journal of Airline and Airport Management* (D040) não está indexado na Scopus.
- Quatro fontes são anais seriados com CiteScore: CDC, Winter Simulation Conference, IROS e Transportation Research Procedia. Incluí-las ou não no indicador é decisão metodológica do autor/Codex.

A planilha usa as mesmas colunas de `data/d3/citescore_2025_coleta.csv` (Codex), para fusão sem retrabalho.

Os trabalhos de congresso (AIAA) continuarão sem indicador de periódico em qualquer opção. O protocolo já prevê que eles permaneçam disponíveis para leitura técnica.

## 2. Afirmações da seção teórica e da extração

Legenda: ✅ confere · ⚠️ confere com ajuste de redação · ❓ não verificável com os textos disponíveis.

| # | Afirmação (tex / extração) | Situação | O que a fonte diz |
|---|---|---|---|
| 1 | Onat, Lupien e Sengupta (2026): a falta de posição livre no estacionamento pode impedir o início do atendimento | ✅ | arXiv:2609.37288v1, p. 2: "If the parking pads are full, the TLOF becomes blocked under the Blocking Before Service-Server Not Occupied (BBS-SNO) discipline". **Nit:** o tex fala em "espera intermediária finita", mas os stands são um nó M/M/c/c sem sala de espera (p. 3); o buffer finito K=100 fica no espaço aéreo (p. 5). Sugestão: "com capacidade finita de estacionamento". |
| 2 | Guerreiro et al. (2020): FCFS em configurações distintas revela limites por área de pouso ou por estacionamento | ❓ | Não há PDF local (`acesso.csv`: `sem_pdf_oa_direto`), embora a extração cite "PDF NASA, pp. 1–2". Há **confirmação indireta** em Wille et al. (2026), p. 14: "Guerreiro et al. (2020), who distinguished between TLOF-limited or surface-limited operational conditions". **Ação:** baixar o PDF do NTRS e conferir as pp. 1–2. |
| 3 | Wille et al. (2026): uma regra de prioridade "pode reduzir atrasos de chegada preservando a capacidade prática" | ⚠️ | p. 14: "The median typically remains equal or decreases if PBQ is implemented […] the majority of the arrival delays decrease, while a limited number of arriving aircraft experience significant delays […] the average delay is not significantly affected (0 % to 9 %)". p. 13: "In most cases, the maximum values are higher". Tabela 8: a *specific practical capacity* varia no máximo 0,5 op/h. **A redação atual omite que os atrasos máximos aumentam e que a média praticamente não muda.** A regra é por energia de reserva (PBQ) e é comparada com FIFO. Sugestão: "reduz a maioria dos atrasos de chegada, mas aumenta os máximos, sem alterar de forma relevante a média nem a capacidade prática específica". |
| 4 | ConOps NUAIR (`kunchulia2021`): a abertura do gate depende da prontidão da aeronave | ✅ | PDF p. 71 (impressa p. 62), seção 5.1.1: "when the aircraft is ready for boarding the fleet operator automation will open the departure gate". |
| 5 | Preis (2023): fluxo de passageiros sob hipóteses de lotação e de simultaneidade entre embarque e serviço da aeronave | ✅ | p. 3, §3.1: "vehicle-related turnaround and passenger boarding can happen simultaneously at the gate"; "The load factor of each vehicle is assumed to be 1.0". A premissa da D2 (recarga concluída antes do embarque, VAR‑022) é diferente, e o tex marca corretamente essa diferença. |
| 6 | Feldhoff (2022): distingue o tempo no sistema da parcela de passageiros acima do limite de cada estação | ✅ | p. 10: "longer than the maximum waiting time according to the 'Optimum' parameter […] ('number above LoS' – NALoS). In addition, we analyzed the system time". |
| 7 | Bennaceur et al. (2022): espera "entre a chegada ao vertiporto e a partida efetiva" | ⚠️ | p. 7, eq. 2: `WT_ig = f_g − E[ν_i]`, ou seja, o **horário programado** do voo menos o **horário esperado** de chegada. É uma espera esperada e planejada, não uma espera observada até a partida efetiva. Sugestão: "a espera esperada entre a chegada prevista ao vertiporto e a partida programada". As classes Regular/Premium conferem (p. 7). |
| 8 | Qin et al. (2026): relação entre capacidade, congestionamento e escolha do horário de partida | ❓ | Só existe o resumo do editor. A extração já registra esse limite. O tex afirma o vínculo com verbo assertivo ("já relacionam"); isso é aceitável apenas se o resumo disser exatamente isso. Antes da versão final, conferir o texto integral. |
| 9 | Onat et al. (2024): relacionam "decisões de frota e recarga" ao atraso dos passageiros | ⚠️ | p. 1: os 19 cenários variam **tamanho da frota e distância entre vertiportos**, e a recarga segue uma política heurística fixa ("guided by a heuristic dispatch and charge policy"). Sugestão: "relacionam o tamanho da frota, sob uma política de recarga fixa, ao atraso dos passageiros". **Versão:** a extração diz "PDF do artigo AIAA 2024", mas o arquivo lido é o **arXiv:2312.02505v1** (dez. 2023), e não a versão AIAA. Corrigir o localizador. |
| 10 | Saxena et al.: a prontidão no gate depende do fim do embarque | ✅ | arXiv:2408.01152v3, p. 12: "DRGATE_i … the time at which a departing flight i is ready to leave the gate after passenger boarding". A versão já está declarada na extração. |
| 11 | W4407949957 (Su et al.): reserva com capacidades explícitas de chegada, estacionamento e partida | ✅ | arXiv:2403.18166v4, p. 5: "three kinds of capacity constraints: (i) arrival […] (ii) departure […] (iii) parking". Na extração, citar a versão arXiv v4. |
| 12 | D040 e D044: construtos subjetivos (segurança percebida; usabilidade) | ✅ | D040 p. 8: escala Likert de 7 pontos sobre "perceived necessity of various security elements"; D044 p. 4: escala quantitativa de usabilidade de vertiportos. |
| 13 | Little (1961): `L = λW` | ✅ (conteúdo clássico) | O PDF não foi relido. O enunciado do tex está correto. "Em uma fila estável" é uma simplificação aceitável; a extração já faz a ressalva sobre janela terminante. |
| 14 | W7127406362 e D028 (somente resumo) | ❓ | Usados só na extração, não no tex. O limite já está declarado. |

**Resumo:** 8 afirmações conferem, 3 precisam de ajuste de redação (Wille, Bennaceur, Onat 2024) e 3 dependem de texto integral (Guerreiro, Qin e as de resumo). Também há 1 localizador de versão errado (Onat 2024) e 1 nit (Onat 2026). Nenhuma afirmação está contradita pela fonte.

## 3. Coerência com a D2

- O LoS temporal do tex ("proporção das visitas com espera observada […] que cumprem o limite da estação") **confere** com o VAR‑015 e o VAR‑029 da D2 e não usa a palavra "proxy".
- A premissa de recarga antes do embarque **confere** com o VAR‑022.
- **Observação para o autor, sem reabrir a decisão:** Feldhoff (2022) traz duas tabelas. A Tabela 5 (p. 8) tem os limites IATA; a Tabela 6 (p. 9) tem os limites que *ela própria adotou* para táxi aéreo, escalonados por um fator de tempo de 0,167 com base nos 20 min de voo. A D2 usa os valores da Tabela 5 (180/120/180 s). Convém que o texto diga explicitamente que a escolha é a Tabela 5, e não a adaptação da Tabela 6, para que um revisor não leia a citação como se fosse a 6.

## 4. Riscos de reprodutibilidade

1. **Resolvido em 19/11/2026.** Os 26 PDFs de `/tmp/ih214_open_pdfs/` foram copiados para `data/raw/d3/pdfs/`. Os scripts e os registros temporários do Codex e do Claude (`/tmp/ih214*`, com a procedência da triagem dupla) foram para `data/raw/d3/codex_tmp/`. A pasta `data/raw/` fica fora do Git pelo `.gitignore` (direitos autorais). O SHA‑256 e a origem de cada um dos 56 arquivos estão em `data/d3/fontes_manifesto.csv`, que é versionado. A cópia dos PDFs foi conferida como idêntica. **Para o Codex:** promover para `scripts/` os scripts de `codex_tmp/` que produziram os CSVs da D3.
2. **Toda a D3 está fora do Git** (`data/d3/`, `deliverables/D3_*`, `scripts/d3_ranking.py`, `sections/theoretical_basis.tex`). Sugestão: fazer um commit de checkpoint antes de o Codex retomar.
3. O `d3_ranking.py` fixa o ano 2026 no código. Isso é aceitável, mas convém declarar o ano como constante nomeada (`RESEARCH_YEAR`).

## 5. Pendências entregues ao Codex / autor

| Prioridade | Ação | Responsável sugerido |
|---|---|---|
| Alta | Corrigir a redação das afirmações 3, 7 e 9 no tex | Codex (dono do texto) |
| Alta | Decidir a edição do CiteScore (opções a/b/c da seção 1.1) | Autor |
| Alta | Copiar os PDFs de `/tmp` e fazer o commit de checkpoint | Autor |
| Média | Obter o PDF de Guerreiro et al. (NTRS) e o texto integral de Qin et al. (2026) | Autor (acesso CAPES/ITA) |
| Baixa | Corrigir o localizador de Onat 2024 (arXiv v1) e o nit de Onat 2026 | Codex |
