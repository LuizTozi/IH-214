# D3: relatório do segundo leitor (Claude), 20/11/2026

> **Situação em 21/11/2026: recomendações resolvidas.** Este relatório registra o estado de 20/11. Desde então:
> 1. a frase de Onat et al. (2026) foi corrigida (TLOF bloqueado para novas chegadas);
> 2. D036, D023 e D029 foram lidos em texto integral e a lacuna foi restrita a filas por estação, prontidão do grupo e retenção do stand;
> 3. o resumo de Qin et al. foi arquivado com URL e data em `data/d3/extracao.md`; o texto integral segue indisponível e a seção limita a afirmação ao resumo;
> 4. as afirmações sem fonte receberam citação: critério de atraso (Zhang et al., D005; Preis e Hornung, D023) e embarque (Saxena et al., D021);
> 5. a frase sobre posto adicional foi marcada como hipótese da D2;
> 6. Guerreiro et al. (D026) foi conferido no PDF da NASA, pp. 3 e 9–10 (reservas FCFS em blocos não sobrepostos; regiões limitadas por estacionamento ou por vertipads);
> 7. D012 e D045 permanecem `texto_indisponivel`, como limite documentado.
>
> A tabela abaixo é histórica; o estado final está em `data/d3/auditoria_final.md`.

Trabalhei somente em leitura: nenhum arquivo do projeto foi alterado durante a auditoria. O relatório foi depois gravado neste arquivo. Nesta sessão, WebFetch, WebSearch e curl foram recusados pelo sistema de permissões. Por isso a tarefa (1) não pôde ser refeita online: a seção de acesso registra só o que os arquivos do projeto já documentam. As tarefas (2) e (3) usam os PDFs e textos locais (`data/raw/d3/`) e os resumos em `works.csv` e `chain_metadata.csv`.

## 1. Acesso

| Registro | URL conhecida | Versão | Situação | Pendência |
|---|---|---|---|---|
| **D012** · *Vertiport investment strategies and system congestion in urban air mobility* | DOI 10.2139/ssrn.7616311; PDF em `papers.ssrn.com/sol3/Delivery.cfm/…MECA.pdf?abstractid=7616311` (`acesso.csv`) | Preprint SSRN 2026 (`works.csv`, tipo `preprint`) | Indisponível. O Codex registrou `HTTPError`; nesta sessão não consegui tentar de novo. Não há resumo nos metadados. | Tentar entrar no SSRN com conta própria, que costuma ser exigida no download. Se não der, manter `texto_indisponivel`. Nada sobre o conteúdo pode ser afirmado. |
| **D045** · *VERTIFIED: a modular and scalable approach for designing vertiports* | `elib.dlr.de/224147/1/260326_Oguzhan_Nohutcu_DICUAM_2026_V3.pdf` | Arquivo "V3", DICUAM 2026, repositório institucional do DLR (elib) | Indisponível. O Codex registrou `HTTPError401`, o que indica acesso restrito no elib. Não há resumo. | Ver a página `elib.dlr.de/224147/` (status de acesso e resumo) ou pedir o texto ao autor ou ao DLR. Manter `texto_indisponivel`. |
| **Qin et al.** · W7171717774 · DOI 10.1016/j.tre.2026.105103, TRE 2026 | Só o DOI. `chain_access.csv` registra `sem_pdf_oa_direto` | Versão do editor | Texto integral indisponível. **Achado de reprodutibilidade:** `chain_metadata.csv` tem o campo `abstract` **vazio**. A "prévia primária do editor, resumo e destaques" citada em `extracao.md` (linha 15) não tem URL, data de acesso nem cópia local. | Obter o texto pelo Periódicos CAPES/ITA (ScienceDirect). No mínimo, guardar o resumo com URL e data de acesso. Até lá, a frase do tex sobre Qin não pode ser conferida por terceiros. |

## 2. Auditoria factual de `sections/theoretical_basis.tex`

Legenda: ❌ contradito pela fonte · ⚠️ falta citação ou ajuste · ❓ não verificável nesta sessão · ✅ confere

