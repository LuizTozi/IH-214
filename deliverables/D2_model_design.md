# Deliverable 2 — desenho conceitual, dados e método

## Situação

**D2 concluída em 19 de novembro de 2026 para o caso-base sintético de topologia unitária.** As fases A a D são executáveis para verificação. A configuração rebocada
aprovada usa 37,7 s do toque à saída do TLOF e 22,8 s por trecho de táxi.
As lacunas de calibração e de execução do experimento integrado estão
identificadas por variável no protocolo de cenários.

**Revisão de 21 de novembro de 2026, após a D3.** A revisão bibliográfica não
alterou topologia, entradas, durações nem resultados dos traços A–D. Ela
precisou três definições: (1) quantidade de recursos, vazão observada (VAR-016)
e capacidade operacional sob critério de atraso são grandezas distintas;
(2) o contraste de política (VAR-018) é a admissão antecipada, e não o uso de
uma reserva técnica, que também existe em FCFS; (3) as comparações entre
políticas partem dos pedidos oferecidos e reportam admitidos, recusados e
pendentes. As fontes citadas nessas passagens foram conferidas no texto
integral em 21/11/2026. Os testes das fases A–D continuam passando (18 testes
e 5 subtestes). O estado de 19/11 permanece no commit `8d508bf`.

**Revisão de 25 de novembro de 2026, após a D4 (v2.2).** A execução do
experimento mostrou três pontos em que a D2 precisava de precisão, sem mudar
topologia, entradas ou traços A–D:
(1) a vazão (VAR-016) conta só decolagens com passageiros; as decolagens
vazias, de grupos ausentes conhecidos apenas no fechamento do manifesto, são
relatadas à parte;
(2) o tempo da chegada ao início do embarque (VAR-012) continua definido, mas
não serve para comparar desenhos quando a chegada antecede a partida em 15 a
60 min. A comparação usa a espera do fim da inspeção ao início do embarque
(VAR-045);
(3) a regra de execução da agenda (VAR-039) foi fixada: a saída planejada é
prioridade, não horário mínimo (LIT-008, §5.2.1.2, p. 82).

## Decisões tomadas para a versão 0

### Topologia-base regulatória

A topologia-base será a composição modular da EASA PTS-VPT-DSN (2022), e não a LIEDT ou outra
topologia proposta por artigo. Ela contém um **FATO--TLOF**, uma **taxiway/ground taxi-route** e
um **stand** conectado à área de passageiros. A PTS define esses elementos como blocos do
vertiporto e assume, no seu caso-base de projeto, no máximo uma aeronave no FATO. Portanto, a
versão-base terá ocupação unitária do FATO--TLOF, com uma aeronave por vez; expansões serão
cenários posteriores. A PTS é uma especificação técnica protótipo, não uma regra vinculante, e
define geometria/viabilidade, não tempos de serviço ou capacidade horária.

### Quantidade de recursos, vazão e capacidade operacional

Na D2, **capacidade de atendimento simultâneo** designa a quantidade de recursos
que podem atender ao mesmo tempo: TLOF (VAR-009), stand/gate (VAR-010), posição de
recarga (VAR-011) e postos de cada estação do terminal (VAR-042). Essas quantidades
são entradas de cenário, com unidade e regra de ocupação próprias. Duração de
serviço e separação temporal são entradas distintas; aumentar a duração não
equivale a retirar fisicamente um posto. **Vazão observada** (VAR-016) é a
contagem de decolagens concluídas dividida pela janela de observação. Uma
**capacidade operacional sob critério de atraso** só pode ser estimada após
declarar demanda, política, horizonte e limiar de atraso; não é a contagem de
posições nem a vazão de um único traço. Zhang et al. (2023, D005, DOI
10.3390/su15010709, §2 e §5.3) e Preis e Hornung (2022, D023, DOI
10.3390/app12147260, §§3.1 e 3.4) mostram por que o critério altera a capacidade
reportada: Zhang et al. obtêm 53,3 ou 31,9 surtidas/h para a mesma
configuração conforme o atraso aceitável seja 90 s ou 30 s; Preis e Hornung
definem a capacidade prática pelo limiar de atraso médio. Os valores e limiares desses estudos não são entradas transferidas
para a D2. Localizadores e limites constam da [extração da D3](../data/d3/extracao.md).

