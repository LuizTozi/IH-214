# Tarefa 01 — evidência de passageiro, turnaround e recarga

Autor: Claude (Opus 5.5), 18/11/2026. Formato: `claude/OUTPUT_TEMPLATE.md`, organizado por decisão de modelagem.
Fontes completas em `TASK_01_SOURCE_TABLE.csv` (T1-Sxx); regras e valores em `TASK_01_PARAMETER_CANDIDATES.csv` (PC-xx).
Nenhum arquivo central foi editado. As sugestões para `data/model_dictionary.csv` estão na seção final.

## Resumo executivo

| Pergunta | Resposta curta | Evidência suficiente? |
|---|---|---|
| Q1 Etapas transferíveis | check-in → pesagem → inspeção/controle de acesso → espera → caminhada → embarque. Sem despacho de bagagem e sem fronteira. | **Sim**, como sequência (PC-01). Tempos de serviço continuam fracos. |
| Q2 Ordem e pré-requisitos | desembarque concluído → serviço → aeronave pronta para embarque → embarque → checagem → despacho → slot revalidado. Recarga e passageiros mutuamente exclusivos no caso-base. | **Sim** (PC-10, PC-12). |
| Q3 Atraso, no-show, assentos vazios | Nenhuma fonte de vertiporto/eVTOL estabelece comportamento ou regra. | **Não.** Manter como cenário declarado. |
| Q4 Eve/Joby e recarga | Os documentos oficiais trazem alcance-alvo e arquitetura, mas não trazem kWh, curva, tempo de carga nem reserva. Sustentam só a existência das classes de cenário. | **Parcial**: sustenta a classe de cenário, não sustenta valores. |
| Q5 Vertistop × vertiporto | Nenhuma fonte vinculante. A definição "vertistop sem recarga" vem de um rascunho da FAA que o EB 105A final não manteve. | **Não** como regra; **sim** como cenário (PC-18). |

---

## Decisão 1 — Sequência obrigatória de processamento do passageiro (Q1)

**Decisão:** fixar na Fase D a ordem `chegada → check-in → pesagem → inspeção/controle de acesso → espera → caminhada até o stand → embarque`. Todas as etapas são obrigatórias. A inspeção é uma estação cujo tempo de serviço varia por cenário (inspeção completa ou só controle de acesso); ela não é removida.

**Evidência sintetizada:**
- Feldhoff (2022, pp. 2–4, Fig. 3) revisa terminais aeroportuários, serviços de helicóptero (Uber Copter, BLADE) e conceitos de vertiporto (Wisk/Skyports). Deriva check-in (com identificação), registro de massa do passageiro e da bagagem e inspeção, depois embarque. Não há despacho de bagagem (tudo é bagagem de mão) nem controle de fronteira.
- Feldhoff e Soares Roque (2021, "Passenger processing") acrescentam: controle de acesso à área de manobra, checagem da bagagem, peso e balanceamento "antes de cada voo" registrados em folha de carga, e área de espera para passageiros prontos a embarcar.
- O ConOps NUAIR/NASA (2021, §5.1.1.1, pp. 61–63) descreve a mesma ordem: emissão de bilhete → inspeção pelo pessoal de segurança → fila antes do embarque → briefing de segurança na área de embarque.
- O ICAO Doc 10121 (§6.3.2, p. 6-6) exige folha de carga finalizada antes de cada voo. Isso justifica a pesagem como **pré-requisito de prontidão**, não como conveniência.

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

Nenhum desses valores é observado em vertiporto. Devem entrar como faixas de sensibilidade, e os tempos de check-in e de inspeção continuam como **lacuna** (VAR-004 e VAR-005 permanecem `undefined`).

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
- EASA CRD 2022-06 (pp. 89–90, 106–107) confirma que **UAM.OP.MVCA.205** trata de "recarga de baterias com passageiros embarcando, a bordo ou desembarcando" para VCA elétricas. Também registra que a troca de bateria é manutenção (Reg. (UE) 1321/2014) e exige pessoal certificador.

**Implicação proposta para a D2:** (i) refinar a definição de VAR-022 com a cadeia acima (PC-10); (ii) manter a exclusão recarga × passageiros no caso-base (PC-12, confirma a decisão já tomada); (iii) retirar a troca de bateria (PAR-011) dos cenários-base e deixá-la, no máximo, como cenário exploratório rotulado (PC-13).

**Classificação:** literatura (ConOps e documentos oficiais); regra de cenário para a sobreposição.

**Limitações e condição de transferência:** o ConOps é prescritivo, para operação automatizada de alta densidade, e não traz durações. O ICAO trata de aeronaves convencionais. O texto adotado de UAM.OP.MVCA.205 **não** foi relido literalmente nesta tarefa, porque o EUR-Lex não respondeu ao acesso automatizado. Uso o registro já feito por Codex em `data/search_log.md`, e a CRD confirma o objeto e a numeração da regra.

---

