# Tarefa 01 — evidência de passageiro, turnaround e recarga

Autor: Claude (Opus 5.5), 18/11/2026. Formato: `claude/OUTPUT_TEMPLATE.md`, organizado por decisão de modelagem.
Fontes completas em `TASK_01_SOURCE_TABLE.csv` (T1-Sxx); regras e valores em `TASK_01_PARAMETER_CANDIDATES.csv` (PC-xx).
Nenhum arquivo central foi editado. As sugestões para `data/model_dictionary.csv` estão na seção final.

## Resumo executivo

| Pergunta | Resposta curta | Evidência suficiente? |
|---|---|---|
| Q1 Etapas transferíveis | check-in → pesagem → inspeção/controle de acesso → espera → caminhada → embarque. Sem despacho de bagagem e sem fronteira. | **Sim**, como sequência (PC-01). Tempos de serviço continuam fracos. |
| Q2 Ordem e pré-requisitos | desembarque concluído → serviço → aeronave pronta para embarque → embarque → checagem → despacho → slot revalidado. O Reg. (UE) 2024/1111 (UAM.OP.MVCA.205) permite recarga/troca com passageiros apenas com SOP baseada em avaliação de risco e treinamento; a não sobreposição no caso-base é decisão já registrada na D2. | **Sim** (PC-10, PC-12). |
| Q3 Atraso, no-show, assentos vazios | Nenhuma fonte de vertiporto/eVTOL estabelece comportamento ou regra. | **Não.** Item permanece indefinido; nenhum valor ou política foi adotado. |
| Q4 Eve/Joby e recarga | Os documentos oficiais trazem alcance-alvo e arquitetura, mas não trazem kWh, curva, tempo de carga nem reserva. | **Não** para valores. As classes de recarga vêm de NUAIR/NASA, NREL e EASA PTS, não de Eve/Joby. |
| Q5 Vertistop × vertiporto | Nenhuma fonte vinculante. A definição "vertistop sem recarga" vem de um rascunho da FAA que o EB 105A final não manteve. | **Não** como regra; **sim** como cenário (PC-18). |

---

## Decisão 1 — Sequência obrigatória de processamento do passageiro (Q1)

**Decisão:** a ordem `chegada → check-in → pesagem → inspeção/controle de acesso → espera → caminhada até o stand → embarque` é a que as fontes abaixo descrevem. A regra "todas as etapas são obrigatórias" é decisão da D2. As fontes **divergem** sobre inspeção completa ou só controle de acesso, e nenhuma decide; a escolha fica pendente.

**Evidência sintetizada:**
- Feldhoff (2022, pp. 2–4, Fig. 3) revisa terminais aeroportuários, serviços de helicóptero (Uber Copter, BLADE) e conceitos de vertiporto (Wisk/Skyports). Deriva check-in (com identificação), registro de massa do passageiro e da bagagem e inspeção, depois embarque. Não há despacho de bagagem (tudo é bagagem de mão) nem controle de fronteira.
- Feldhoff e Soares Roque (2021, "Passenger processing") acrescentam: controle de acesso à área de manobra, checagem da bagagem, peso e balanceamento "antes de cada voo" registrados em folha de carga, e área de espera para passageiros prontos a embarcar.
- O ConOps NUAIR/NASA (2021, §5.1.1.1, pp. 61–63) descreve a mesma ordem: emissão de bilhete → inspeção pelo pessoal de segurança → fila antes do embarque → briefing de segurança na área de embarque.
- O ICAO Doc 10121 (§6.3.2, p. 6-6) exige folha de carga finalizada antes de cada voo. O Reg. (UE) 2024/1111, UAM.OP.MVCA.175(b)(1) (p. 45), exige que o comandante esteja satisfeito quanto a massa e CG antes do voo. O regulamento não prescreve como a massa é obtida; a pesagem como estação vem de Feldhoff (2022, p. 4) e da prática da BLADE citada por ela (p. 3).

**Implicação proposta para a D2:** registrar a sequência como regra (PC-01) e a declaração de massa como pré-requisito de partida (PC-11). Quanto aos canais de check-in, PAR-005 a PAR-007 já cobrem a divisão balcão/quiosque/online.

**Classificação:** literatura (sequência); hipótese (tempos).

