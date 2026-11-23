# D4.1 — Especificação do experimento integrado, versão 2

Versão de trabalho revisada em 23/11/2026. A redação do desenho experimental do artigo ocorrerá após a conclusão integral da D4. A unidade de comparação é uma janela operacional sintética. A pergunta é quanto mudam as decolagens por hora, a cobertura da demanda oferecida, a espera **em cada estação do terminal** e a retenção da aeronave pelo grupo quando se altera a admissão, a quantidade de stands ou a quantidade de servidores de uma estação. O piloto avaliará a precisão e a adequação da faixa de carga.

## Por que a versão 1 foi revista

A revisão crítica de 23/11/2026 mostrou que a versão 1 não podia observar o que a D3 apresenta como contribuição:

1. Todo passageiro presente percorria balcão, bagagem e inspeção antes de saber da recusa. As filas do terminal eram calculadas sem depender da aeronave (`scripts/phase_d.py`, função `terminal`). A espera por estação era, portanto, idêntica em todas as configurações.
2. Os passageiros chegavam até o pedido t e ficavam prontos por volta de t + 400 s. Com recarga de 30 ou 60 min, a aeronave só ficava pronta para embarque depois de t + 1980 s. O grupo nunca retinha a aeronave fora da família sem recarga.
3. Com um ou dois stands e um carregador, o lado ar limitava o fluxo a poucos passageiros por hora. A ocupação do balcão ficava em torno de 40% ou menos, e quase não se formavam filas.
4. O perfil de chegada era estipulado pelos autores, embora o cadastro já tivesse a janela de Feldhoff 2022 (PAR-004).

A versão 2 corrige cada ponto com quatro decisões do autor:

- **Lado ar:** escala de Feldhoff 2022 (1 TLOF e 5 stands).
- **Terminal:** contrastes de servidor no balcão e na inspeção, avaliados um por vez.
- **Recusa:** avisada no instante da decisão.
- **Chegadas:** relativas à partida programada, com a janela da fonte.

## Configurações e contrastes

| Configuração | Stands | Balcões | Postos de inspeção | Papel |
|---|---:|---:|---:|---|
| Base | 5 | 1 | 1 | referência de todos os contrastes |
| S4 | 4 | 1 | 1 | contraste de estacionamento: Base menos S4 |
| B2 | 5 | 2 | 1 | contraste do balcão: B2 menos Base |
| I2 | 5 | 1 | 2 | contraste da inspeção: I2 menos Base |

Cada configuração roda sob duas políticas: agendamento antecipado e FCFS local. Isso dá 8 células por família. Há quatro contrastes principais, todos pareados dentro da réplica:

- **Política:** agenda menos FCFS em cada configuração.
- **Estacionamento:** Base menos S4 sob política fixa.
- **Balcão:** B2 menos Base sob política fixa.
- **Inspeção:** I2 menos Base sob política fixa.

A estação de bagagem mantém um servidor em todas as células.

**Por que cada contraste afeta o terminal**

- Os contrastes de servidor mudam diretamente a capacidade de uma estação.
- O contraste de política muda a carga do terminal, porque a recusa passa a retirar passageiros das filas.
- O contraste de stands não muda o terminal diretamente. Ele aparece na espera depois da inspeção e na retenção do stand.

## Matriz de famílias para cada réplica

| Família | Pedidos/h no período de oferta | Recarga por voo | Informação da agenda |
|---|---:|---:|---|
| Referência | 6 | 30 min | durações declaradas |
| Demanda baixa | 4 | 30 min | durações declaradas |
| Demanda alta | 8 | 30 min | durações declaradas |
| Sem recarga local | 6 | 0 min | durações declaradas |
| Recarga longa | 6 | 60 min | durações declaradas |
| Informação perfeita | 6 | 30 min | chegadas e durações de bagagem realizadas |

- **Cinco primeiras famílias:** 8 células cada, total de 40.
- **Família de informação perfeita:** acrescenta quatro execuções de agendamento, uma por configuração. Seus controles FCFS são os da referência, pois o FCFS usa apenas eventos realizados.
- **Total:** 44 execuções distintas por réplica. Pedidos futuros permanecem desconhecidos em todas as células.