### Crescimento incremental

O desenvolvimento será deliberadamente incremental:

| Fase técnica | Fronteira ativa | Critério para avançar |
|---|---|---|
| A | pouso no TLOF → liberação/saída do TLOF | eventos, exclusão mútua e tempos verificados em casos simples |
| B | Fase A + táxi, stand/gate e saída para TLOF | bloqueio e ocupação de recursos reproduzíveis |
| C | Fase B + turnaround e recarga declarada | sequência de estados, ocupação e liberação de recursos verificadas |
| D | Fase C + chegada, check-in, checagem de bagagem, inspeção completa, espera, gate e embarque | sincronização completa passageiro--eVTOL e métricas de LoS (critério de tempo da IATA ADRM) |

Todas as etapas de passageiros serão obrigatórias na Fase D; nenhuma delas será eliminada da
versão integrada por conveniência. O uso de fases serve para verificação do código, não para
redefinir o escopo final.

### Política de coordenação

O caso-base será **agendado**: um pedido é aceito quando há janela e recursos de origem/destino
compatíveis. **FCFS** será implementado como benchmark de alocação local; os resultados compararão
agendamento e FCFS sob a mesma demanda e topologia. Prioridades por emergência, energia ou classe
de passageiro ficam fora da primeira comparação, salvo se uma fonte ou resultado justificar sua
entrada.

O contraste de política é a **admissão antecipada** condicionada à janela e à
disponibilidade futura, versus a alocação local por ordem da solicitação ao
recurso. Uma reserva técnica em linha de tempo após a solicitação pode integrar
um agendador FCFS; Guerreiro et al. (2020, D026, DOI 10.2514/6.2020-2903,
pp. 3–4 e 9–10) usam esse tipo de registro. Por isso, a presença de uma reserva
no código não classifica, sozinha, a política como agendada. A comparação
conserva os **pedidos oferecidos**, o manifesto, os serviços, os recursos e a
condição inicial; a quantidade admitida pode mudar e será reportada como
resultado da política. Os detalhes de janela, tolerância e realocação seguem
em VAR-039.

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
obrigatórias, embarque concluído e slot de saída válido. O tratamento de lugares vagos, atraso e ausência depende da regra de formação e fechamento do grupo descrita no protocolo de cenários. Como a EASA permite carga/troca durante
embarque, permanência a bordo ou desembarque somente sob avaliação de risco, procedimento e
pessoal qualificado, o caso-base **não** sobrepõe recarga e fluxo de passageiros; sobreposição será
cenário posterior condicionado a uma regra de segurança documentada.

### Decisões do autor sobre escopo (18/11/2026)

Registradas pelo autor após a Tarefa 01 (`claude/outputs/TASK_01_EVIDENCE.md`):

- **Fronteira da aeronave:** o estudo trata a eVTOL em solo e nos eventos de pouso e decolagem no
  TLOF. Voo, rota, espaço aéreo e energia de missão estão fora do escopo.
- **Inspeção do passageiro:** inspeção de segurança completa (revisão do autor, que antes escolhera
  controle de acesso). Tempo de serviço (VAR-005) ainda sem fonte; candidato aeroportuário em leitura.
- **Checagem de bagagem:** estação incluída, U(30, 60) s, suposição de Feldhoff e Soares Roque (2021).
  A fonte não diz se ela vem antes ou depois da inspeção.
- **LoS:** tempos máximos IATA ADRM de primeira classe/fast-track reproduzidos por Feldhoff (2022,
  Tab. 5): balcão 180 s, autoatendimento 120 s, inspeção 180 s.
- **Valores pontuais** de especialistas e autores (Preis e Hornung, 2022; Feldhoff, 2022) usados como
  constantes, pois as fontes não publicam distribuição.
