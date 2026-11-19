# Registro de busca do Deliverable 1

## Protocolo inicial

- **Data de início:** 18 de novembro de 2026.
- **Escopo:** filas e capacidade em vertiportos de passageiros, operações eVTOL, processamento
  terminal, energia/recarga e métricas de nível de serviço ou satisfação.
- **Inclusão:** estudos acadêmicos ou técnicos com método identificável e relação direta com pelo
  menos um dos cinco eixos do escopo.
- **Exclusão:** Vertiporto Sarah; estudos exclusivamente de drones de carga sem mecanismo
  transferível; notícias; material sem autoria ou fonte verificável.
- **Eixos:** capacidade airside; turnaround/energia; processamento de passageiros; teoria de
  filas/simulação; satisfação, aceitação ou qualidade de serviço.

## Acervo inicial

O acervo local de capacidade e turnaround será a primeira fonte de triagem em texto completo. As
buscas externas, suas consultas, data e resultado serão acrescentados abaixo antes da seleção final.

## Busca externa — 18 de novembro de 2026

| Consulta | Fonte | Inclusões verificadas | Uso |
|---|---|---|---|
| `10.2514/6.2019-0526` | DOI/AIAA por registros bibliográficos | Vascik e Hansman (2019) | Capacidade por topologia e operação. |
| `10.1007/s13272-021-00544-4` | Springer e repositório RWTH | Feldhoff e Soares Roque (2021) | Integra infraestrutura, processo de passageiros e demanda. |
| `Urban Air Mobility Factors Affecting Vertiport Capacity` | ICNS/DOI | Rimjha e Trani (2021) | DES de capacidade e sensibilidades de recursos. |

Os registros completos foram inseridos na matriz e no arquivo BibTeX. A busca seguinte cobrirá
satisfação, qualidade de serviço e despacho centrado no passageiro.

## Busca dirigida e leitura de fontes primárias — 18 de novembro de 2026

| Consulta / fonte | Inclusão verificada | Decisão de modelagem que suporta |
|---|---|---|
| `Passenger-centric Urban Air Mobility` / DOI | Bennaceur, Delmas e Hamadi (2022) | Espera, classes de serviço e equidade como resultados do passageiro; não modela estações de terminal. |
| `Evaluating eVTOL Network Performance` / AIAA | Onat et al. (2024) | Simulação de fluxos acoplados de passageiro, aeronave e energia; atraso do passageiro como saída. |
| `10.1016/j.tra.2024.104288` / repositório institucional | Chen et al. (2024) | Espera percebida e estados intra-vertiporto na resposta da demanda. |
| `10.1016/j.jairtraman.2023.102486` / editora e repositório | Escribano Macias et al. (2023) | Rede aberta de filas para pads e condição de estabilidade; separar espera do passageiro de loiter da aeronave. |
| FAA EB 105A; EASA PTS-VPT-DSN; FAA UAM ConOps v2.0; PCA 351-7; ANAC Panorama | Cinco documentos oficiais, lidos nas seções operativas | Geometria, segurança, slots e DCB viram limites de cenário; nenhum documento fornece calibração de LoS/satisfação ou tempos de fila. |

### Resultado de triagem

A matriz possui agora 20 fontes rastreáveis. A evidência foi agrupada por decisão de modelo, e não
por autoria: (i) recursos e bloqueios airside; (ii) turnaround, stand e energia; (iii) processamento
terminal; (iv) espera percebida, QoS e resposta da demanda; e (v) restrições de projeto e coordenação.
As fontes regulatórias foram deliberadamente classificadas como restrições de cenário, não como
dados de calibração.

## Leitura dirigida para a Deliverable 2 — 18 de novembro de 2026

| Fonte local | Inclusão verificada | Uso que altera a especificação |
|---|---|---|
| Schweiger, Knabe e Korn (2022), DOI `10.1016/j.ast.2021.107144` | Artigo completo, pp. 1–11 | Define uma topologia airside exemplar, recursos, estados de aeronave, FCFS, gates e a conexão airside–passageiro. |

Foram extraídos um glossário com páginas de origem em
`deliverables/GLOSSARY_VERTIDROME.md` e uma ressalva de evidência: LIEDT e seus tempos são
premissas de um caso de estudo, não requisitos regulatórios nem parâmetros observados universais.