| § | Afirmação | Situação | Evidência |
|---|---|---|---|
| 1 | Onat et al. (2026): "quando as posições estão ocupadas, **uma chegada pode bloquear o TLOF**" | ❌ | D001, arXiv:2609.37288v1, PDF p. 2, col. esq.: "If the parking pads are full, the TLOF becomes blocked under the BBS-SNO discipline. This means that **no arriving aircraft can be serviced at or occupy the TLOF** until a parking pad becomes available". Na simulação (PDF p. 5): "aircraft must wait in the arrival queue if no parking pads are available". Quem bloqueia o TLOF é o estacionamento cheio; a chegada espera na fila e não ocupa a posição. É justamente a ressalva que `extracao.md` já faz para D001. Sugestão: "o TLOF fica bloqueado para novas chegadas, que aguardam na fila até a liberação de uma posição". A parte "capacidade finita de estacionamento" já está corrigida. |
| 1 | Little, $L=\lambda W$, com fronteiras de inspeção e de estação | ✅ | Enunciado clássico correto, e a ressalva sobre janela terminante está em `extracao.md`. Não reli o PDF. |
| 2 | "Estimar uma capacidade prática exige […] declarar o critério de atraso" | ⚠️ sem citação | A afirmação está correta, mas não cita fonte. Há duas fontes locais: D001, PDF p. 1, "capacity as the maximum steady-state throughput of aircraft per hour given that the maximum queuing delay […] remains below a specified threshold"; e Zhang et al. (D005), já em `extracao.md`. Essas fontes também sustentam a distinção pedida entre **recurso simultâneo** (entrada) e **capacidade operacional** (resultado condicionado ao critério). |
| 2 | Guerreiro et al.: FCFS com ocupações em linhas de tempo; limites por TLOF ou por estacionamento | ❓ | Não há PDF em `data/raw/d3/pdfs/`, e o NTRS citado em `extracao.md` não pôde ser aberto. Wille et al. (p. 14), segundo a auditoria anterior, confirma apenas indiretamente os limites por TLOF ou superfície. |
| 2 | "A reserva técnica após a solicitação não equivale à admissão antecipada" | ✅ como distinção do autor | Isto é interpretação, não achado de fonte, e a redação já trata assim. Há reforço independente no resumo de D029 (DOI 10.2514/6.2025-3308): o arcabouço usa um "centralized vertipad reservation registry" e compara FCFS com sequenciamento por regras. Ou seja, reserva técnica e política de alocação são dimensões distintas. |
| 2 | Wille et al.: PBQ contra FIFO; a maioria dos atrasos cai, os maiores sobem, a média e a capacidade prática quase não mudam | ✅ | Coincide com as citações da auditoria de 19/11 (pp. 13–14 e Tabela 8). Não reli o PDF, que está fora do diretório permitido nesta sessão. |
| 3 | `kunchulia2021`: abertura do gate depende da prontidão da aeronave | ✅ | ConOps, PDF p. 71, §5.1.1 (auditoria anterior). |
| 3 | "No sentido inverso, o embarque depende da disponibilidade dos passageiros" | ⚠️ sem citação | A sentença pode citar Saxena et al. (D021), arXiv:2408.01152v3, PDF p. 6, §3.1.1: "the flight whose boarding completes first will be ready to leave first", e PDF p. 12, DRGATE. |
| 3 | Preis (2023): lotação e simultaneidade entre embarque e serviço da aeronave | ✅ | PDF p. 3, §3.1 (auditoria anterior). A premissa da D2, diferente desta, está marcada. |
| 3 | "Um posto adicional na inspeção pode antecipar o embarque […] ou apenas deslocar a espera para o gate" | ⚠️ natureza | Nenhuma fonte sustenta esta frase: é uma hipótese mecanística derivada da D2. Convém marcá-la como hipótese, por exemplo "espera-se que…", para não ser lida como achado da literatura. |
| 4 | Feldhoff: Tabela 5 (IATA) e não Tabela 6; NALoS | ✅ | Coerente com a auditoria anterior. |
| 4 | Bennaceur: espera esperada entre a chegada prevista e a partida programada | ✅ | Coincide com a eq. 2, PDF p. 7. |
| 5 | "O resumo de Qin et al. relaciona capacidade, congestionamento e escolha do horário" | ❓ | Não há resumo arquivado no projeto (seção 1), então a frase não pode ser conferida. |
| 5 | Onat et al. (2024): tamanho de frota, sob política fixa de recarga, e atraso agregado | ✅ | Coincide com a auditoria anterior (arXiv:2312.02505v1, p. 1). |

## 3. Evidências contrárias à lacuna

A lacuna em exame é a sincronização local entre as filas do terminal e a prontidão do eVTOL, com desfechos medidos nos dois lados. Os cinco registros abaixo já passaram pela triagem com disposição `avancar` e foram examinados **só pelo resumo**; nenhum tem PDF local. Nenhum deles, pelo resumo, mede filas por estação do terminal. Ainda assim, quatro deles ligam recursos ou política do lado ar a desfechos do passageiro, e isso enfraquece qualquer formulação genérica da lacuna.

