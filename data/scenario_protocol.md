# Protocolo de cenários (D2)

## Comparação principal

Comparar agendamento/reserva com FCFS de alocação local, usando a mesma topologia,
capacidade, solicitações, manifesto de passageiros, durações de serviço e condições
iniciais em cada réplica pareada. No caso agendado, a admissão depende de janelas e
recursos compatíveis. No FCFS, a posição na fila depende do instante de solicitação
ao recurso (LIT-004 fundamenta o benchmark; sua implementação é local). Conservar
o horário solicitado em ambas as políticas como referência para medir atraso.
Janelas, tolerâncias, realocação e desempate em igualdade de horário operacional
continuam pendentes (VAR-039). O cenário deve distinguir voo solicitado, admitido,
concluído e pendente no fim. As etapas do terminal são obrigatórias na Fase D.
Uma fase parcial serve à verificação incremental.

## Respostas propostas às perguntas do autor

1. **Formação do grupo.** Vincular cada reserva de assento individual a um identificador de
   voo e destino comum, com 1 a 4 passageiros. Passageiros do mesmo voo podem chegar em
   instantes distintos. A alocação por assento e horário tem precedente em operação
   de helicóptero (LIT-029), e o destino comum consta no cenário de Feldhoff e Soares
   Roque (LIT-010, §6.1). Usar o mesmo manifesto no agendamento e
   no FCFS de aeronaves isola o efeito da política de recursos. O perfil da quantidade
   de reservas por voo e a dependência entre chegadas ficam abertos (VAR-032).
2. **Assentos vazios, atraso e ausência.** Propor cenário em que, ao fechar o grupo, o voo
   elegível pode sair com os passageiros que estão prontos, desde que ao menos um esteja
   apto. A BLADE exige chegada 15 min antes e informa que o operador pode deixar de
   aguardar atrasados (LIT-028, §5). Os 15 min dizem respeito à **chegada**, não ao
   fechamento do embarque. A possibilidade de partir sem aguardar é evidência de
   mecanismo. A regra “ao menos um pronto” é proposta de cenário consistente com
   a fronteira de voos de passageiros, com aprovação pendente. O instante de fechamento,
   destino do passageiro perdido e tratamento do voo sem passageiros prontos continuam
   `undefined` (VAR-033). Distinguir assento nunca reservado, passageiro ausente e
   passageiro presente retido no atendimento. Cenários determinísticos de verificação
   podem forçar esses estados. As respectivas probabilidades permanecem `undefined`.
3. **Recarga.** Propor o stand para a configuração inicial da Fase C, com 30 min
   declarados, 60 min como sensibilidade no mesmo local e 0 min para a variante sem
   recarga local. Testar posição separada depois de definir o reposicionamento
   (VAR-038). O ConOps NUAIR/NASA descreve as duas configurações (LIT-008, §5.1.1.6.4).
   Os tempos adotados pelo autor são variantes de Preis (LIT-001, PAR-002).
4. **Sensibilidade de LoS.** O caso-base conserva balcão 180 s, quiosque 120 s e inspeção
   180 s (PAR-026). A comparação opcional e fundamentada usa a adaptação economia × 0,167
   de Feldhoff (2022, Tab. 6), na mesma ordem 200/20/100 s (PAR-031, proposta). O
   recálculo usa os mesmos tempos de fila, sem alterar a operação. Por estação, publicar
   o denominador, as esperas censuradas e a conformidade. Para bagagem, publicar a
   espera e manter a conformidade indefinida até haver limiar adequado (VAR-030).

## Verificação por fase

| Fase | Caso mínimo | Critério |
|---|---|---|
| A | Sem pedidos; um pedido; pedidos concorrentes; pedido no instante da liberação; separação positiva | Conservação, uma única ocupação física, atraso não negativo e liberação do próximo pedido no instante elegível |
| B | Sem stand livre; táxi ocupado; dois movimentos disputam um recurso | Nenhuma transferência usa recurso indisponível. Bloqueio e ocupação têm registro distinto. Retorno ao TLOF respeita a capacidade unitária |
| C | Mesma sequência com 0, 30 e 60 min; stand compartilhado | O cenário zero preserva o desembarque e o embarque quando representados. A recarga positiva bloqueia os recursos declarados e antecede presença de passageiros no embarque |
| D | Estação livre e ocupada; espera igual ao limite; grupo completo e incompleto; slot indisponível | O limite conta como conforme. Prontidão de embarque e prontidão de partida são eventos distintos. Verificar que cada passageiro concluiu as etapas exigidas |