## Leitura dirigida para aeronave de referência e recarga — 18 de novembro de 2026

| Fonte | Evidência verificada | Decisão que informa |
|---|---|---|
| Eve Air Mobility; documento societário oficial | Configuração inicial: 4 passageiros + piloto; envergadura publicada de 15,2 m e comprimento de 10,3 m. | Limite de grupo de passageiros; não usar envergadura como D regulatório. |
| Joby Aviation; Expo 2025 oficial | Configuração: piloto + 4 passageiros; dimensões exibidas: aproximadamente 14,0 m de envergadura e 7,6 m de comprimento. | Segunda aeronave de referência; limite de grupo de passageiros. |
| EASA Easy Access Rules for Air Operations, UAM.OP.MVCA.205 | Recarga/troca durante embarque, permanência a bordo ou desembarque exige avaliação de risco, procedimentos e pessoal qualificado. | Caso-base sem sobreposição de recarga e passageiros. |
| FAA/NREL Vertiport Electrical Infrastructure Study | Local e necessidade de EVSE dependem de aeronave, missão, demanda, programação, rede elétrica e restrições físicas; vertistops rápidos podem não justificar recarga. | Recarga como cenário da Fase C, e não requisito automático em cada pouso. |

## Fontes oficiais dos fabricantes e plano de figuras — 18 de novembro de 2026

Foram triados documentos e páginas oficiais da Eve e da Joby em
`data/oem_source_register.csv`. Os itens aproveitáveis para o modelo são capacidade de passageiros,
arquitetura de propulsão/bateria, alcance-alvo e contexto de interface de recarga. Nenhuma fonte OEM
publicada foi aceita como tempo de serviço, curva de carga certificada ou dimensão D regulatória.

O plano de figuras em `figures/FIGURE_PLAN.md` estabelece diagramas originais em TikZ e gráficos
vetoriais a partir de resultados. A primeira figura conceitual, `figures/fig_coupled_network.tex`,
representa a rede acoplada e não reutiliza imagens promocionais.

## Tarefa 01 de Claude — passageiro, turnaround e recarga — 18 de novembro de 2026

Síntese completa em `claude/outputs/TASK_01_EVIDENCE.md`; metadados em
`claude/outputs/TASK_01_SOURCE_TABLE.csv`.

| Consulta / fonte | Inclusão verificada | Decisão de modelagem que suporta |
|---|---|---|
| Acervo local IT-214 (Feldhoff 2022; Preis e Hornung 2022; NUAIR/NASA 2021; NREL 2023; EB 105A; PTS) | Releitura dirigida, com páginas | Sequência obrigatória do passageiro, cadeia de prontidão, regra energética de recarga. |
| `10.1007/s13272-021-00544-4` / PMC8395386 | Feldhoff e Soares Roque (2021), já na matriz | Controle de acesso U(5,20) s, checagem de bagagem U(30,60) s, folha de carga antes de cada voo. |
| ICAO Doc 10121 (cópia local) | `icao2019doc10121` (LIT-023) | Plano de turnaround como cadeia de dependências; tempos do Apêndice H apenas indicativos. |
| EASA CRD 2022-06 (download EASA) | `easa2023crd202206` (LIT-024) | UAM.OP.MVCA.205 trata de recarga com passageiros; troca de bateria é manutenção. |
| `10.3390/drones6070179` (cópia local) | `schweigerPreis2022` (LIT-025) | "Vertistop sem recarga" vem de rascunho do FAA EB 105; tratar como cenário. |
| SEC 10-K 2025 de Eve e Joby | Já registrados (OEM-002, OEM-004) | Sem kWh, curva, tempo de carga ou reserva: sustentam apenas classes de cenário de recarga. |

Não acessados nesta rodada: texto adotado do Reg. (UE) 2024/1111 (EUR-Lex não respondeu a acesso
automatizado), Onat et al. (2024) e FAA AC 150/5390-2D.

### Segunda rodada da Tarefa 01 — 18 de novembro de 2026