### Escolha da faixa de demanda

Os números abaixo são **estimativas determinísticas dos autores**, calculadas com o cadastro. A D4.2 e o piloto da D4.3 devem conferi-las.

**Ciclo do stand com recarga de 30 min**

- **Serviços:** 27 + 65,8 + 26,7 + 1800 + 27 s, mais 124,6 s por passageiro embarcado.
- **Grupo médio:** 2,25 presentes por pedido.
- **Reserva de chegada:** 37,7 + 22,8 s.
- **Total:** cerca de 2290 s por ciclo, sem espera pelo grupo.
- **Capacidade:** perto de 7,9 voos/h com 5 stands e 6,3 voos/h com 4 stands.

**Carga do balcão (180 s por passageiro)**

| Pedidos/h | Passageiros/h | Ocupação do balcão | Ocupação dos 5 stands |
|---:|---:|---:|---:|
| 4 | 9 | 0,45 | 0,49 |
| 6 | 13,5 | 0,68 | 0,74 |
| 8 | 18 | 0,90 | 0,99 |

Na demanda alta, a configuração S4 fica acima da capacidade estimada. A inspeção (90 s) chega a no máximo 0,45. Essa folga é coerente com Feldhoff 2022, que não observou esperas na inspeção acima do limite em nenhum de seus nove cenários (p. 10). A autora atribui as esperas baixas nas estações seguintes ao atraso gerado pelo balcão, que fica antes delas. O contraste I2 pode, portanto, resultar pequeno, e esse também é um resultado. Já o B2 pode deslocar parte da espera para a inspeção.

## Construção do dia oferecido

**Horizonte e geração de pedidos**

- **Janela:** 8 h, no intervalo [0, 28.800 s), com recursos livres e filas vazias na abertura.
- **Pedidos:** processo de Poisson homogêneo entre 2700 s, inclusive, e o horizonte, exclusive. O início em 2700 s garante que a chegada mais antiga de um passageiro, 60 min antes da partida, não seja negativa em nenhuma família.
- **Contagem:** partidas e ocupação nas 8 h completas. Registrar a demanda realizada e a taxa nominal nas 7,25 h de oferta.

**Sequência comum de pedidos**

- Gerar os pedidos a 8/h e atribuir a cada um uma marca uniforme independente em [0,1).
- Conservar as marcas abaixo de 0,75 para 6/h e abaixo de 0,5 para 4/h.
- Preservar identificadores, horários, passageiros e durações dos pedidos comuns.
- Gerar um dia independente por réplica. Arquivar a semente, a configuração e o traço antes de aplicar as políticas.

**Partida programada (PAR-056)**

- STD = t + 900 s + recarga declarada.
- Vincular o alvo à recarga mantém constante, em todas as famílias, a folga entre a aeronave pronta e a partida. A pontualidade deixa de ser trivial com recarga de 60 min. Assim, a família de recarga mede o efeito da duração do ciclo sobre a capacidade, sem tornar todo voo atrasado por construção.
- Os 900 s são escolha dos autores.

**Manifesto e chegadas**

- **Reservas:** para cada pedido, sortear de 1 a 4 reservas equiprováveis para um destino comum (PAR-052).
- **Ausência:** por reserva, com probabilidade 0,10 (PAR-053).
- **Chegada de quem comparece:** em STD − U(900, 3600) s, ou seja, entre 60 e 15 min antes da partida programada (PAR-054).
  - **Fonte da janela:** Feldhoff 2022, p. 6. A fonte comprime a distribuição diurna da IATA em 15–60 min antes da STD.
  - **Forma: SUPOSTA.** A fonte modela a chegada por uma distribuição beta, mas não informa os parâmetros. Adota-se a uniforme como suposição declarada até que os parâmetros sejam obtidos.
- **Bagagem:** duração sorteada separadamente em U(30, 60) s (PAR-028).
- **Independência:** os sorteios são independentes, condicionados ao horário e à vinculação ao voo.

**Fechamento do manifesto (PAR-059)**