**Limitações e condição de transferência:** a necessidade de inspeção de segurança é deixada em aberto pelos dois artigos ("será determinada pelas autoridades"). A pesagem vem da prática de táxi aéreo de helicóptero e da folha de carga aeroportuária; é um mecanismo transferível, não uma regra eVTOL verificada aqui.

### Tempos de serviço disponíveis (fracos)

| Estação | Valor | Fonte | Natureza |
|---|---|---|---|
| Pesagem | 20 s | Feldhoff 2022, p. 5 | suposição da autora |
| Controle de acesso | U(5, 20) s | Feldhoff e Soares Roque 2021 | suposição sem citação |
| Checagem de bagagem | U(30, 60) s | Feldhoff e Soares Roque 2021 | suposição sem citação |
| Check-in e inspeção | **não reportados** | Feldhoff 2022 só cita Metzner (2020) | — |
| Área de espera → porta do gate | 31,9 s | Preis e Hornung 2022, Tab. 3 | especialistas (n = 3) |
| Entrar no gate | 19,7 s | idem | especialistas (n = 5) |
| Sair do gate | 26,7 s | idem | especialistas (n = 2) |

Nenhum desses valores é observado em vertiporto. São suposições ou estimativas **dos autores citados**, registradas com a fonte; a forma de usá-los no modelo é decisão pendente. Os tempos de check-in e de inspeção continuam como **lacuna** (VAR-004 e VAR-005 permanecem `undefined`).

---

## Decisão 2 — Ordem e pré-requisitos do turnaround (Q2)

**Decisão:** a prontidão de partida (`R_ready`, VAR-022) é uma cadeia de eventos, não uma condição única:

```text
aeronave no stand
 -> desembarque concluído e passageiros fora do airside
 -> serviço (recarga somente se a condição energética exigir; sem passageiros presentes)
 -> tripulação confirma "pronta para embarque" -> gate abre (status = embarque)
 -> cada passageiro "afivelado e pronto" (fim do embarque)
 -> folha de carga fechada; checagem de sistemas
 -> despacho pelo operador -> slot de partida revalidado -> saída do stand
```

**Evidência sintetizada:**
- NUAIR/NASA (2021): no pré-voo (§5.1.1.1, pp. 61–63), a tripulação confirma "pronta para embarque" antes de o gate abrir, e o despacho vem após checagem e autorização. No táxi e decolagem (§5.1.1.2, p. 64), o PSU revalida o slot antes da autorização. Na chegada (§5.1.1.5, pp. 69–70), os passageiros desembarcam e são conduzidos ao terminal antes de a aeronave ser declarada desembarcada e o serviço começar.
- Preis e Hornung (2022, Tab. A1, p. 20) definem o embarque como iniciado no ato de entrar na aeronave e encerrado com o passageiro "afivelado e pronto para decolar". Esse é o evento que fecha `W_pax` e alimenta `R_ready` (PC-08).
- ICAO Doc 10121 (§6.3.1, p. 6-5; Apêndice H): o turnaround é uma cadeia de dependências descrita num plano específico do operador, com metas relativas a STA/STD. O próprio manual diz que os tempos do Apêndice H são apenas indicativos.
- **Reg. (UE) 2024/1111, Anexo IX (Part-IAM), texto adotado lido no Jornal Oficial:**
  - **UAM.OP.MVCA.205** (p. 46), "Charging or swapping of VCA batteries while passengers embark, are on board, or disembark": a recarga **ou troca** com passageiros só pode ocorrer se o operador tiver (1) procedimentos operacionais padrão baseados em avaliação de risco e (2) programa de treinamento do pessoal envolvido.
  - **UAM.OP.MVCA.175(b)** (p. 45): o voo não começa sem que o comandante esteja satisfeito quanto a massa e CG, bagagem, requisitos de energia do manual de operações e carga distribuída e presa.
  - **UAM.OP.MVCA.225(b)(1)** (pp. 46–47): antes do táxi, cada passageiro sentado com o cinto afivelado.
- A EASA CRD 2022-06 (pp. 89–90, 106–107) mostra a renumeração da regra para .205 e registra a posição da EASA de que a troca de bateria é manutenção (Reg. (UE) 1321/2014).

