# Glossário técnico de vertidromo e operações eVTOL

## Como usar este glossário

Este glossário registra termos relevantes ao modelo do artigo e sua origem verificável. A fonte
primária desta versão é Schweiger, Knabe e Korn (2022), identificada pela chave
`schweigerKnabeKorn2022`. A página indicada é a página impressa no artigo. Quando os autores
propõem uma definição ou uma topologia para o próprio caso, isto é indicado como **definição do
estudo**; não deve ser confundido com exigência regulatória.

| Termo | Definição para leitura e para o modelo | Origem verificável | Status para esta pesquisa |
|---|---|---|---|
| UAM (*Urban Air Mobility*) | Modalidade de mobilidade aérea urbana que integra veículos, infraestrutura e serviços sob demanda ou programados. | Schweiger et al. (2022), pp. 1–2. | Contexto do sistema. |
| VTOL (*Vertical Take-Off and Landing*) | Aeronave capaz de decolar e pousar verticalmente. | Schweiger et al. (2022), pp. 1, 3. | Tipo de veículo no escopo. |
| eVTOL | VTOL com propulsão elétrica. O artigo usa predominantemente “VTOL”; o “e” é uma especificação tecnológica usada na literatura e nas normas atuais. | Schweiger et al. (2022), p. 1; EASA PTS-VPT-DSN (2022). | Não assumir características energéticas sem especificação da aeronave. |
| Aeródromo UAM | Termo genérico, adotado pelos autores a partir da FAA, para infraestrutura de solo apta a UAM. | Schweiger et al. (2022), p. 3. | Termo guarda-chuva. |
| Vertidromo (*vertidrome*) | Aeródromo UAM que acomoda somente veículos VTOL; terminologia proposta pelos autores para o estudo. | Schweiger et al. (2022), p. 3. | Útil como sinônimo conceitual de vertiporto VTOL, mas não é denominação regulatória brasileira. |
| STOLdrome | Aeródromo UAM exclusivo para aeronaves (e)STOL. | Schweiger et al. (2022), p. 3. | Fora do escopo. |
| Vertistop | Local com TLOF para embarque/desembarque, no qual o veículo é processado principalmente no próprio ponto. | Schweiger et al. (2022), p. 3. | Topologia simples de comparação. |
| Vertiport / vertiporto | Instalação que pode separar touchdown/lift-off da interação com passageiros em gate e oferecer carregamento, manutenção e outros serviços. | Schweiger et al. (2022), p. 3. | Unidade de análise do artigo. |
| Landside | Parte ligada ao passageiro e à interface terrestre do serviço. O artigo a contrasta com o airside. | Schweiger et al. (2022), pp. 1, 5. | Rede de passageiros da D2. |
| Airside | Parte operacional do lado aeronáutico: espaço terminal, TLOF, rotas de táxi e gate parking position. | Schweiger et al. (2022), pp. 2, 4. | Rede de aeronaves da D2. |
| Limite do sistema airside | No estudo, vai da entrada no espaço aéreo terminal até a posição de estacionamento no gate; inversamente para a partida. | Schweiger et al. (2022), p. 4, Fig. 1. | Define a fronteira da sub-rede airside. |
| Espaço aéreo terminal (*terminal airspace*) | Volume sob jurisdição do vertidromo, conectado ao espaço em rota e limitado em número de veículos/ operações paralelas viáveis. | Schweiger et al. (2022), p. 4. | Recurso/capacidade de cenário; não necessariamente modelado na primeira versão. |
| Espaço aéreo em rota (*enroute airspace*) | Espaço aéreo entre as áreas terminais dos vertidromos. | Schweiger et al. (2022), p. 4. | Fora da fronteira local inicial. |
| Área/ponto de transição | Interface de entrada e saída entre espaço em rota e espaço aéreo terminal. | Schweiger et al. (2022), p. 4. | Evento de entrada/saída se a camada aérea for ativada. |
| VTOL Final Approach Fix | Ponto de entrada usado pelos autores antes da aproximação final de um VTOL. | Schweiger et al. (2022), p. 4 e p. 7. | Marco de tempo/rota de cenário. |
| VTOL Initial Departure Fix | Ponto de saída após a decolagem, análogo ao marco de aproximação final. | Schweiger et al. (2022), pp. 4, 7. | Marco de tempo/rota de cenário. |
| FATO (*Final Approach and Take-Off Area*) | Área de aproximação final e decolagem que circunda o TLOF na topologia proposta. | Schweiger et al. (2022), pp. 2, 6. | Recurso geométrico; dimensões devem vir de norma/aeronave aplicável. |
| TLOF (*Touchdown and Lift-Off Area*) | Área central para toque no pouso e lift-off na decolagem. | Schweiger et al. (2022), pp. 2, 6. | Recurso de serviço exclusivo no DES. |
| Área de segurança (*safety area*) | Zona de segurança ao redor do TLOF, completando a zona crítica na topologia do estudo. | Schweiger et al. (2022), p. 6. | Restrição física de cenário. |
| Gate parking position | Posição onde a aeronave estaciona e se conecta ao fluxo de passageiros; os autores a tratam como fronteira interna do airside. | Schweiger et al. (2022), pp. 4–6. | Recurso de sincronização passageiro–aeronave. |
| Taxiway / rota de táxi | Caminho de movimentação na superfície entre TLOF e gate. | Schweiger et al. (2022), pp. 2, 6. | Recurso de movimento; pode gerar bloqueio. |
| Táxi em solo | Movimento de aeronave no solo, por capacidade própria ou dispositivo externo, entre posições do vertiporto. | Schweiger et al. (2022), p. 6. | Tempo de serviço dependente de rota/topologia. |
| Hover taxi / hovering | Movimento ou espera pairada. Os autores observam maior exigência de segurança, footprint e energia do que o táxi em solo. | Schweiger et al. (2022), p. 6. | Alternativa de cenário, não valor-base. |
| Topologia | Arranjo físico e conexão entre recursos do vertidromo. | Schweiger et al. (2022), pp. 2–3, 5. | Decisão estrutural da D2. |
| LIEDT | *Linear Independent Expandable Drive Through*: topologia linear proposta pelos autores, com fluxos separados de chegada e partida e gates atravessáveis. | Schweiger et al. (2022), pp. 5–6, Fig. 2. | Exemplo de topologia; não é padrão nem solução ótima. |
| Fluxo unidirecional | Regra de circulação em que chegadas e partidas seguem trajetórias separadas, reduzindo interação e conflito. | Schweiger et al. (2022), pp. 5–6. | Política/topologia candidata a cenário. |
| Operações independentes | Chegada e partida usam recursos/fluxos separados; simplifica a gestão, mas reduz flexibilidade de compartilhar recursos. | Schweiger et al. (2022), pp. 5, 7–8. | Trade-off a ser testado. |
| Under-Deck Parking (UDP) | Área de estacionamento sob o deck operacional, usada no caso LIEDT para guardar aeronaves e liberar gates. | Schweiger et al. (2022), pp. 6, 9. | Recurso opcional; não entra no modelo mínimo sem cenário específico. |
| Turnaround | Conjunto de processos entre chegada e próxima partida. No caso dos autores, inclui etapas específicas de posicionamento, acesso/egresso e elevador VTOL. | Schweiger et al. (2022), p. 6. | Tempo de serviço; o valor de 600 s do caso é cenário de estudo, não parâmetro universal. |
| Boarding / deboarding | Embarque e desembarque de passageiros. | Schweiger et al. (2022), pp. 5–6, 8. | Eventos que sincronizam as duas redes. |
| ConOps (*Concept of Operations*) | Descrição de topologia, perfis de missão e regras operacionais que estruturam a operação pretendida. | Schweiger et al. (2022), pp. 1–2, 5. | Especificação antes da simulação. |
| DES (*Discrete-Event Simulation*) | Simulação em que mudanças de estado ocorrem em eventos discretos; proposta pelos autores para representar layout e regras do vertidromo. | Schweiger et al. (2022), pp. 2, 9. | Método principal previsto para a D2–D4. |
| VALoS | *Vertidrome Airside Level of Service*: conceito de avaliação airside que os autores associam a capacidade, eficiência, atraso e pontualidade. | Schweiger et al. (2022), pp. 1–2, 9. | Referência para métricas airside; não mede satisfação de passageiro. |
| Slot de chegada/departida | Autorização/janela de recurso para chegada ou partida, verificada antes da operação no ConOps dos autores. | Schweiger et al. (2022), p. 4. | Regra upstream de admissão/reserva. |
| Pré-checagem de partida | Verificação de disponibilidade de posições no vertidromo de origem/destino e de espaço aéreo antes de aceitar o pedido. | Schweiger et al. (2022), p. 4. | Lógica de viabilidade e reserva. |
| Despacho (*dispatching*) | Decisão de liberar e direcionar veículos conforme demanda, disponibilidade e regras de operação. | Schweiger et al. (2022), pp. 3–4, 9. | Política de alocação a comparar. |
| Sequenciamento | Definição da ordem de atendimento/movimento de veículos. | Schweiger et al. (2022), pp. 4, 7–8. | Regra de coordenação; inicialmente FCFS. |
| FCFS | *First-come, first-served*: quem chega primeiro é atendido primeiro; regra adotada pelos autores para entrada no espaço aéreo terminal. | Schweiger et al. (2022), p. 8. | Cenário-base de política. |
| Holding / espera aérea | Procedimento para manter separação segura quando o pouso não pode ser liberado imediatamente. | Schweiger et al. (2022), pp. 7–8. | Atraso airside; não confundir com espera do passageiro. |
| Estado da aeronave | Rótulo operacional que orienta as regras de alocação. No estudo: chegada, espera, estacionamento e partida. | Schweiger et al. (2022), p. 8, Fig. 4. | Base para a máquina de estados do DES. |
| Capacidade | Aptidão de processar uma distribuição de demanda com dado arranjo e regras; depende de recursos, tempos e bloqueios. | Schweiger et al. (2022), pp. 2–3, 6, 9. | Métrica/resultante, não só “número de passageiros”. |
| Throughput | Volume de movimentos/atendimentos concluídos por unidade de tempo. | Schweiger et al. (2022), pp. 3, 4, 6. | Saída operacional do modelo. |
| Utilização | Uso relativo de infraestrutura frente à capacidade disponível. | Schweiger et al. (2022), p. 4. | Saída por recurso. |

## O que este artigo resolve para a D2

Ele sustenta a representação de TLOFs, gates, rotas de táxi, estados de aeronave, regras FCFS,
slots e bloqueios como partes de uma rede de eventos discretos. Também oferece um exemplo claro de
como o gate conecta airside e passageiro. Não fornece uma definição validada de satisfação,
distribuições empíricas de processamento terminal ou valores universais de turnaround/LoS.

## Referência base

Schweiger, K.; Knabe, F.; Korn, B. (2022). *An exemplary definition of a vertidrome's airside
concept of operations*. Aerospace Science and Technology, 125, 107144.
https://doi.org/10.1016/j.ast.2021.107144