## Decisão 3 — Passageiro atrasado, grupo incompleto, no-show e assentos vazios (Q3)

**Decisão:** **não há evidência** para calibrar comportamento. Manter como **cenário explícito**, sem valor de base.

**Evidência sintetizada (o que existe):**
- Feldhoff (2022, p. 6, Tab. 2) compila janelas de chegada: serviços UAM existentes pedem chegada até 15 min antes; Wisk/Skyports consideram 15 min suficientes. Isso é a origem de PAR-004 (15–60 min). Não há dado de atraso nem de no-show.
- Feldhoff (2022, p. 10) alerta que walking e *bunching* (grupos que chegam juntos pelo mesmo modo de acesso) não foram modelados, e que esse efeito subestima as filas no check-in. Isso apoia gerar chegadas por grupo (1–4) em vez de passageiros independentes.
- NUAIR/NASA (2021, §5.1.1.6.1, p. 71): se a aeronave fica indisponível, os passageiros esperam no terminal; sem aeronave substituta, o voo é cancelado e eles são reacomodados (PC-19). É regra de aeronave indisponível, não de passageiro atrasado.
- Feldhoff e Soares Roque (2021): todos os passageiros de um eVTOL têm o mesmo destino, e há área de espera para "o próximo eVTOL disponível". Isso é suposição de utilização máxima.
- Fator de ocupação: Feldhoff (2022, p. 6) usa 60% fora de pico e 80% no pico, por suposição, a partir de expectativas de fabricantes. Isso sustenta explicitamente partidas com assentos vazios como **cenário**, não como comportamento observado.

**Implicação proposta para a D2:** declarar três políticas de cenário, sem pretensão empírica: (a) aguardar o grupo completo até o STD e depois partir; (b) partir no slot com os assentos vazios; (c) reacomodar o atrasado no próximo voo com assento livre. A taxa de no-show/atraso fica como parâmetro de sensibilidade **suposto**, com valor 0 no caso-base.

**Classificação:** cenário.

**Limitações:** nenhuma fonte de vertiporto/eVTOL mede atraso, no-show ou tolerância de espera. Usar taxas de companhias aéreas exigiria uma fonte comportamental e uma justificativa de transferência que não foram encontradas.

---

## Decisão 4 — Recarga: necessidade, local e disciplina (Q4)

**Decisão:** a recarga é disparada por uma **condição energética de prontidão** (o estado de carga precisa cobrir a próxima missão), declarada na reserva com sua duração. Não ocorre em todo pouso. As classes de cenário mantidas são: no stand, em posição adjacente dedicada (com reposicionamento) e ausente (tipo vertistop).

**Evidência sintetizada:**
- NREL (2023, p. 53): um voo não é programado até a aeronave ter carga suficiente para o destino. Pp. 55–56: recarga FCFS a potência constante até 100%. A NREL cita o perfil constante até 80% com queda linear apenas como "a suposição realista mais simples", sem calibrá-lo.
- NUAIR/NASA (2021, §5.1.1.6.4, p. 73): a recarga é pedida no plano de voo e reservada com sua duração, e é feita no gate/estacionamento ou após reposicionamento, cujo tempo entra na reserva. Isso mapeia diretamente as categorias de VAR-021.
- EASA PTS (p. 18; C.200(f), p. 25; C.320, p. 36): o stand é definido para embarque/desembarque, carga e serviço, e o projeto do stand deve considerar o local do carregador. FAA EB 105A (§3.1, p. 31; §5.0, pp. 47–48): equipamento de carga amplia folgas; não há consenso sobre conectores ou classes de carga.
- Pesquisa OEM da NREL (p. vi; pp. 12–13), com fabricantes anônimos: potência DC de pico de 300 kW a 1 MW, baterias de 130 a mais de 300 kWh, dados incompletos, nenhum fabricante considerando troca de bateria.
- **Eve** (10-K 2025, Item 1): 4 passageiros + piloto; alcance esperado de 100 km na entrada em serviço; oito rotores alimentados por caminhos redundantes de uma bateria de alta tensão; carga rápida é objetivo de projeto; baterias ainda em P&D. **Ausentes:** kWh, número de pacotes, química, interface, tempo de carga, reserva.
- **Joby** (10-K 2025, Item 1): piloto + até 4 passageiros; alcance-alvo de até 100 milhas por carga; viagem média prevista de cerca de 25 milhas; quatro baterias separadas; sistema GEACS com carga simultânea de pacotes e condicionamento de bateria; especificação de interface universal a ser aberta. **Ausentes:** kWh, tempo de carga, reserva, turnaround numérico.

**O que se pode inferir de Eve/Joby, e só isso:** as duas declaram alcance-alvo maior que a missão urbana típica que elas próprias citam. Isso torna **plausíveis** tanto um cenário sem recarga em cada escala quanto um cenário com recarga periódica. Os documentos não permitem decidir qual ocorre nem quanto dura, porque falta a energia por missão e a reserva regulatória. Logo, ambas as classes devem ser mantidas e nenhum tempo de carga deve ser derivado.

