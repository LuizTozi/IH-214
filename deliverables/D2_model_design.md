# Deliverable 2 — desenho conceitual, dados e método

## Situação

Em desenvolvimento. Este é um artefato de especificação; não é texto do artigo.

## Decisões tomadas para a versão 0

### Topologia-base regulatória

A topologia-base será a composição modular da EASA PTS-VPT-DSN (2022), e não a LIEDT ou outra
topologia proposta por artigo. Ela contém um **FATO--TLOF**, uma **taxiway/ground taxi-route** e
um **stand** conectado à área de passageiros. A PTS define esses elementos como blocos do
vertiporto e assume, no seu caso-base de projeto, no máximo uma aeronave no FATO. Portanto, a
versão-base terá capacidade unitária para o FATO--TLOF e um fluxo de uma aeronave; expansões serão
cenários posteriores. A PTS é uma especificação técnica protótipo, não uma regra vinculante, e
define geometria/viabilidade, não tempos de serviço ou capacidade horária.

### Crescimento incremental

O desenvolvimento será deliberadamente incremental:

| Fase técnica | Fronteira ativa | Critério para avançar |
|---|---|---|
| A | pouso no TLOF → liberação/saída do TLOF | eventos, exclusão mútua e tempos verificados em casos simples |
| B | Fase A + táxi, stand/gate e saída para TLOF | bloqueio e ocupação de recursos reproduzíveis |
| C | Fase B + turnaround e recarga | balanço de estados e energia/recurso consistente |
| D | Fase C + chegada, check-in, inspeção/acesso, espera e embarque | sincronização completa passageiro--eVTOL e métricas de LoS (critério de tempo da IATA ADRM) |

Todas as etapas de passageiros serão obrigatórias na Fase D; nenhuma delas será eliminada da
versão integrada por conveniência. O uso de fases serve para verificação do código, não para
redefinir o escopo final.

### Política de coordenação

O caso-base será **agendado**: um pedido é aceito quando há janela e recursos de origem/destino
compatíveis. **FCFS** será implementado como benchmark de alocação local; os resultados compararão
agendamento e FCFS sob a mesma demanda e topologia. Prioridades por emergência, energia ou classe
de passageiro ficam fora da primeira comparação, salvo se uma fonte ou resultado justificar sua
entrada.

### Aeronaves de referência e sincronização passageiro--aeronave

As aeronaves de referência serão a Eve eVTOL e a Joby S4, ambas em configuração pilotada de
**quatro passageiros mais um piloto**. Logo, um grupo de passageiros por voo terá de 1 a 4 pessoas;
o piloto não entra na demanda de passageiros. As especificações publicadas registram envergadura de
15,2 m e comprimento de 10,3 m para Eve e aproximadamente 14,0 m e 7,6 m para Joby. Esses valores
estão versionados em `data/aircraft_reference_registry.csv`.

Não se deve chamar automaticamente essas envergaduras de **D de projeto**: na EASA, D é a menor
circunferência que envolve a aeronave na configuração de decolagem/pouso. Até haver desenho de
certificação/AFM para esse fim, as dimensões publicadas servirão apenas à caracterização das
aeronaves; o dimensionamento geométrico regulatório ficará fora da Fase A e será tratado como dado
pendente, não estimado por IA.

A sincronização seguirá a lógica de turnaround de aeroportos/heliportos: uma partida requer aeronave
no stand, desembarque encerrado, grupo de até quatro passageiros que completou todas as etapas
obrigatórias, embarque concluído e slot de saída válido. A decisão de aguardar passageiro atrasado ou
partir com assentos vazios continua como cenário explícito. Como a EASA permite carga/troca durante
embarque, permanência a bordo ou desembarque somente sob avaliação de risco, procedimento e
pessoal qualificado, o caso-base **não** sobrepõe recarga e fluxo de passageiros; sobreposição será
cenário posterior condicionado a uma regra de segurança documentada.

### Decisões do autor sobre escopo (18/11/2026)

Registradas pelo autor após a Tarefa 01 (`claude/outputs/TASK_01_EVIDENCE.md`):

- **Fronteira da aeronave:** o estudo trata a eVTOL em solo e nos eventos de pouso e decolagem no
  TLOF. Voo, rota, espaço aéreo e energia de missão estão fora do escopo.
- **Controle do passageiro:** controle de acesso, e não inspeção de segurança completa. Base:
  Feldhoff e Soares Roque (2021), única fonte lida com tempo de serviço (U(5, 20) s, suposição dos
  autores); para inspeção completa não foi encontrado tempo publicado para vertiporto.
- **Massa do passageiro:** não modelada. O Reg. (UE) 2024/1111 (UAM.OP.MVCA.175(b)(1)) exige massa
  e CG conhecidos antes do voo, mas o modo de obtê-los fica fora do escopo; não há estação de
  pesagem.
