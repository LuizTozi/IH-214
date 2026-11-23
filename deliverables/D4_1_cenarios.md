# D4.1 — Especificação do experimento integrado, versão 1

Versão de trabalho para revisão em 23/11/2026. As hipóteses e a matriz abaixo documentam as propostas da D4.1. A redação do desenho experimental do artigo ocorrerá após a conclusão integral da D4. A unidade de comparação é uma janela operacional sintética. A pergunta é quanto mudam as decolagens por hora, a cobertura da demanda oferecida e as esperas dos passageiros quando se altera a admissão ou se acrescenta uma posição de estacionamento. As escolhas numéricas abaixo servem para construir contrastes reproduzíveis. O piloto avaliará a precisão e a adequação da faixa de carga.

## Matriz para cada réplica

| Família | Pedidos/h no período de oferta | Recarga por voo | Previsão da bagagem |
|---|---:|---:|---|
| Referência | 2 | 30 min | 45 s |
| Demanda baixa | 1 | 30 min | 45 s |
| Demanda alta | 4 | 30 min | 45 s |
| Sem recarga local | 2 | 0 min | 45 s |
| Recarga longa | 2 | 60 min | 45 s |
| Informação perfeita sobre a duração da bagagem | 2 | 30 min | duração individual realizada |

Cada linha contém quatro células, agendamento ou FCFS local com um ou dois stands. As cinco primeiras famílias geram 20 células. A última acrescenta duas execuções de agendamento. Seus dois controles FCFS são os da referência, pois o FCFS usa apenas eventos realizados. São 22 execuções distintas por réplica. A comparação de informação isola a incerteza na duração do serviço de bagagem. Pedidos futuros permanecem desconhecidos em todas as células.

A faixa de demanda foi escolhida em torno de uma referência física simples. Um carregador continuamente ocupado por sessões de 30 min pode terminar duas sessões por hora. Isso orienta a escolha de 1, 2 e 4 pedidos oferecidos/h. A vazão de decolagens dependerá também de cancelamentos, das demais etapas e do fechamento da janela.

## Construção do dia oferecido

- Horizonte de 8 h, intervalo [0, 28.800 s), recursos livres e filas vazias na abertura. Gerar pedidos por processo de Poisson homogêneo entre 900 s inclusive e o horizonte exclusivo. Os 15 min iniciais permitem chegadas de passageiros antes do primeiro pedido. Contar partidas e ocupação nas 8 h completas. Registrar a demanda realizada e a taxa nominal nas 7,75 h de oferta.
- Gerar primeiro os pedidos a 4/h. Atribuir a cada um uma marca uniforme independente em [0,1). Conservar marcas abaixo de 0,5 para 2/h e abaixo de 0,25 para 1/h. Preservar identificadores, horários, passageiros e durações dos pedidos comuns. Gerar um dia independente por réplica e arquivar a semente, a configuração e o traço antes de aplicar as políticas.
- Para cada pedido no instante t, sortear de 1 a 4 reservas equiprováveis para um destino comum. Por reserva, sortear ausência com probabilidade 0,10. Para quem comparece, sortear chegada uniforme contínua entre t menos 900 s e t mais 60 s. Sortear separadamente a duração da bagagem em U(30,60) s. Os sorteios são independentes, condicionados ao horário e à vinculação ao voo. Esses valores são hipóteses do experimento.
- O manifesto fecha em t. Presença até t inclusive confirma o assento. Ausência e chegada posterior encerram a reserva sem reacomodação. Um grupo vazio cancela o pedido antes da alocação. Cada presente entra no balcão ao chegar e segue para bagagem e inspeção. Cada estação tem um servidor, fila FCFS sem abandono e espaço para todo o manifesto. Uma recusa é comunicada aos confirmados na saída da inspeção ou imediatamente em t para quem já concluiu a estação. Até a comunicação, todos seguem o mesmo percurso. O instante individual é o maior entre t e o fim da inspeção.
- Um passageiro desembarca por aeronave admitida. A política recebe o mesmo grupo confirmado, a recarga declarada, o pedido de toque em t e o alvo de decolagem em t mais 45 min. Esse alvo fixo permite medir também a exposição da pontualidade a uma recarga mais longa. A tolerância superior é de 60 s.