Na Fase A, usar inicialmente traços sintéticos determinísticos e capacidade unitária.
Os instantes abaixo são valores de teste da especificação. Em cada linha, a duração
toque–saída é de 10 s para cada pedido. Nos empates, a ordem de entrada do traço
é usada para a verificação, com liberação processada antes de nova ocupação no
mesmo instante.

| Pedidos (s) | Separação após saída (s) | Toques esperados (s) | Saídas físicas esperadas (s) | Liberações esperadas (s) |
|---|---:|---|---|---|
| nenhum | 0 | nenhum | nenhum | nenhum |
| 0 | 0 | 0 | 10 | 10 |
| 0, 0 | 0 | 0, 10 | 10, 20 | 10, 20 |
| 0, 10 | 0 | 0, 10 | 10, 20 | 10, 20 |
| 0, 5 | 3 | 0, 13 | 10, 23 | 13, 26 |

A ocupação física termina na saída. A indisponibilidade pode incluir separação.
Na série saturada sem outros recursos, com serviço constante `s` e separação
constante `d`, os intervalos entre liberações são `s + d`. A taxa de verificação
é `3600 / (s + d)` liberações/h. A Fase A não gera uma estimativa de partidas/h do
vertiporto integrado. Os 99,2 s de PAR-001 têm fronteira diferente do serviço
físico de VAR-006; PAR-013 permanece candidato de movimento agregado.

### Execução da Fase A

Executar a partir da raiz do repositório com Python 3 e a biblioteca padrão.

```bash
python3 scripts/phase_a.py data/scenarios/phase_a_verification.json --policy scheduled
python3 scripts/phase_a.py data/scenarios/phase_a_verification.json --policy fcfs
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -v
```

A configuração versionada informa a base do cenário, o horizonte e a separação
em segundos. Cada pedido tem identificador, instante de solicitação, duração
toque–saída e janela de toque `[início, fim]` com extremos inclusivos. O recurso
começa livre e tem capacidade unitária (VAR-009). Todos os números da configuração
são sintéticos. A resolução de entrada é de milissegundos.

O agendamento processa as solicitações na ordem de chegada e busca o primeiro
intervalo livre que comporte a ocupação e a separação, com toque dentro da janela.
Uma janela inviável gera rejeição no instante da solicitação. O FCFS usa a mesma
lista de pedidos e durações e aloca o TLOF pela ordem da solicitação, sem impor a
janela de reserva. Empates usam a ordem de entrada. Essas regras implementam a
verificação da Fase A. A política operacional integrada continua em VAR-039.

A saída JSON inclui os dados de entrada, a alocação planejada, o log cronológico
e o resumo. Entradas, eventos e liberações observadas pertencem à janela
`[0, horizonte)`. A situação de cada pedido é apurada imediatamente antes do
fechamento. Ocupação e separação são recortadas na janela. O atraso médio de
acesso inclui apenas pedidos que chegaram ao toque dentro da observação.
Interpretá-lo junto com o número de toques, rejeições e pendências.

| Execução sintética | Pedidos | Aceitos | Rejeitados | Liberações na janela | Em ocupação no fechamento | Ocupação física |
|---|---:|---:|---:|---:|---:|---:|
| Agendamento | 4 | 3 | 1 | 2 | 1 | 72,5% |
| FCFS | 4 | 4 | 0 | 3 | 1 | 77,5% |

Os valores exercitam conflito, rejeição e censura no horizonte. A comparação
de desempenho exige um experimento com demanda, durações e janelas fundamentadas.

## Experimento integrado e regras de interpretação