**Implicação proposta para a D2:**
- (i) refinar a definição de VAR-022 com a cadeia acima (PC-10);
- (ii) a não sobreposição recarga × passageiros no caso-base já é **decisão registrada na D2** (seção "Aeronaves de referência e sincronização"). O texto adotado confirma que a regra **permite** a sobreposição sob condições; portanto, a D2 deve descrever a exclusão como decisão de escopo, não como proibição (PC-12);
- (iii) troca de bateria (PAR-011): **decisão pendente do autor**. Fatos: o regulamento a contempla (UAM.OP.MVCA.205); a CRD a classifica como manutenção; os OEMs pesquisados pela NREL (p. vi) não a consideram; os 10-K de Eve e Joby não a mencionam (PC-13).

**Classificação:** literatura (regulamento vinculante, ConOps e documentos oficiais).

**Limitações e condição de transferência:** o ConOps é prescritivo, para operação automatizada de alta densidade, e não traz durações. O ICAO trata de aeronaves convencionais. O regulamento vale para a UE; os AMC/GM associados não foram lidos.

---

## Decisão 3 — Passageiro atrasado, grupo incompleto, no-show e assentos vazios (Q3)

**Decisão:** **não há evidência**. Nenhum valor, taxa ou política foi adotado; o item permanece indefinido até haver fonte.

**Evidência sintetizada (o que existe):**
- Feldhoff (2022, p. 6, Tab. 2) compila janelas de chegada: serviços UAM existentes pedem chegada até 15 min antes; Wisk/Skyports consideram 15 min suficientes. Isso é a origem de PAR-004 (15–60 min). Não há dado de atraso nem de no-show.
- Feldhoff (2022, p. 10) alerta que walking e *bunching* (grupos que chegam juntos pelo mesmo modo de acesso) não foram modelados, e que esse efeito pode subestimar as filas no check-in. Não foi encontrada fonte com distribuição de chegada em grupo.
- NUAIR/NASA (2021, §5.1.1.6.1, p. 71): se a aeronave fica indisponível, os passageiros esperam no terminal; sem aeronave substituta, o voo é cancelado e eles são reacomodados (PC-19). É regra de aeronave indisponível, não de passageiro atrasado.
- Feldhoff e Soares Roque (2021): todos os passageiros de um eVTOL têm o mesmo destino, e há área de espera para "o próximo eVTOL disponível". Isso é suposição de utilização máxima.
- Fator de ocupação: Feldhoff (2022, p. 6) usa 60% fora de pico e 80% no pico, suposição da autora a partir de expectativas de fabricantes. Isso implica voos com assentos vazios na simulação dela, mas não descreve comportamento de atraso nem regra de partida.

**Implicação para a D2:** nenhuma regra nova. A pendência já listada na D2 ("definir como passageiros são agrupados por voo e se a partida pode ocorrer com assentos vazios") continua aberta e exige fonte.

**Classificação:** sem evidência.

**Limitações:** nenhuma fonte de vertiporto/eVTOL mede atraso, no-show ou tolerância de espera. Usar taxas de companhias aéreas exigiria uma fonte comportamental e uma justificativa de transferência que não foram encontradas.

---

## Decisão 4 — Recarga: necessidade, local e disciplina (Q4)

**Decisão:** a recarga é disparada por uma **condição energética de prontidão** (o estado de carga precisa cobrir a próxima missão), declarada na reserva com sua duração. Não ocorre em todo pouso. As classes de cenário mantidas são: no stand, em posição adjacente dedicada (com reposicionamento) e ausente (tipo vertistop).

