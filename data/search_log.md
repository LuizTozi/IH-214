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