- **Recarga:** declarada na reserva (NUAIR/NASA, 2021, p. 73), com o tempo de Preis (2023, Tab. 1,
  pp. 355–356) em todo turnaround: 0 (sem recarga local), 30 (base) ou 60 min. Preis supõe embarque
  simultâneo ao serviço da aeronave. A recarga sem passageiros é uma decisão do caso-base,
  detalhada na seção de sincronização.
  Não se usa potência nem limiar energético, pois energia de missão está fora do escopo.
- **Massa do passageiro:** não modelada. O Reg. (UE) 2024/1111 (UAM.OP.MVCA.175(b)(1)) exige massa
  e CG conhecidos antes do voo, mas o modo de obtê-los fica fora do escopo; não há estação de
  pesagem.
- **Troca de bateria:** excluída do estudo.

### Recarga declarada e ocupação de recursos

A duração é atribuída a cada turnaround como entrada do cenário (VAR-008, PAR-002).
No agendamento, os serviços previstos entram na reserva. No benchmark FCFS, a mesma
duração é conhecida na solicitação de atendimento e a alocação local segue a ordem de
chegada ao recurso. Isso mantém a carga de serviço comparável entre as políticas.
A duração de 0 min indica ausência de serviço de recarga. Desembarque e embarque seguem
o fluxo previsto em todos os níveis.

| Configuração (VAR-021) | Duração compatível | Recursos |
|---|---|---|
| No stand | 30 ou 60 min | stand e posição de recarga ocupados durante o serviço |
| Em posição separada | 30 ou 60 min | trajeto de reposicionamento e posição de recarga; acesso a stand antes e depois do serviço conforme o fluxo adotado |
| Sem recarga local | 0 min | sem ocupação de carregador |

A [implementação da Fase C](../scripts/phase_c.py) verifica na topologia unitária o caso
de 30 min no stand, a variante de 60 min e a passagem sem recarga. O
[cenário executável](../data/scenarios/phase_c_stand_verification.json) explicita
as durações por etapa e a origem de cada entrada. A verificação usa um passageiro
por sentido, com os recursos do gate disponíveis. O ConOps NUAIR/NASA (§5.1.1.6.4,
p. 73, LIT-008) descreve reserva de serviço no local de estacionamento e, alternativamente,
serviço com reposicionamento contabilizado na reserva. A EASA PTS (C.200(f), LIT-013)
prevê considerar a localização do equipamento no projeto do stand. A variante em posição
separada exige definir tempos, rota, liberação e nova alocação do stand antes de ser executada
(VAR-038). A ausência de recarga local é uma configuração de cenário.

O turno de referência e as variantes vêm de Preis (2023, §3.1 e §3.3, LIT-001). O estudo usa
VoloCity como referência e permite sobreposição entre o serviço da aeronave e o embarque.
A D2 usa as durações como cenários aplicados à configuração de referência Eve/Joby. Energia
por missão, estado de carga, potência e probabilidade de recarga ficam fora desta especificação.

### Eventos e verificação da Fase A

O relógio do serviço físico inicia no toque no TLOF e termina quando a aeronave deixa
a posição. Para cada solicitação, registrar `pedido`, `toque`, `saída física` e `liberação`.
Uma aeronave de cada vez pode ocupar o recurso. A solicitação antecede ou coincide com o
toque, e o tempo desde o pedido até o toque é atraso de acesso ao recurso. O modelo começa
na fronteira do TLOF. A espera por acesso é lógica, sem representação de holding em voo.
Se um cenário aplicar separação após a saída, ela retém a disponibilidade até a liberação,
com relógio próprio e registro separado da ocupação física. A sequência de pouso e táxi
consta no ConOps NUAIR/NASA (§5.1.1.5); o marco de separação após saída é descrito por
Preis e Hornung (2022, Tab. A1, A4).