**Evidência sintetizada:**
- Reg. (UE) 2024/1111, **UAM.OP.VCA.191(c)** (pp. 40–41): a energia utilizável calculada antes do voo é a soma de táxi, viagem, contingência, **reserva final** (baseada no tempo do AFM para arremeter do ponto de decisão de pouso e voltar a ele), adicional (se necessária) e extra. A UAM.OP.MVCA.175(b)(7) proíbe iniciar o voo sem cumprir esses requisitos. Assim, a **estrutura** do limiar de despacho (VAR-025) é regulatória; os valores dependem do AFM.
- NREL (2023, p. 53): um voo não é programado até a aeronave ter carga suficiente para o destino. Pp. 55–56: recarga FCFS a potência constante até 100%. A NREL cita o perfil constante até 80% com queda linear apenas como "a suposição realista mais simples", sem calibrá-lo.
- NUAIR/NASA (2021, §5.1.1.6.4, p. 73): a recarga é pedida no plano de voo e reservada com sua duração, e é feita no gate/estacionamento ou após reposicionamento, cujo tempo entra na reserva. Isso mapeia diretamente as categorias de VAR-021.
- EASA PTS (p. 18; C.200(f), p. 25; C.320, p. 36): o stand é definido para embarque/desembarque, carga e serviço, e o projeto do stand deve considerar o local do carregador. FAA EB 105A (§3.1, p. 31; §5.0, pp. 47–48): equipamento de carga amplia folgas; não há consenso sobre conectores ou classes de carga.
- Pesquisa OEM da NREL (p. vi; pp. 12–13), com fabricantes anônimos: potência DC de pico de 300 kW a 1 MW, baterias de 130 a mais de 300 kWh, dados incompletos, nenhum fabricante considerando troca de bateria.
- **Eve** (10-K 2025, Item 1): 4 passageiros + piloto; alcance esperado de 100 km na entrada em serviço; oito rotores alimentados por caminhos redundantes de uma bateria de alta tensão; carga rápida é objetivo de projeto; baterias ainda em P&D. **Ausentes:** kWh, número de pacotes, química, interface, tempo de carga, reserva.
- **Joby** (10-K 2025, Item 1): piloto + até 4 passageiros; alcance-alvo de até 100 milhas por carga; viagem média prevista de cerca de 25 milhas; quatro baterias separadas; sistema GEACS com carga simultânea de pacotes e condicionamento de bateria; especificação de interface universal a ser aberta. **Ausentes:** kWh, tempo de carga, reserva, turnaround numérico.

**Eve e Joby:** os documentos oficiais **não** contêm energia por missão, reserva, curva nem tempo de carga. Por isso não determinam se há recarga a cada escala nem quanto ela dura. Nenhum tempo de carga foi derivado.

**Implicação para a D2:** (i) VAR-008 é disparada pela regra energética (Reg. 2024/1111 UAM.OP.VCA.191; NREL p. 53) e tem a duração declarada na reserva (NUAIR/NASA p. 73); o valor permanece `undefined`; (ii) as categorias de VAR-021 vêm de NUAIR/NASA (p. 73), EASA PTS (C.200(f)) e NREL/Schweiger e Preis (vertistop) (PC-15, PC-18); (iii) a NREL usou fila FCFS no carregador (PC-16); (iv) 300–1000 kW é o único intervalo de potência publicado, com OEMs anônimos (PC-17); seu uso no modelo é decisão pendente.

**Classificação:** literatura (regras); observado (declarações OEM de metas de projeto); cenário (classes e potência).

**Limitações:** o limiar de estado de carga (energia da missão + reserva final) é **desconhecido** para Eve e Joby. Os valores de Preis e Hornung (311 kW, 133 kWh) e de Feldhoff e Soares Roque (30 min, Volocopter 2X) são genéricos ou de outro veículo. Não devem ser atribuídos às aeronaves de referência.

---

## Decisão 5 — Vertistop × vertiporto quanto à recarga local (Q5)

**Decisão:** **não existe** fonte vinculante que proíba recarga em vertistop. "Vertistop sem recarga" entra como **classe de cenário**, não como regra regulatória.

**Evidência sintetizada:**
- Schweiger e Preis (2022, pp. 4–5) mostram que a definição "vertistop: como vertiporto, mas sem carga, abastecimento, manutenção ou armazenamento" vem do **rascunho para a indústria** do FAA EB 105. A ASTM WK59317 (norma em desenvolvimento) define vertistop apenas como instalação mínima de embarque/desembarque, análoga a ponto de ônibus.
- O **FAA EB 105A final** (p. 3, nota 1) afirma que, para projeto, vertistops e vertipads são iguais a vertiportos quanto aos requisitos fundamentais. A restrição de recarga do rascunho não está no texto vigente lido.
- NREL (2023, p. 1): recarga em vertistop "dificilmente se justifica" com turnarounds rápidos. A frase é argumento econômico e operacional, citando Schweiger e Preis, e não regra.
- NUAIR/NASA (2021, p. 41): vertistop destina-se apenas a pouso e decolagem para deixar ou pegar passageiros e carga. Schweiger e Preis (2022, p. 31): turnarounds curtos (0,5–10 min) correspondem a vertistops "touch-and-go", e turnarounds longos (30 min ou mais) a vertiportos equipados.