| Consulta / fonte | Inclusão verificada | Decisão de modelagem que suporta |
|---|---|---|
| EUR-Lex PDF `CELEX:32024R1111` | `eu2024reg1111` (LIT-026), texto adotado lido | UAM.OP.MVCA.205 permite recarga **ou troca** com passageiros sob SOP e treinamento; a exclusão no caso-base é escolha de modelagem. UAM.OP.VCA.191(c) define a composição do limiar energético de despacho. |
| arXiv 2408.01152 (cópia local) | `saxena2025vertiminal` (LIT-027) | Limites analíticos de throughput para verificar o DES; ordem de saída do gate. |
| FAA AC 150/5390-2D | não obtido (faa.gov respondeu HTTP 403) | Pendente; o EB 105A já cobre o necessário para recarga e passageiros. |
| Onat et al. (2024) | não obtido (AIAA, acesso pago) | Pendente. |

## Revisão de evidência da D2 — 18 de novembro de 2026

| Consulta e acesso | Leitura | Decisão afetada |
|---|---|---|
| LIT-001/002/003, PDFs no acervo local | Preis §§3.1 e 3.3, Tab. 1 e Ap. A.1; Feldhoff Tabs. 5–6 e p. 10; Preis e Hornung Tabs. 3 e A1 | Separar ocupação física de separação do TLOF, preservar cenários de recarga e aplicar LoS a esperas por estação. |
| NTRS 20210016168, PDF final corrigido | NUAIR/NASA §§5.1.1.5 e 5.1.1.6.4 | Marcos de pouso e táxi, reserva de recarga no stand e com reposicionamento. |
| Rotina de reserva e atraso em transporte de helicóptero por assento | BLADE, termos gerais §5 (LIT-028) e seção sobre compra por assento (LIT-029) | Propostas para agrupamento e fechamento da lista de embarque; nenhuma taxa ou tempo de corte foi adotado. |
| DOI 10.3390/aerospace7060069, PDF institucional da TU Delft | Janssen et al., §§2–3, Tabs. 2 e 4 (LIT-030) | Candidato para inspeção completa. Tempo de passagem incorpora espera e processos simultâneos. |
| Tempos aeroportuários de atendimento no balcão e quiosque, repositório do Técnico Lisboa | Félix, §5.2.2 pp. 54–56 (LIT-031) | Limites de atendimento candidatos, com escopo e natureza registrados. |
| Simulação terminante, aquecimento, replicações, Winter Simulation Conference | Law, §§2–6 (LIT-032) | Protocolo de horizonte e comparação pareada; configuração quantitativa depende de piloto. |

## Preparação da execução da Fase A — 19 de novembro de 2026