- O manifesto fecha em STD − 900 s, que coincide com o tmin da fonte. Todo passageiro que comparece chega até esse instante. A perda de voo vem apenas da ausência ou da recusa.
- Um grupo sem nenhum presente no fechamento cancela o pedido. Se a aeronave já tiver sido admitida, ela segue o ciclo e decola sem passageiros. Registrar esse caso separadamente.

**Percurso no terminal**

- Cada presente entra no balcão ao chegar e segue para bagagem e inspeção.
- Cada estação tem fila FCFS única, sem abandono e com espaço para todos.
- Quando há dois servidores, o passageiro da frente ocupa o primeiro servidor livre. Em empate, vai para o de menor índice.

**Retorno da aeronave**

- Um passageiro desembarca por aeronave admitida.
- A política recebe as reservas do pedido, a recarga declarada, o pedido de toque em t e a STD. A tolerância superior de pontualidade é de 60 s (PAR-049).

## Recusa e carga do terminal (PAR-062)

A recusa de um pedido é comunicada a todas as reservas no instante da decisão (t, na agenda):

- **Ainda não chegou:** não comparece.
- **Já está numa estação:** conclui o serviço em curso e deixa o terminal.
- **Está em fila:** deixa a fila no próprio instante.
- **Já concluiu a inspeção:** deixa a sala de espera.

Registrar cada saída com a estação e o instante. A espera desses passageiros fica censurada no instante da saída e é contada à parte.

O FCFS não recusa pedidos. Sua carga de terminal é a de todas as reservas presentes.

**Hipótese declarada, a confirmar pelo autor:** no FCFS, a aeronave sem recursos disponíveis aguarda no ar sem limite de tempo e sem desvio. Essa assimetria em relação à janela de 300 s da agenda será informada ao lado das pendências. Um limite de espera no ar pode ser acrescentado como sensibilidade.

## Recursos, admissão e sincronização

**Recursos comuns a todas as configurações**

- Um TLOF e uma rota bidirecional unitária.
- O mesmo tempo de táxi para todos os stands (SUPOSTO, como na versão 1).

**Recursos ligados ao stand (SUPOSTO)**

- Cada stand tem seu próprio carregador e seu próprio acesso de passageiros (gate).
- **Motivo:** a D2 trata stand e carregador como posição única (`phase_d_terminal_verification.json`). Com cinco posições, um carregador ou gate compartilhado introduziria um terceiro gargalo, alheio às perguntas deste experimento.
- **Limite da fonte:** Feldhoff 2022 não modela o lado ar. A topologia de 5 stands vem da Ref. [8] da fonte (Vascik e Hansman 2019, LIT-009). Ali, os 5 stands foram considerados os mais eficientes para turnaround de 300 s, muito menor que o ciclo deste estudo. Adota-se a topologia, não a conclusão sobre eficiência.

**Sequência no stand**

- Atribuir o stand livre de menor índice.
- A aeronave espera no próprio stand e recarrega após a saída do passageiro de chegada.
- Caminhada e embarque são individuais e sequenciais em cada stand.
- O rebocador é representado pelos tempos de manuseio e táxi, sem fila própria.

**FCFS**

- Cada recurso atende a solicitação elegível mais antiga.
- Para iniciar a chegada, verificar a disponibilidade conjunta de TLOF, rota e stand.
- Antes do retorno, reservar rota e TLOF. O stand é liberado na saída.
- Em empate, processar liberações antes das aquisições e usar o identificador crescente do voo ou passageiro.
- Registrar separadamente reserva, ocupação física e bloqueio.

**Agenda**

- Decidir em t. Procurar o primeiro toque viável no intervalo fechado [t, t + 300 s] (PAR-055), usando o calendário dos compromissos já admitidos e a sequência de serviço da D2.
- Reservar o stand de menor índice que permita esse toque. Recusar quando nenhum toque couber na janela.
- Permitir o planejamento além do horizonte para aplicar a mesma regra aos últimos pedidos.

**Previsão da prontidão do grupo na agenda**

