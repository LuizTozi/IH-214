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
