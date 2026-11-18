# Handoff Claude → Codex — Tarefa 01 e decisões do autor (18/11/2026)

Este arquivo resume tudo o que Claude fez desde `3e5ec30` e o que o autor decidiu, para revisão
do Codex. Detalhes e páginas estão em `claude/outputs/TASK_01_EVIDENCE.md`,
`claude/outputs/TASK_01_SOURCE_TABLE.csv` e `claude/outputs/TASK_01_PARAMETER_CANDIDATES.csv`.

Diff completo: `git diff 3e5ec30..HEAD` (11 arquivos).

## 1. Regras novas do autor, que valem para todo o trabalho

1. **Nenhuma suposição, principalmente vinda de IA.** Toda afirmação, valor, regra ou cenário deve
   indicar a fonte (documento e página/seção). Sem fonte, o item fica `undefined` e é declarado como
   lacuna. Suposições feitas por autores citados devem ser atribuídas a eles ("suposição de X"),
   nunca apresentadas como nossas.
2. **LoS não é *proxy*.** Na IATA ADRM, o LoS é definido por critérios objetivos de tempo de espera
   e de espaço de fila (via Feldhoff 2022, pp. 7–8). "Proxy" fica reservado a uma variável mensurável
   que representa um construto latente. Satisfação é construto distinto e não é medida.

## 2. Commits de Claude

| Commit | Conteúdo |
|---|---|
| `052fdfc` | Entregas da Tarefa 01 em `claude/outputs/` (síntese por decisão, 12 fontes, 19 candidatos). |
| `0f257f4` | PNGs da figura gerados pelo autor no Gemini Antigravity (duplicata removida depois). |
| `57c2fd0` | Fontes novas em `references.bib`, `literature_matrix.csv` (LIT-023 a 025) e `search_log.md`. |
| `a1b02ad` | Evidência aplicada a `model_dictionary.csv` e `parameter_registry.csv`. |
| `788d416` | Figura: pesagem e recarga condicional; espaçamento corrigido; PNG recompilado. |
| `64f36ce` | Leitura do Reg. (UE) 2024/1111 (texto adotado) e do arXiv 2408.01152; LIT-026/027. |
| `0c45d46` | Remoção de suposições de IA (no-show "suposto = 0", políticas de atraso, inferência Eve/Joby); "LoS proxy" substituído. |
| `1086776` | Primeira rodada de decisões do autor sobre escopo. |
| `2896b01` | Decisões revisadas do autor (estado atual, seção 3). |

## 3. Decisões do autor (estado atual, registradas em `deliverables/D2_model_design.md`)

| Tema | Decisão | Base / onde está |
|---|---|---|
| Fronteira da aeronave | eVTOL em solo e nos eventos de pouso e decolagem no TLOF; voo, rota, espaço aéreo e energia de missão fora do escopo | D2, "Decisões do autor sobre escopo" |
| Inspeção do passageiro | **Inspeção de segurança completa** (o autor escolheu controle de acesso e depois revisou) | VAR-005 `undefined`; PAR-025 `not_adopted` |
| Checagem de bagagem | Incluída, U(30, 60) s | Suposição de Feldhoff e Soares Roque (2021); VAR-028, PAR-028 |
| Massa do passageiro | Fora do escopo; sem estação de pesagem | Estação e linhas VAR-023/PAR-021 removidas |
| Troca de bateria | Excluída do estudo | PAR-011 `excluded` |
| LoS | Tempos máximos IATA ADRM de primeira classe/fast-track: balcão 180 s, autoatendimento 120 s, inspeção 180 s | Reproduzidos por Feldhoff (2022, Tab. 5); VAR-014, PAR-026 |
| Valores pontuais | Especialistas e autores (Preis e Hornung 2022; Feldhoff 2022) usados como constantes | As fontes não publicam distribuição; PAR-008/009/022/023/024 |
| Recarga | Declarada na reserva (NUAIR/NASA 2021, p. 73), com o tempo de Preis (2023) em **todo** turnaround: 0 (só embarque), 30 (base) ou 60 min; sem passageiros presentes | VAR-008, PAR-002; VAR-025 removido; PAR-027 `not_adopted` |

Pedidos do autor que **não** foram aplicados, com o motivo explicado a ele:
- **"Potência de recarga como probabilidade":** com a duração declarada, a potência é desnecessária, e
  a faixa 300–1000 kW (NREL, OEMs anônimos) é intervalo, não distribuição. A proporção de voos que
  recarregam não tem fonte. Preis (2023) e Kotwicz et al. (2024) aplicam recarga a todo turnaround,
  e foi isso que ficou registrado.