- **Fatores.** Demanda, capacidade dos recursos, recarga e política de coordenação.
  Comparar políticas com capacidade fixa; medir gargalos alterando um recurso por
  vez com demanda fixa. Comparar a rede acoplada com submodelos parciais apenas
  para diagnosticar mecanismos. O intervalo de 5 a 30 aeronaves/h (PAR-014,
  LIT-006) é faixa de outro estudo, disponível para triagem. A demanda final e o
  processo de chegada precisam ser definidos por cenário, inclusive a relação
  entre fluxo de aeronaves e passageiros (VAR-001, VAR-002 e VAR-032).
- **Horizonte.** A proposta é simulação terminante de uma janela operacional.
  Fixar o período de admissão, condição inicial e regra de encerramento antes de
  rodar. Medir throughput na janela declarada e reportar pendências na fronteira.
  Se houver drenagem após encerrar admissões, reportá-la separadamente para
  completar o seguimento da coorte. O aquecimento é dispensável para o cenário
  terminante quando o estado inicial representa a abertura em estudo.
  Para eventual regime permanente, determinar aquecimento após piloto (LIT-032,
  §§3 e 5). O valor do horizonte segue `undefined` (VAR-035).
- **Replicações.** Usar réplicas independentes e parear a mesma realização de
  demanda e de durações nas duas políticas. Registrar sementes e mecanismo de
  geração por réplica e fonte de aleatoriedade. Comparar diferenças por réplica
  com intervalo de confiança, incluindo incerteza das médias e das medidas de
  cauda relevantes. Quando a resposta for P95, calcular o P95 de cada réplica
  e comparar essas estatísticas entre políticas. Estimar a precisão no piloto
  antes de fixar o número de réplicas e as sementes das rodadas finais (LIT-032, §§2, 4 e 6; VAR-036/037).
- **Métricas.** Por fase, definir a população e o evento de saída. Reportar
  throughput, utilização, bloqueio e atraso airside. Na Fase D, acrescentar
  espera de fila por estação, tempo até embarque, P95, conformidade de LoS nos
  postos com limiar e passageiros que não embarcaram. Manter pendências e
  censura visíveis. Pontualidade por tolerância depende de valor declarado (VAR-040).
- **Ordem bagagem–inspeção.** A checagem de bagagem de mão de PAR-028 é
  uma estação distinta do raio X da inspeção. As fontes
  de Tarefa 01 não estabelecem a precedência entre as duas etapas distintas.
  Verificar cada ordem como traço de modelagem, sem tratá-las como políticas
  observadas. VAR-034 continua `undefined` para a configuração experimental.

## Cenário adotado para a ocupação do TLOF e a rota de táxi

**VAR-006, toque até saída física do TLOF.** As fontes examinadas dão
componentes, sem um valor total transferível. A proposta para análise por
cenários é calcular `T_preparação + L_TLOF / v`. `L_TLOF` é a distância
percorrida desde o ponto de toque até a posição em que a aeronave libera
fisicamente o TLOF. `T_preparação` inclui apenas atividades efetivamente
realizadas após o toque e antes do movimento. No táxi rebocado, Preis e Hornung
(LIT-003, Tabs. 3 e A1) dão 5 s de desligamento de motores e 27 s de acoplamento
como estimativas separadas. Se ambas forem sequenciais no TLOF, a soma é 32 s
de atividades identificadas. Outras checagens ou esperas permanecem explícitas
e fora dessa soma. A desconexão realizada no stand pertence ao stand, e a
separação pós-saída pertence a VAR-031. Os 99,2 s de PAR-001 continuam como
referência agregada.

**VAR-041, da saída física do TLOF até a entrada no stand.** Para a duração
de deslocamento, usar `L_rota / v`, seguindo Wille (LIT-034, §3.1). Definir
`L_rota` ao longo do trajeto, com o limite da VAR-006 como ponto inicial na
chegada. Aplicar a definição correspondente no retorno. Para a rota
bidirecional unitária, a proposta é reservar rota e destino antes de iniciar
a transferência, registrar a ocupação física desde a entrada na rota e
liberá-la quando a aeronave a desocupar por completo. O mesmo caminho fica
indisponível aos movimentos opostos enquanto estiver reservado ou ocupado.
Medir espera pelo destino separadamente do tempo de movimento. A política é
uma adaptação de modelagem da aquisição e liberação de recursos de Wille
(LIT-034, §3.2, Fig. 4).