- **Presentes:** usar o estado observado das filas e as durações declaradas. Para bagagem em curso, prever a duração restante pela média de U(30,60) condicionada ao tempo já decorrido. Para bagagem não iniciada, prever 45 s (PAR-058).
- **Reservas ainda não chegadas:** supor chegada no fechamento do manifesto (STD − 900 s), seguida das durações declaradas sem fila. É a previsão mais tardia compatível com a regra de fechamento.
- **Informação perfeita:** usar as chegadas e as durações de bagagem realizadas. As filas futuras continuam previstas pelo estado observado.
- **Restrição:** nenhuma decisão pode consultar a lista de pedidos futuros.

**Execução agendada**

- Respeitar a ordem dos compromissos por recurso, seus horários mínimos e as precedências físicas.
- Uma demora, inclusive a de um passageiro que fica pronto depois do previsto, propaga o início até a primeira disponibilidade conjunta.
- Preservar a admissão concedida. Registrar o toque fora da janela e atualizar o calendário dos compromissos restantes antes de avaliar outro pedido.
- A D4.2 deverá verificar uma propagação de atraso causada pelo grupo e a viabilidade das reservas simultâneas de rota e destino.

**Valores de serviço**

- **Sequência, unidades e durações físicas:** valores do [traço integrado da D2](../data/scenarios/phase_d_terminal_verification.json), com bagagem sorteada por pessoa e recarga fixada por família.
- **PAR-045 a PAR-049:** mantêm natureza sintética. O balcão de 180 s (PAR-046) também é sintético. O contraste B2 deve ser lido nessa condição.
- **Hipóteses comuns:** a ordem balcão, bagagem e inspeção e a autorização imediata de tripulação e despacho.
- **Lista completa de parâmetros experimentais:** está no [cadastro](../data/parameter_registry.csv).

## Onde cada mecanismo pode aparecer

A tabela usa a mesma notação do texto: t é o pedido, STD = t + 900 + R, e R é a recarga declarada.

| Mecanismo | Condição esperada | Famílias e contrastes |
|---|---|---|
| Fila por estação | Ocupação do balcão entre 0,45 e 0,90 | Todas. Os contrastes B2, I2 e de política mudam a espera |
| Retenção pelo grupo | Chegada tardia (até t + R) somada a cerca de 315 s de serviço e à fila. A aeronave fica pronta em torno de t + 180 s + R | Todas. Cresce com a fila do balcão, logo com a demanda, e cai em B2 |
| Bloqueio por estacionamento | Ocupação dos stands perto de 1 | Demanda alta e S4 |
| Efeito da informação | Agenda reserva o stand pela previsão mais tardia do grupo | Família de informação perfeita |

Essa tabela registra hipóteses de teste, não resultados. O sinal e a magnitude de cada efeito serão estimados nas réplicas.

## Observação e critério de passagem

**Fechamento no horizonte**

- Fechar os pedidos em cancelados, recusados, decolados ou pendentes de decolagem.
- Uma decolagem antes do horizonte conta mesmo que a separação termine depois.

**Estações do terminal**

- Por estação e configuração, contar visitas com início observado, esperas censuradas no horizonte e saídas por recusa.
- Informar espera média e P95.
- Informar a conformidade aos limites da D2 (PAR-026): 180 s no balcão e na inspeção. A bagagem não tem limite adotado.

**Grupo e aeronave**

- Registrar, por voo, o instante em que o último confirmado fica pronto e o instante em que a aeronave fica pronta para embarque.
- A retenção pelo grupo é o tempo em que a aeronave pronta aguarda passageiros.

**Percurso**

- Registrar o P95 da chegada ao início do embarque, quantos iniciaram embarque e o destino das demais reservas.

**Ocupação**

- Truncar os intervalos no horizonte e dividir pelo número de unidades vezes 8 h.

A especificação fecha os fatores, o pareamento, as regras de decisão e os denominadores. A evidência de execução virá na D4.2, com traços de disputa, recusa com saída do terminal, retenção pelo grupo, erro de previsão e corte no horizonte. O tamanho amostral depende do piloto da D4.3. Qualquer revisão posterior desta versão deverá indicar o motivo e as células afetadas.