O intervalo toque–saída tem valor de cenário adotado (VAR-006, PAR-043).
A calibração empírica permanece pendente.
Preis (2023, Apêndice A.1, Eq. 3) agrega 46,3 s de entrada no espaço aéreo, 22,9 s de
hover final até o toque, 5,0 s para parar motores e 30,0 s após desocupar o pad.
Os 99,2 s (PAR-001) são referência de outro recorte temporal. Os 30 s de A4 podem
ser usados como cenário de separação (PAR-029), com fronteira e fonte
explícitas. Separação e ocupação física são contabilizadas uma vez cada.

A Fase A usa um [simulador determinístico](../scripts/phase_a.py), com
[configuração de verificação](../data/scenarios/phase_a_verification.json) e casos
de teste documentados no protocolo. A saída é a liberação do TLOF. A contagem
de partidas concluídas começa quando a rede passa a representar partidas.

## Fronteira do sistema (versão 0)

Uma unidade de análise é um vertiporto de passageiros em uma janela operacional finita. O modelo
representará dois fluxos sincronizados:

```text
passageiro: chegada -> check-in -> checagem de bagagem e inspeção (bagagem antes da inspeção no traço D) -> espera -> gate -> embarque -> partida
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
| Interface | stand/gate | cenário | uma aeronave por posição; a ocupação cobre atendimento e bloqueio enquanto a posição está retida |
| Recarga | posição de recarga | ausente na Fase A; configuração na Fase C | requer duração positiva e localização compatível com o cenário |
| Terminal | check-in, checagem de bagagem e inspeção | VAR-042 | etapas obrigatórias com capacidade de atendimento e de fila declaradas |
| Passageiro | grupo de voo | 1 a 4 passageiros nas aeronaves de referência | aguarda prontidão conjunta; LoS é avaliado nas estações com limiar |

### Dependências entre aeronave e passageiros

O modelo integrado distingue três marcos. Os eventos vêm da cadeia de chegada,
processamento, abertura do gate e despacho do ConOps NUAIR/NASA (LIT-008,
§§5.1.1.1, 5.1.1.2, 5.1.1.5 e 5.1.1.6.4) e das definições operacionais
de Preis e Hornung (LIT-003, Tab. A1).

| Marco | Condições registradas |
|---|---|
| Aeronave pronta para embarque | aeronave no stand, desembarque concluído, passageiros desembarcados fora da área operacional, recarga prevista concluída e liberação pela tripulação |
| Passageiro apto ao embarque | check-in, checagem de bagagem e inspeção concluídos; passageiro associado ao voo e aceito pela regra vigente de fechamento do grupo |
| Partida pronta (VAR-022) | embarque concluído para o grupo aceito, despacho autorizado e slot válido quando aplicável |

O embarque começa após os dois primeiros marcos e com o gate disponível.
Registrar início e fim de embarque por passageiro e aquisição e liberação por
recurso. Isso permite medir separadamente a espera anterior ao embarque e o
bloqueio do stand após a conclusão do atendimento. A agregação dos tempos
pontuais por passageiro depende da regra de serviço e de simultaneidade no
gate (VAR-044).

## Método proposto

1. Usar aproximações analíticas apenas para casos sem bloqueio (por exemplo, estabilidade e
   referência de fila multisservidor).
2. Usar simulação de eventos discretos para a rede acoplada, pois há capacidade finita,
   sincronização passageiro--aeronave e dependência entre recursos.
3. Declarar cada entrada como observada, de literatura, hipótese ou cenário. A primeira rodada
   será uma análise de cenários, não uma previsão de uma operação real.

A revisão D3 encontrou acoplamento entre operações do lado ar e atraso de
passageiros em Preis e Hornung (2022, D036, DOI 10.3390/electronics11071071,
§§3.2–3.4) e em Preis e Hornung (2022, D023, DOI 10.3390/app12147260,
§§2–4). Assim, a contribuição a testar na D2 é mais específica: medir filas
**por estação do terminal** e sua sincronização com a prontidão da aeronave,
a recarga declarada e a retenção do stand, acompanhando desfechos em ambos os
lados. A espera agregada do passageiro nessas fontes não substitui a espera
de fila da estação definida em VAR-029: em D023 (§3.3), o atraso do passageiro
é a diferença entre o tempo no lado ar em operação real e em operação ideal.
A leitura dirigida da D3 foi concluída (`data/d3/sintese_mecanismos.md`) e
sustenta esse recorte restrito, não uma alegação ampla de novidade; o efeito
dos dois contrastes continua sendo hipótese a testar nos experimentos.

## Métricas ligadas à pergunta de pesquisa

| Dimensão | Métrica | Definição operacional |
|---|---|---|
| Fluxo eVTOL | throughput | decolagens com passageiros por hora; vazias à parte (VAR-016) |
| Congestionamento | utilização e bloqueio | fração de ocupação por recurso; tempo ou ocorrência de bloqueio |
| Serviço do passageiro | espera após a inspeção | fim da inspeção até início do embarque individual (VAR-045); a VAR-012, da chegada ao embarque, fica como descrição |
| Confiabilidade | P95 da espera e pontualidade | percentil 95; proporção que parte dentro da tolerância declarada |
| LoS (IATA ADRM, critério de tempo) | atendimento ao tempo máximo de espera | por estação, proporção das esperas mensuráveis iguais ou inferiores ao respectivo limite (VAR-015) |
| Equidade | dispersão por classe/coorte | diferença de espera entre grupos definidos no cenário |

A espera média por estação resume o congestionamento típico entre as visitas com início de atendimento observado. A espera do fim da inspeção ao início do embarque (VAR-045) mostra quanto da demora ocorre depois do processamento, à espera da aeronave ou do grupo. O P95 da chegada ao embarque (VAR-012) não é usado na comparação, pois, com chegadas de 15 a 60 min antes da partida, reflete sobretudo a antecedência. A diferença de espera média entre coortes, quando definidas no cenário, permite examinar a distribuição dessa demora.

Cada tabela comparativa identificará a **demanda oferecida comum** e, por
política, os pedidos admitidos, recusados, cancelados, concluídos e pendentes ao
fim da janela. Para indicadores de passageiro, apresentará a população elegível,
o número de observações completas, a censura e o denominador. Uma diferença
entre médias ou percentis calculados apenas entre embarcados pode refletir
mudança de composição quando uma política recusa um voo; não deve ser
interpretada isoladamente como melhora de atendimento. A comparação principal
de partidas usa todos os pedidos oferecidos e o mesmo horizonte; esperas
condicionais aos atendidos serão interpretadas junto à cobertura e às recusas.
No traço D de verificação, A2 é recusado no agendamento e concluído em FCFS:
o P95 até embarque usa duas pessoas numa política e três na outra. Esse traço
verifica a contabilidade, sem estimar efeito populacional.

Para cada estação, `VAR-029` mede o tempo da entrada em fila ao início do atendimento, em
segundos. Atendimento imediato registra 0 s. Cada estação tem seu denominador, formado pelas
visitas com início de atendimento observado. Uma fila ainda aberta ao fim da observação
é reportada como censurada. Uma estação sem observações completas tem conformidade
indefinida. Passageiros com check-in já concluído online, quando esse canal for ativado,
ficam fora dos denominadores de balcão e quiosque. O evento de fim do embarque é usado
em VAR-022. O início individual encerra VAR-012.

Os limites adotados em VAR-014/PAR-026 vêm da IATA ADRM via Feldhoff (2022, Tab. 5).
A conformidade é complementar a NALoS na mesma amostra (Feldhoff, 2022, p. 10).
Para checagem de bagagem, reportar tempo de fila e cobertura sem calcular conformidade
até dispor de limiar rastreável. O critério de espaço exige layout de terminal. As
medidas desta versão são operacionais. Satisfação exige instrumento próprio e fica fora
da medição.

## Prontidão para implementação

O [protocolo de cenários](../data/scenario_protocol.md) especifica a comparação, os
testes, as propostas para as perguntas abertas e as condições de entrada de cada fase.
O dicionário identifica as entradas ativas e pendentes. O registro de parâmetros
acompanha valores, regras e candidatos, com seus vínculos à matriz de fontes.
O traço D fixa tempos de serviço, ordem das estações e fechamento do manifesto para verificação. O desenho das réplicas e dos cenários de sensibilidade pertence ao experimento integrado.

## Partida e terminal integrados na Fase D

Por decisão do autor, as lacunas de duração são preenchidas com valores
estipulados para cenários sintéticos. Cada execução conserva a configuração
usada. O registro distingue esses valores das hipóteses e constantes tomadas
da literatura. Para o artigo, os resultados desta configuração caracterizam
o comportamento da rede sob as premissas declaradas. A calibração empírica
é uma extensão futura.

| Evidência examinada | Consequência para o modelo |
|---|---|
| NASA, ensaio multipiloto, tabelas 2 e 3 | Os 30/40 s de partida incluem táxi e os 61 s de chegada começam na aproximação. Medir a ocupação do TLOF apenas dentro dos marcos físicos. |
| FAA, ASPM, e estudo suíço com 7.168 voos elétricos | Tempos de bloco e voo permitem medir intervalos agregados. A rede mede separadamente reboque, percurso e espera. |
| Waterloo, campanha com 55 voos do Velis Electro | As médias reportadas de 54 min de carga e 88 min entre voos justificam a distinção de métricas. PAR-002 define as durações aplicadas aos eVTOLs do cenário. |
| Eve, demonstração de 30 dias com helicóptero de quatro lugares | Seis frequências diárias descrevem oferta. Pedidos e contagens de passageiros são entradas próprias do cenário. |
| ANAC, VRA e alocação de slots | Registrar separadamente solicitação, recusa por janela, cancelamento de grupo vazio, operação pendente e partida. |
| RBAC 155.201(d) e UE 2024/1111, UAM.OP.MVCA.205 | O primeiro trata da exclusividade da FATO para helicópteros. O segundo estabelece condições para recarga com passageiros. O caso-base usa um único recurso de pouso e recarga entre a saída e a entrada de passageiros. |

O [registro da busca](../data/search_log.md) reúne links e escopo das fontes.
A [configuração da fase D](../data/scenarios/phase_d_terminal_verification.json)
e o [simulador](../scripts/phase_d.py) operacionalizam a topologia unitária.
O embarque individual depende da conclusão da inspeção e da disponibilidade
da aeronave e do gate. A partida depende do último embarque, do manuseio
do rebocador e da disponibilidade de rota e TLOF.

A medição prioritária acompanha quatro eventos da mesma aeronave, em segundos
desde a abertura da janela. As diferenças sucessivas medem táxi de partida,
ocupação física e separação. No primeiro ciclo do traço D, saída do stand
aos 651,6 s, entrada no TLOF aos 674,4 s, decolagem aos 724,4 s e liberação aos 727,4 s.
Os intervalos são respectivamente 22,8 s (PAR-044), 50 s (PAR-045) e 3 s
(PAR-048). A contagem de partidas aumenta na decolagem. Um marco fora do
horizonte recebe valor nulo na medição e conserva o horário previsto no plano.

## Revisão decorrente da D4.1 · 23/11/2026

A [especificação experimental](D4_1_cenarios.md), versão 2.1, estende o caso verificado para quatro ou cinco stands com TLOF e rota compartilhados. Cada stand tem carregador e gate próprios, por suposição declarada. A especificação também traz:

- estações do terminal com um ou dois servidores;
- partida programada como referência das chegadas (15 a 60 min antes) e do fechamento do manifesto (15 min antes);
- distinção entre duração prevista e realizada;
- comunicação da recusa (agenda) ou do desvio (FCFS, se a chegada não começar até 300 s após o pedido), com saída dos passageiros do terminal.

O dia terminante, os pedidos oferecidos e os manifestos definem a população comum. A verificação da extensão pertence à D4.2.