Exemplo de sensibilidade para discussão, com distâncias ilustrativas de
15 m dentro do TLOF e 60 m na rota. São distâncias hipotéticas de cálculo,
sem dimensionamento regulatório e sem adotar um D para Eve ou Joby.

| Referência de velocidade | Velocidade (m/s) | Movimento dentro do TLOF (s) | Movimento na rota (s) |
|---|---:|---:|---:|
| Prática de helipontos (PAR-039) | 1,22 | 12,3 | 49,2 |
| Hipótese de Wille (PAR-040) | 1,80 | 8,3 | 33,3 |
| Táxi ativo de Preis e Hornung (PAR-035) | 2,15 | 7,0 | 27,9 |
| Táxi rebocado de Preis e Hornung (PAR-036) | 2,63 | 5,7 | 22,8 |

Em 19/11/2026, o autor aprovou o cenário rebocado, com os 15 m dentro do
TLOF e 60 m na rota. As entradas do cenário são 37,7 s para VAR-006
(PAR-043) e 22,8 s por trecho para VAR-041 (PAR-044). Os valores são
arredondados a 0,1 s. Adota-se a regra de aquisição e liberação descrita
acima para a rota compartilhada de capacidade unitária. A desconexão no
stand continua pertencendo ao atendimento no stand. Os valores da tabela
são cálculos condicionais e não constituem calibração de Eve ou Joby.

### Execução da Fase B

```bash
python3 scripts/phase_b.py data/scenarios/phase_b_towed_verification.json --policy scheduled
python3 scripts/phase_b.py data/scenarios/phase_b_towed_verification.json --policy fcfs
```

O traço começa com todos os recursos livres. A admissão no toque exige
TLOF, rota e o único stand disponíveis. A saída do TLOF inicia o táxi de
chegada e a entrada no stand libera a rota. Após o atendimento no stand, a
aeronave pode aguardar a disponibilidade do TLOF. O retorno reserva a
rota e o TLOF, começa quando termina a separação de chegada e o stand está
pronto, e libera o stand na saída. O fim do ciclo é a liberação do TLOF
após a separação de partida. A simulação registra intervalos de reserva,
ocupação e separação dentro da janela `[0, horizonte)`, além dos tempos
planejados e dos estados dos pedidos.

O traço usa os dois tempos aprovados. Horários de pedido, janelas,
separações, 40 s de serviço agregado de stand e 10 s de ocupação de TLOF
na partida são entradas sintéticas de verificação. No traço de três
pedidos, o agendamento tem um ciclo liberado, um pedido recusado e um
ciclo em andamento. O FCFS tem um ciclo liberado, um em andamento e um
pedido em espera. Isso verifica transições e exclusão mútua na topologia
unitária. Os resultados são de um traço determinístico de teste.

## Critérios para fechar a D2 operacional

A Fase A foi executada e verificada com cenários sintéticos. Para calibrar a duração
de ocupação física, é preciso um registro com o primeiro contato no TLOF e o
instante em que a aeronave deixa a posição, incluindo o modo de movimentação em
solo aplicável. A separação posterior é medida à parte. Um tempo que inclui
aproximação, segurança de espaçamento ou táxi até o stand exige decomposição com
eventos identificáveis para alimentar VAR-006.

A Fase B tem cenário de duração e regra de aquisição/liberação da rota
(VAR-041) e foi verificada para a topologia unitária. Seus tempos de teste
de stand e de partida precisam ser substituídos por entradas fundamentadas
ao avaliar operações integradas. Para executar todas as variantes da Fase C, faltam as
entradas de reposicionamento. Para a Fase D, as fontes registradas para check-in
e inspeção são candidatas de transferência (PAR-030/032/033), e os parâmetros
o traço D fixa VAR-004 e VAR-005 em PAR-046 e PAR-047. Antes da rodada integrada, revalidar
somente entradas e cenários ativos e congelar a configuração completa da execução.