- **Troca de bateria:** excluída do estudo.

### Recarga: regra de evidência

A localização e a necessidade de recarga não serão escolhidas por conveniência. O relatório FAA/NREL
mostra que ambas dependem de características OEM, rota, programação, demanda, capacidade elétrica
e restrições físicas; ele também observa que vertistops de turnaround rápido podem não justificar
recarga. Assim, a Fase A não terá carregador. Para a Fase C, serão comparados somente cenários
explicitamente justificados: recarga no stand, recarga em posição adjacente dedicada e ausência de
recarga local para operação tipo vertistop. A necessidade de recarga será determinada por estado de
energia e missão, quando parâmetros confiáveis forem disponíveis; não será imposta a cada pouso.

## Fronteira do sistema (versão 0)

Uma unidade de análise é um vertiporto de passageiros em uma janela operacional finita. O modelo
representará dois fluxos sincronizados:

```text
passageiro: chegada -> check-in -> controle de acesso -> espera -> gate -> embarque -> partida
eVTOL:     chegada -> TLOF/pad -> táxi -> stand/gate -> turnaround/recarga -> pad -> partida
```

O embarque só ocorre quando a aeronave, o gate/stand e os passageiros do voo estão elegíveis.
Assim, atraso de aeronave pode prolongar espera de passageiro; congestionamento no terminal pode,
por sua vez, atrasar a prontidão de partida. O modelo não representa rota completa, preço,
manutenção profunda, meteorologia ou um sítio real específico na primeira versão.

## Recursos e estados mínimos

| Camada | Recurso / estado | Capacidade | Regra inicial |
|---|---|---:|---|
| Coordenação | slot de chegada/partida | cenário | restringe liberação; não é tempo de serviço |
| Airside | TLOF/pad e rota de táxi | cenário | ocupação exclusiva e bloqueio físico |
| Interface | stand/gate | cenário | uma aeronave por posição; embarque/desembarque e energia podem requerê-lo |
| Energia | carregador | ausente na Fase A; cenário na Fase C | localização e necessidade definidas por evidência de missão, energia e infraestrutura |
| Terminal | check-in e controle de acesso | cenário | estações obrigatórias com filas finitas ou infinitas declaradas |
| Passageiro | grupo de voo | demanda | aguarda prontidão conjunta e tem limiar de LoS |

## Método proposto

1. Usar aproximações analíticas apenas para casos sem bloqueio (por exemplo, estabilidade e
   referência de fila multisservidor).
2. Usar simulação de eventos discretos para a rede acoplada, pois há capacidade finita,
   sincronização passageiro--aeronave e dependência entre recursos.
3. Declarar cada entrada como observada, de literatura, hipótese ou cenário. A primeira rodada
   será uma análise de cenários, não uma previsão de uma operação real.

## Métricas ligadas à pergunta de pesquisa

| Dimensão | Métrica | Definição operacional |
|---|---|---|
| Fluxo eVTOL | throughput | partidas concluídas por hora |
| Congestionamento | utilização e bloqueio | fração de ocupação por recurso; tempo ou ocorrência de bloqueio |
| Serviço do passageiro | espera até embarque | chegada ao vertiporto até início do embarque |
| Confiabilidade | P95 da espera e pontualidade | percentil 95; proporção que parte dentro da tolerância declarada |
| LoS (IATA ADRM, critério de tempo) | atendimento ao tempo máximo de espera | proporção de passageiros cuja espera em cada estação não excede o tempo máximo da IATA ADRM (Feldhoff, 2022, Tabs. 5–6) |
| Equidade | dispersão por classe/coorte | diferença de espera entre grupos definidos no cenário |

LoS não é tratado como *proxy*: na IATA ADRM ele é definido por critérios objetivos de tempo de
espera e de espaço de fila (Feldhoff, 2022, pp. 7–8). A primeira versão mede apenas o critério de
tempo; o critério de espaço exige layout do terminal. Satisfação é um construto distinto, não medido
neste modelo, e não será inferida a partir do tempo de espera.

## Decisões ainda necessárias antes de implementação integrada

- definir como passageiros são agrupados por voo e se a partida pode ocorrer com assentos vazios;
- decidir se recarga ocorre no stand ou em recurso separado e estabelecer sua regra de necessidade;
- escolher o conjunto de tempos máximos de LoS (Feldhoff, 2022, reporta dois: IATA ADRM primeira
  classe/fast-track e economia × 0,167);
- definir horizonte, aquecimento, número de replicações e sementes;
- escolher as primeiras faixas de demanda e os tempos/distribuições ainda sem evidência observada.

O dicionário em `data/model_dictionary.csv` é a fonte de verdade para essas escolhas.