**Implicação proposta para a D2:** (i) base de VAR-008: "duração = f(déficit de energia, potência), apenas quando a condição PC-14 não é atendida"; (ii) VAR-021 com as três categorias justificadas (PC-15, PC-18); (iii) fila de carregador FCFS no cenário (PC-16); (iv) 300–1000 kW apenas como limites de sensibilidade de potência (PC-17), sem conversão em duração.

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

## Decisão 6 — Métrica de LoS por estação (apoio à Fase D)

**Decisão:** além de `p_LoS` global (VAR-015), registrar a **proporção acima do limiar por estação** (NALoS, Feldhoff 2022) como métrica de diagnóstico de gargalo.

**Evidência:** Feldhoff (2022, pp. 8–9) usa os limites "Optimum" da IATA ADRM para primeira classe/fast-track: balcão 180 s, autoatendimento 120 s, inspeção 180 s, e pesagem 180 s por escolha da autora. Ela mostra ainda um conjunto alternativo com fator de tempo 0,167 (200, 20 e 100 s). O balcão de check-in foi o gargalo (pp. 10–12).

**Implicação:** usar os dois conjuntos como níveis de cenário de VAR-014 (PC-09), nunca como satisfação.

**Classificação:** cenário. **Limitação:** é uma adaptação de uma autora sobre um manual aeroportuário; não há padrão de LoS de vertiporto.

---

## Fontes triadas e não usadas, ou não acessadas

| Fonte | Situação | Motivo |
|---|---|---|
| EASA Opinion 01/2024 (ground handling) | lida, descartada | Não trata de VTOL nem de ordem de turnaround; é proposta de quadro geral de gestão. |
| Onat et al. (2024) | **não acessada** | Sem cópia local; fica pendente para a regra de despacho com energia. |
| FAA AC 150/5390-2D | **não lida** | O EB 105A (suplemento) foi lido; o AC-base não foi verificado nesta tarefa. |
| Texto adotado de UAM.OP.MVCA.205 (Reg. (UE) 2024/1111) | **não relido** | O EUR-Lex não respondeu ao acesso automatizado; ver Decisão 2. |
| arXiv 2408.01152 (vertiport terminal scheduling) | não triada | Fora do tempo desta rodada; candidata para a política de alocação passageiro–voo. |

## Conclusão

- **Evidência suficiente para mudar o modelo:** **sim** para sequência de passageiros, cadeia de prontidão, exclusão recarga × passageiros, exclusão da troca de bateria do caso-base e regra energética de necessidade de recarga. **Não** para tempos de check-in/inspeção, comportamento de atraso/no-show, duração de carga de Eve/Joby e proibição regulatória de carga em vertistop.
- **Alterações sugeridas para `data/model_dictionary.csv`** (não aplicadas; Codex decide):
  1. **VAR-022** `R_ready`: substituir a definição pela cadeia da Decisão 2; `source_or_basis` = "NUAIR/NASA 2021 §5.1.1.1/§5.1.1.5; ICAO Doc 10121 §6.3; EASA CRD 2022-06 (UAM.OP.MVCA.205)".
  2. **VAR-012** `W_pax`: definir o fim como "primeiro passageiro do grupo inicia o embarque" e registrar o evento "afivelado e pronto" (Preis e Hornung 2022, Tab. A1) como fim do embarque.
  3. **VAR-005** `S_security`: nota "variante de controle de acesso U(5,20) s, Feldhoff e Soares Roque 2021; screening completo sem fonte"; manter `undefined`.
  4. **VAR-008** `S_charge`: base "apenas quando o estado de carga não cobre a próxima missão (NREL 2023 p. 53); duração reservada (NUAIR/NASA 2021 p. 73)"; manter `undefined` por falta de energia por missão de Eve e Joby.
  5. **VAR-021** `L_charge`: justificar "ausente" como classe touch-and-go, sem base regulatória (FAA EB 105A p. 3).
  6. **Novas linhas sugeridas:** `S_weigh` (hipótese, 20 s); `t_walk_in`/`t_gate_in`/`t_gate_out` (literatura, Preis e Hornung 2022); `SOC_dispatch` (limiar energético, **undefined**); `p_noshow` (cenário, **suposto** = 0 no caso-base, sem fonte); `R_late_policy` (cenário: aguardar / partir vazio / reacomodar).
  7. `parameter_registry.csv`, **PAR-011** (troca de bateria): nota "excluída do caso-base: manutenção sob Reg. (UE) 1321/2014 (EASA CRD 2022-06 p. 90)".
- **O que permanece desconhecido:** distribuições de check-in e inspeção em vertiporto; tolerância de espera e taxas de atraso/no-show; energia por missão, reserva final, curva e tempo de carga de Eve e Joby; texto literal adotado de UAM.OP.MVCA.205; requisito regulatório de inspeção de segurança de passageiros eVTOL na UE, nos EUA e no Brasil.