### Execução da Fase C no stand

```bash
python3 scripts/phase_c.py data/scenarios/phase_c_stand_verification.json --policy scheduled
python3 scripts/phase_c.py data/scenarios/phase_c_stand_verification.json --policy fcfs
python3 -m unittest discover -s scripts
```

Cada pedido declara a duração da recarga antes da alocação. O tempo agregado de
40 s da Fase B dá lugar à sequência de desacoplar o rebocador, desembarcar,
sair até a porta do terminal, recarregar quando previsto, entrar a partir da
porta, embarcar e acoplar o rebocador. O cenário identifica o parâmetro de cada
etapa em `service_basis`. Há um passageiro em cada sentido. A porta representa
a fronteira de saída da área operacional neste teste. Tripulação, gate e passageiro
de partida estão disponíveis quando termina o serviço precedente. As etapas são
sequenciais. O stand fica ocupado até a saída para o táxi de partida.

O mesmo traço contém pedidos de 30, 0 e 60 min, para testar a declaração por
voo. No primeiro pedido, a recarga ocorre de 180 a 1.980 s e o TLOF é liberado
em 2.175,5 s. O intervalo observado de cada recurso termina no máximo no
horizonte de 6.000 s. Os horários planejados preservam o restante do ciclo.
A ocupação agregada de partida de 50 s é sintética. O equipamento de reboque
é tratado pelos tempos de manuseio, sem fila própria. A posição de recarga
separada permanece dependente de VAR-038.

A [busca de registros operacionais para calibração](search_log.md#busca-dirigida-de-dados-operacionais-para-as-fases-ac--19-de-novembro-de-2026) documenta os marcos da NASA, as observações de recarga em aeronave elétrica de asa fixa, o exercício brasileiro com helicóptero, os dados de voos e as restrições regulamentares, com o uso permitido por seus recortes.

### Execução da fase D e medição de partida

```bash
python3 scripts/phase_d.py data/scenarios/phase_d_terminal_verification.json --policy scheduled
python3 scripts/phase_d.py data/scenarios/phase_d_terminal_verification.json --policy fcfs
python3 -m unittest discover -s scripts
```

O exemplo tem quatro pedidos de aeronave e sete reservas individuais. O
manifesto fecha no instante do pedido. Presença no terminal até o fechamento
(inclusive) confirma o assento. Ausentes e atrasados perdem o voo. Um grupo
vazio cancela o pedido antes de adquirir o TLOF. Cada confirmado só acessa
o embarque após concluir as três estações. A aeronave aguarda, se necessário.
Essas regras são hipóteses dos autores para o traço. Um passageiro desembarca
por aeronave admitida. Cada embarque de partida usa caminhada, acesso ao gate
e embarque individuais, em série. A autorização de tripulação e despacho é
imediata. A única janela reservada no exemplo é a de chegada.

O terminal processa os confirmados em ambas as políticas, inclusive os que
recebem recusa do pedido de aeronave. O traço pressupõe atendimento mantido
até a comunicação do resultado. A agenda conhece os tempos determinísticos
de processamento para dimensionar cada reserva. A fila é FCFS por estação,
com desempate por ID de passageiro. Os valores de bagagem do manifesto são
realizações fixadas dentro de U(30,60) de PAR-028. Todos os recursos começam
livres. As filas comportam todo o manifesto. Os valores por voo e passageiro
estão no JSON versionado. PAR-045 a PAR-049 identificam as novas constantes.

O relatório identifica visitas às estações, filas censuradas, conformidade
por estação, ocupação por recurso, situação do manifesto e marcos da partida.
O P95 usa posto de ordem superior sobre tempos chegada–início do embarque
observados. A utilização divide a ocupação física pelo horizonte. A razão de
pontualidade pode ser calculada dividindo as partidas dentro da tolerância
pelas decolagens observadas. O exemplo verifica a implementação. Inferência
sobre diferenças entre políticas requer cenários e réplicas apropriados.