| # | ID · DOI | Trecho do resumo (`works.csv` / `chain_metadata.csv`) | Inferência permitida | Pendência |
|---|---|---|---|---|
| 1 | **D036** · 10.3390/electronics11071071 | "Pad operations were identified to be most impactful on passenger delays"; "Pad and gate processes have a threshold capacity beyond which delays increase exponentially"; "dynamic passenger and vehicle interactions cannot be neglected" | Já existe simulação por agentes, com pads, gates e stands, que liga processos do lado ar ao atraso do passageiro. A novidade não pode ser "acoplar aeronave e passageiro". | Ler o texto (MDPI, de acesso aberto pelo editor) e verificar se o atraso do passageiro inclui alguma etapa do terminal ou só o embarque no gate. Página: pendente. |
| 2 | **D023** · 10.3390/app12147260 | "practical hourly capacity of 264 movements […] 4 pads, 12 gates and 20 stand"; "average passenger delay of less than 3 min"; estudo paramétrico com "boarding/de-boarding" | Mede movimentos/h e atraso do passageiro **no mesmo estudo**, variando pads, gates e a duração do embarque. É evidência dos dois lados para o contraste de capacidade. Saxena (D021, PDF p. 3) descreve a ref. [34] como trabalho que "analysed average passenger delay based on vertiminal layout"; o título coincide com D023. | Conferir se [34] em D021 é D023. Verificar a definição de "passenger delay" (atraso de voo atribuído ao passageiro ou espera no terminal). Página: pendente. |
| 3 | **D029** · 10.2514/6.2025-3308 | Sequenciamento por regras contra FCFS com "passenger handling processes" e "realistic charging protocols"; "+11% total completed flights", "idle time −23%" | Há comparação de **política** (regras contra FCFS) com recarga e manuseio de passageiros. Isso contraria afirmar que a comparação entre políticas sob a mesma infraestrutura falta na literatura. Os desfechos do resumo são só do lado ar. | Sem PDF (congresso AIAA). Verificar se há medida de espera do passageiro e se a política agendada equivale à admissão antecipada da D2. |
| 4 | **W3035491886** · 10.2514/6.2020-3253 | MIP de recarga e atendimento de passageiros "to minimize the total waiting time of passengers"; "relations among the number of charging facilities […] and the service quality" | Liga a quantidade de um recurso (carregadores) à espera do passageiro, ou seja, prontidão da aeronave × desfecho do passageiro. | Sem PDF. Verificar se a "espera" vai da solicitação à partida (espera de rede) ou se inclui o terminal. Provavelmente não individualiza estações. |
| 5 | **D004** · 10.1016/j.tra.2026.105027 | "multi-server queuing theory to capture passenger waiting times at vertiports"; "expanding per-site vertipad limits yields diminishing returns beyond 2–3 vertipads" | Relaciona o número de vertipads à espera do passageiro por filas multiservidor. É uma ligação capacidade → passageiro, mas em planejamento de rede e localização. | Ler o texto e verificar se a espera é em estado estacionário e agregada por vertiporto. A transferência para a D2 exige fronteira explícita, como já ocorre com Bennaceur. |

**Leitura conjunta.** A lacuna resiste na forma restrita, desde que fique explícito que a novidade é a medida **por estação do terminal**, sincronizada com a **retenção do stand** e com o requisito de recarga declarado. Na forma "estudos não ligam lado ar e passageiro", ela é contradita por D036 e D023 (com base nos resumos), e em parte por W3035491886 e D004. S7163509946 (CTMC pouso–gate–decolagem, comparando leiautes e regras de operação) reforça o lado ar, mas não mede passageiros.

## 4. Recomendações priorizadas

**Alta**
1. Corrigir a frase de Onat et al. (2026) no §1: a fonte afirma o contrário quanto a quem ocupa o TLOF (D001, PDF p. 2).
2. Antes de fixar a lacuna no §5, ler D036 e D023 (MDPI, abertos) e registrar em `extracao.md` como evidência contrária parcial. Reformular a lacuna em termos de *filas por estação + prontidão + retenção do stand*, não de "acoplamento" genérico.
3. Qin et al.: obter o texto pela CAPES. No mínimo, arquivar o resumo com URL e data de acesso, porque hoje a frase do tex não tem rastro verificável.

**Média**
4. Dar fonte às duas afirmações sem citação: o critério de atraso na capacidade prática (D001 p. 1 ou D005) e a dependência do embarque em relação aos passageiros (D021 pp. 6 e 12).
5. Marcar como hipótese da D2 a frase sobre posto adicional e deslocamento da espera para o gate (§3).
6. Conferir Guerreiro et al. no PDF do NTRS (pp. 1, 3–4, 9–10) e verificar D029 em texto integral, para fixar a distinção entre reserva técnica e política.

**Baixa**
7. D012 e D045: manter `texto_indisponivel`, com o motivo já registrado (HTTP 401 no elib do DLR; erro no SSRN). Tentar acesso com conta ou pedir aos autores. Não inferir nada pelo título.
8. Para refazer a tarefa (1) online, liberar WebFetch ou WebSearch nesta sessão e tentar de novo `elib.dlr.de/224147/`, a página do SSRN 7616311 e os registros Crossref/OpenAlex/Unpaywall de 10.1016/j.tre.2026.105103.