## Recursos, admissão e sincronização

Um TLOF, uma rota bidirecional unitária, um gate e um carregador atendem as duas configurações. Apenas a quantidade de stands muda. As duas posições têm o mesmo tempo de táxi. O carregador atende qualquer posição sem tempo de transferência. A aeronave espera no próprio stand, solicita o carregador após a saída do passageiro de chegada e o libera ao fim da recarga. Recarga zero dispensa essa solicitação. Atribuir o stand livre de menor índice em caso de empate. Manter o gate compartilhado e exclusivo nos intervalos de passagem de entrada e saída. Caminhada e embarque são individuais e sequenciais para cada aeronave. O rebocador é representado pelos tempos de manuseio e táxi, sem fila própria.

Em FCFS, cada recurso atende a solicitação elegível mais antiga. Para iniciar a chegada, verificar disponibilidade conjunta de TLOF, rota e stand. Antes do retorno, reservar rota e TLOF; o stand é liberado na saída. Em empate, processar liberações antes das aquisições e usar o identificador crescente do voo ou passageiro. Registrar separadamente reserva, ocupação física e bloqueio.

Na agenda, decidir em t. Procurar o primeiro toque viável no intervalo fechado [t, t + 300 s], usando o calendário de compromissos já admitidos, os recursos acima e a sequência de serviço da D2. Reservar a sequência prevista com o primeiro stand que permita esse toque. Recusar quando nenhum toque couber na janela. Permitir o planejamento além do horizonte para aplicar a mesma regra aos últimos pedidos. Na previsão, usar o estado observado das filas, os presentes conhecidos e as durações declaradas. Para bagagem em curso, prever duração restante pela média de U(30,60) condicionada ao tempo já decorrido. Na variante de informação perfeita, usar a duração individual efetiva. Nenhuma decisão pode consultar a lista de pedidos ou chegadas futuras.

Durante a execução agendada, respeitar a ordem dos compromissos por recurso, seus horários mínimos e as precedências físicas. Uma demora propaga o início até a primeira disponibilidade conjunta. Preservar a admissão concedida, registrar o toque fora da janela e atualizar o calendário dos compromissos restantes antes de avaliar outro pedido. A D4.2 deverá verificar uma propagação de atraso e a viabilidade das reservas simultâneas de rota e destino.

Para a sequência, unidades e durações físicas, adotar os valores de serviço do [traço integrado da D2](../data/scenarios/phase_d_terminal_verification.json), com bagagem sorteada por pessoa e recarga fixada por família. Os tempos PAR-045 a PAR-049 conservam natureza sintética. A ordem balcão, bagagem e inspeção e a autorização imediata de tripulação e despacho são hipóteses comuns. A lista de parâmetros experimentais está no [cadastro](../data/parameter_registry.csv).

## Observação e critério de passagem

No horizonte, fechar pedidos em cancelados, recusados, decolados ou pendentes de decolagem. Uma decolagem antes do horizonte conta mesmo que a separação termine depois. Para as estações, contar visitas com início observado e esperas censuradas. Para o percurso, registrar o P95 chegada–início do embarque, quantos iniciaram embarque e o destino das demais reservas. Na ocupação, truncar intervalos no horizonte e dividir pelo número de unidades vezes 8 h. Os contrastes principais são agenda menos FCFS com stands fixos, e dois menos um stand sob política fixa.

A especificação fecha os fatores, o pareamento, as regras de decisão e os denominadores. A evidência de execução virá na D4.2 com traços de disputa, recusa, erro de previsão e corte no horizonte. O tamanho amostral depende do piloto da D4.3. Qualquer revisão posterior desta versão deverá indicar o motivo e as células afetadas.