**Implicação proposta para a D2:** manter "ausente" em VAR-021 com a justificativa "classe operacional tipo vertistop (touch-and-go), sem base regulatória de proibição". Isso evita atribuir à FAA uma restrição que o texto vigente não traz.

**Classificação:** cenário.

**Limitações:** a EASA (PTS) não define vertistop. A ASTM WK59317 é um item de trabalho e não foi lida diretamente.

---

## Decisão 6 — Level of Service (LoS) por estação (apoio à Fase D)

**Terminologia:** LoS **não** é tratado como *proxy*. Na IATA ADRM, conforme Feldhoff (2022, pp. 7–8, Tab. 4 e Fig. 4), o LoS de uma instalação de processamento é definido por critérios objetivos de **tempo de espera** e de **espaço de fila**. Satisfação é um construto distinto e não é medido neste modelo.

**Decisão:** medir LoS pelo critério de tempo máximo de espera por estação e pela proporção de passageiros acima dele (NALoS, Feldhoff 2022, p. 10). O critério de espaço exige layout do terminal e não está no escopo atual da D2.

**Evidência:** Feldhoff (2022, pp. 8–9) reporta os tempos máximos "Optimum" da IATA ADRM para primeira classe/fast-track: balcão 180 s, autoatendimento 120 s, inspeção 180 s; para a pesagem, que não existe na ADRM, a autora fixou 180 s. Ela reporta também um conjunto alternativo, economia × 0,167 (200, 20 e 100 s), fator que vem de Schweiger et al. (2021). A ADRM não foi lida diretamente; os valores vêm da reprodução em Feldhoff (2022).

**Implicação:** qual conjunto aplicar em VAR-014 (PC-09) é decisão pendente do autor; as fontes não definem um padrão de LoS para vertiporto.

**Classificação:** literatura (critério ADRM via Feldhoff 2022). **Limitação:** adaptação de uma autora sobre um manual aeroportuário.

---

## Fontes triadas e não usadas, ou não acessadas

| Fonte | Situação | Motivo |
|---|---|---|
| EASA Opinion 01/2024 (ground handling) | lida, descartada | Não trata de VTOL nem de ordem de turnaround; é proposta de quadro geral de gestão. |
| Onat et al. (2024) | **não acessada** | Sem cópia local; artigo AIAA com acesso pago; fica pendente para a regra de despacho com energia. |
| FAA AC 150/5390-2D | **não lida** | faa.gov recusou o acesso automatizado (HTTP 403). O EB 105A, que é o suplemento, foi lido. |
| Texto adotado de UAM.OP.MVCA.205 (Reg. (UE) 2024/1111) | **lido** (segunda rodada) | Ver Decisões 2 e 4 e T1-S13. |
| arXiv 2408.01152 (Saxena et al.) | **lida** (segunda rodada) | Limites analíticos de throughput para verificar o DES (PC-20) e ordem de saída do gate (PC-21). Preprint. |

## Conclusão