- O [ConOps Skyports/Wisk](https://skyports.net/wp-content/uploads/2022/06/2022-04-06-Concept-of-Operations-Autonomous-AAM-Aircraft-Operations-and-Vertiport-Integration-1.pdf), pp. 26–27, descreve checagens após o toque, preparação para movimentação e saída. O recorte FATO do documento também cobre a aproximação e a área de segurança. O documento informa os marcos do processo, mas não fornece duração toque–saída compatível com VAR-006. Mantido como fonte triada para o plano de medição, sem entrada numérica adotada.

## Evidência para VAR-006 e VAR-041 — 19 de novembro de 2026

| Fonte primária | Ponto examinado | Uso na D2 |
|---|---|---|
| Preis e Hornung (2022), LIT-003 | §§4.3.1 e 4.3.4, Tab. 3 e Ap. D, Tab. A1 (T1–T4, T7/A3, A2 e A4) | Separa toque, desligamento, acoplamento, movimento e separação. Componentes e velocidades em PAR-035 a PAR-038; a duração toque–saída não é publicada como medida. |
| Zelinski (2020), LIT-033 | §V.B | Táxi a 4 ft/s (aprox. 1,22 m/s), regra prática de especialistas em helipontos. Os 60 s para aproximação são agregados. |
| Wille (2024), LIT-034 | §§3.1–3.2, Tab. 2 e Fig. 4 | Distância dividida pela velocidade, hipótese de 1,8 m/s, precedência e aquisição/liberação de recursos. As referências de chegada agregam a aproximação. |
| ConOps Skyports/Wisk (2022) | pp. 26–27 | Checagens, desligamento e movimentação após o toque fazem parte do processo descrito. Sem tempos compatíveis com VAR-006. |

## Busca dirigida de dados operacionais para as fases A–C — 19 de novembro de 2026

Busca em português e inglês por tempos de ocupação de vertipad, reboque em heliponto, embarque, sessões de recarga de aeronaves elétricas, marcos de movimento e pedidos de slots. O critério para transferir um tempo foi a compatibilidade entre aeronave, processo e eventos inicial e final. Os resultados abaixo são referências externas para a D2. Nenhum valor foi incorporado ao cenário executável.

| Entrada da D2 | Evidência localizada e recorte | Uso e lacuna |
|---|---|---|
| VAR-006 e ocupação de partida | [NASA, estudo multipiloto, tabelas 2 e 3](https://ntrs.nasa.gov/citations/20240007351). Em simulador com dez pilotos, 61 s em média desde a decisão de desacelerar na aproximação até liberar o pad. Do início do táxi à decolagem, 30 s em partidas expeditas (um caso de 57 s excluído pelos autores) e 40 s nas demais. | Comparação entre procedimentos. Ambos os cronômetros começam antes da fronteira física usada no respectivo serviço da D2. Faltam toque, entrada no TLOF na partida e saída física individualizados em operação rebocada. |
| VAR-041 e PAR-037 | [FAA, dicionário ASPM](https://aspmhelp.faa.gov/index/ASPM__Individual_Flights__Definitions_of_Variables.html). Taxi-in vai do toque à chegada ao gate. Taxi-out vai da saída do gate à decolagem. Alguns horários são estimados. [Preis e Hornung, LIT-003](../data/literature_matrix.csv), tabela 3, documentam velocidade e manuseio por consulta a especialistas. | O trecho da D2 começa ao liberar o TLOF. Falta cronometragem com distância conhecida que separe acoplamento, deslocamento, espera e desconexão. |
| PAR-002 e duração no stand | [Universidade de Waterloo, campanha de agosto de 2024, gráfico 3 e texto](https://uwaterloo.ca/sustainable-aeronautics/blog/electric-plane-performance-2024-how-many-hours-can-flight). Ao longo de 55 voos de treinamento do Velis Electro, os autores reportam médias de 54 min para recarga e 88 min entre fim de um voo e início do próximo. O total de sessões de carga usado na média não é especificado. [Estudo suíço, seção de dados e figura 4](https://doi.org/10.3390/wevj16030118) descreve 7.168 voos de 14 aeronaves elétricas com horários de bloco e voo. | Referência empírica em asa fixa. A lista de campos do estudo suíço não individualiza início e fim de carga. Faltam pares duração declarada/realizada por sessão para a configuração de referência. |
| PAR-008/009/023/024 e demanda | [Eve, ConOps Rio, pp. 29–30](https://www.eveairmobility.com/storage/2023/03/EveConopsRJ.pdf). Demonstração com Bell 505 de quatro lugares para passageiros, seis frequências diárias previstas durante 30 dias. A estimativa de 2,6 passageiros por voo na p. 30 é premissa de projeção. | Precedente de oferta por horário. As frequências não identificam pedidos, recusas ou chegadas individuais. Para calibrar o embarque faltam contagem e horários por grupo, travessia da porta e liberação pela tripulação. |
| Solicitação, oferta de horário e execução | [ANAC, serviço de alocação](https://www.gov.br/pt-br/servicos/solicitar-alocacao-de-slots) distingue indisponibilidade, aceite, recusa de oferta e cancelamento. [Metadados VRA](https://www.anac.gov.br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/voo-regular-ativo-vra/62-voo-regular-ativo-vra) registram voos previstos, realizados e cancelados. | Referência para codificar eventos distintos. Os voos regulares publicados não fornecem o denominador de pedidos de atendimento do vertiporto. |
| Regras de recurso | [ANAC, RBAC 155, 155.201(d)](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbha-e-rbac/rbac/rbac-155) prevê exclusividade da FATO para helicópteros. [Regulamento de Execução (UE) 2024/1111, UAM.OP.MVCA.205](https://eur-lex.europa.eu/eli/reg_impl/2024/1111/oj/eng) condiciona a recarga durante embarque, permanência a bordo ou desembarque a procedimentos baseados em avaliação de risco e treinamento. | Identificam recurso e condições operacionais nos respectivos âmbitos. Não quantificam separação em segundos nem duração de recarga. |