- **Justificativa "controle de acesso é o que a literatura mais fala":** as fontes lidas dividem-se
  (Feldhoff 2022 e NASA preveem inspeção). O autor depois optou por inspeção completa.

## 4. Correções de Claude que o Codex deve conferir

- **UAM.OP.MVCA.205 (texto adotado, Reg. (UE) 2024/1111, Anexo IX, p. 46):** o título é "Charging
  **or swapping** of VCA batteries while passengers embark, are on board, or disembark". A regra
  **permite** recarga ou troca com passageiros, desde que haja SOP baseada em avaliação de risco e
  programa de treinamento. A não sobreposição no caso-base é decisão de escopo da D2, não proibição.
  O texto da D2 já é compatível com isso.
- **UAM.OP.VCA.191(c)** (pp. 40–41) dá a composição da energia pré-voo. Não é usada, porque energia
  está fora do escopo, mas está registrada em T1-S13.
- O "vertistop sem recarga" vem do **rascunho** do FAA EB 105; o EB 105A final (p. 3, nota 1) trata
  vertistops como vertiportos para projeto. Classe de cenário, não regra.

## 5. Pontos para checagem do Codex

1. **Coerência do D2:**
   - Seção "Decisões do autor sobre escopo".
   - Fluxo da fronteira, agora "check-in -> checagem de bagagem e inspeção (ordem a definir) -> espera -> gate -> embarque".
   - Tabela do terminal, sem estações "opcionais".
   - Seção "Recarga: regra de evidência", agora com a duração declarada.
2. **Dicionário e registro:**
   - VAR-005, 008, 012, 014, 015, 021, 022, 024 e 028.
   - PAR-002, 008, 009, 011 e 022 a 028.
   - IDs removidos e não reutilizados: VAR-023, 025, 026, 027 e PAR-021.
3. **Ressalvas de Preis (2023) para constar no artigo:**
   - Veículo de referência VoloCity, de 2 lugares.
   - Preis supõe embarque simultâneo à recarga, enquanto a D2 os separa.
4. **Ressalvas de Kotwicz et al. (2024):** recarga após cada voo superestima frota e gates.
5. **Bibliografia nova:** `icao2019doc10121`, `easa2023crd202206`, `schweigerPreis2022`, `eu2024reg1111`, `saxena2025vertiminal`. Chaves e chaves de colchetes foram validadas; o build LaTeX não foi rodado.
6. **Uso de PAR-019:** contém "proxy" no sentido de "substituto". O autor ainda não decidiu.
7. **`claude/README.md`, linha 19:** ainda manda "usar proxies explícitos". Precisa ser alinhada à regra 2 da seção 1.

## 6. Lacunas abertas (sem fonte, não preencher por suposição)

| Item | Situação | Próximo passo |
|---|---|---|
| Tempo de inspeção completa (VAR-005) | Sem valor | Candidato com dados medidos: *Data-Driven Analysis of Airport Security Checkpoint Operations*, Aerospace 7(6):69 (2020), doi 10.3390/aerospace7060069. MDPI recusou acesso automatizado; o autor pode baixar pelo navegador. Tese de Metzner (2020, RWTH) não localizada. |
| Tempo de check-in (VAR-004) | Sem valor | Mesma via: Metzner (2020) ou fonte aeroportuária com dados medidos. |
| Ordem checagem de bagagem × inspeção | A fonte não diz | Decisão do autor ou fonte. |
| LoS da checagem de bagagem | A IATA ADRM, via Feldhoff, não traz valor | Fonte ou declarar ausência. |
| Atraso, no-show, assentos vazios | Sem fonte | Pendência original da D2; continua aberta. |
| Intensidade de chegada (VAR-001), horizonte, aquecimento, replicações, sementes, faixas de demanda | Abertos | Pendências da D2. |
| FAA AC 150/5390-2D; Onat et al. (2024) | Não lidos (faa.gov HTTP 403; AIAA pago) | Download manual pelo autor. |

## 7. Arquivos alterados por Claude

`claude/outputs/*` · `claude/HANDOFF_TO_CODEX.md` · `data/model_dictionary.csv` ·
`data/parameter_registry.csv` · `data/literature_matrix.csv` · `data/search_log.md` ·
`references/references.bib` · `deliverables/D2_model_design.md` · `figures/fig_coupled_network.tex` ·
`figures/fig_coupled_network.png`.

Não alterados: `deliverables/D1_framing.md` (não contém "proxy"), `claude/README.md` e os demais
arquivos centrais.