- **Evidência suficiente para mudar o modelo:** **sim** para sequência de passageiros, cadeia de prontidão, condição regulatória para recarga/troca com passageiros e regra energética de necessidade de recarga. **Não** para tempos de check-in/inspeção, comportamento de atraso/no-show, duração de carga de Eve/Joby e proibição regulatória de carga em vertistop.
- **Alterações aplicadas em `data/model_dictionary.csv` e `data/parameter_registry.csv`** (commits `claude:` de 18/11/2026; cada linha cita a fonte):
  1. **VAR-022** `R_ready`: cadeia da Decisão 2 (NUAIR/NASA 2021; ICAO Doc 10121; Reg. 2024/1111).
  2. **VAR-012** `W_pax`: fim do embarque = passageiro "afivelado e pronto" (Preis e Hornung 2022, Tab. A1).
  3. **VAR-005** `S_security`: variante de controle de acesso registrada como suposição de Feldhoff e Soares Roque (2021); continua `undefined`.
  4. **VAR-008** `S_charge`: disparo pela regra energética e duração reservada; continua `undefined`.
  5. **VAR-021** `L_charge`: "ausente" justificada como classe touch-and-go das fontes, sem proibição regulatória (FAA EB 105A p. 3).
  6. **Novas linhas:** VAR-023 `S_weigh` (suposição de Feldhoff 2022, 20 s); VAR-024 movimentos no gate (Preis e Hornung 2022); VAR-025 `SOC_dispatch` (estrutura do Reg. 2024/1111; valor `undefined`). As linhas de no-show e de política de atraso foram **removidas** por não terem fonte.
  7. **PAR-011** (troca de bateria): nota apenas factual; a inclusão no caso-base é decisão pendente.
- **O que permanece desconhecido:** distribuições de check-in e inspeção em vertiporto; tolerância de espera e taxas de atraso/no-show; energia por missão, valores de reserva final, curva e tempo de carga de Eve e Joby; AMC/GM da Part-IAM; requisito regulatório de inspeção de segurança de passageiros eVTOL na UE, nos EUA e no Brasil.

## Adendo — segunda rodada (18/11/2026)

- **Lido o texto adotado do Reg. (UE) 2024/1111** (T1-S13). Corrige a leitura anterior: a UAM.OP.MVCA.205 cobre recarga **e troca** com passageiros e as **permite** com SOP baseada em avaliação de risco e com treinamento. A não sobreposição no caso-base é decisão da D2; a troca de bateria é decisão pendente (PC-12, PC-13). A UAM.OP.VCA.191(c) dá a composição do limiar energético (PC-14), e a UAM.OP.MVCA.175(b) e a .225(b)(1) reforçam a cadeia de prontidão (PC-08, PC-11).
- **Lido o arXiv 2408.01152** (T1-S14): limite μ = min(μ_TLOF, μ_taxi, μ_G) para testes de verificação (PC-20) e ordem de saída do gate (PC-21).
- `data/model_dictionary.csv` e `data/parameter_registry.csv` foram atualizados com estas correções.

## Decisões do autor após a Tarefa 01 (18/11/2026)

O autor decidiu, e as decisões foram registradas em `deliverables/D2_model_design.md`:

- **Escopo da aeronave:** solo, pouso e decolagem; voo e energia de missão fora do escopo.
- **Controle de acesso** em vez de inspeção completa (PC-01, PC-03); a justificativa registrada é a única fonte com tempo de serviço, Feldhoff e Soares Roque (2021).
- **Massa do passageiro fora do escopo:** PC-02 e PC-11 não são adotados; VAR-023 e PAR-021 foram removidos.
- **Troca de bateria excluída** (PC-13; PAR-011 marcado como `excluded`).

### Revisão das decisões do autor (18/11/2026, segunda resposta)

- **Inspeção completa**, em vez de controle de acesso. VAR-005 continua sem valor. Candidato com dados medidos: *Data-Driven Analysis of Airport Security Checkpoint Operations*, Aerospace 7(6):69 (2020), doi 10.3390/aerospace7060069. Ainda **não lido**: a editora recusou acesso automatizado (HTTP 403). A tese de Metzner (2020) não foi localizada no repositório.
- **Checagem de bagagem incluída** (VAR-028, PAR-028), U(30, 60) s, suposição de Feldhoff e Soares Roque (2021).
- **LoS:** conjunto IATA ADRM de primeira classe/fast-track (PAR-026: 180/120/180 s).
- **Valores pontuais** de Preis e Hornung (2022) e de Feldhoff (2022) adotados como constantes.
- **Recarga declarada na reserva**, com o tempo de Preis (2023) em todo turnaround: 0/30/60 min (PAR-002). A proporção de voos que recarregam não tem fonte; Preis (2023) e Kotwicz et al. (2024, recarga até 100% após cada voo) aplicam recarga a todo turnaround. VAR-025 foi removido (energia fora do escopo). PAR-027 (potência) não é usado: com duração declarada a potência é desnecessária, e uma faixa de potência não é distribuição de probabilidade.
