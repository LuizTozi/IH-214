# D4.2 — Registro de verificação

A revisão v2.4 passou em 76 testes e reproduziu integralmente 30 dias. A descrição abaixo documenta a verificação original.

Concluída em 23/11/2026, sobre a especificação D4.1 v2.1. Ambiente Conda `ih214` (`environment.yml`: Python 3.12, SimPy 4.1.2). Para reproduzir:

```bash
conda activate ih214
cd scripts && python -m unittest -v
```

São 60 testes: 26 das fases A a D e do gerador, e 34 da D4.2. Os instantes esperados nos casos montados à mão foram calculados antes da execução, com os valores de `scripts/d4_param.py`.

## Módulos

| Módulo | Papel |
|---|---|
| `scripts/d4_dia.py` | Gera o dia oferecido antes da política (pedidos, marcas, reservas, chegadas, bagagem) |
| `scripts/d4_terminal.py` | Estações com 1 ou 2 servidores; saída por recusa ou desvio; sala de espera por voo; previsão de prontidão |
| `scripts/d4_param.py` | Durações do lado ar e regras, com a procedência PAR-0xx |
| `scripts/d4_sim.py` | Lado ar (TLOF, rota, N stands), FCFS com desvio, execução agendada e métricas da célula |
| `scripts/d4_agenda.py` | Calendário, previsão do grupo, busca do toque e do stand, recusa |
| `scripts/d4_experimento.py` | 48 células por réplica, com uma linha por célula, versão do código, semente e identificador do dia |

## Exigências da D4.2 e onde são verificadas

| Exigência (plano e especificação) | Teste |
|---|---|
| Sorteios antes da política e vinculados ao pedido; afinamento aninhado | `test_d4_dia`: afinamento aninhado, horários da família |
| Durações do ciclo iguais às conferidas na D4.1 | `test_d4_sim`: voo isolado (279,8 + R + 124,6n) e intervalos físicos |
| Disputa de recurso | Rota espaçando chegadas (60,5 s); partida bloqueada por chegada na rota (50,5 s); stand ocupado levando a desvio |
| Desvio no FCFS (janela inclusiva) | Toque permitido em t + 300 s; desvio em t + 300,1 s |
| Recusa com saída do terminal | `test_d4_terminal` (na fila, em atendimento, antes de chegar, na sala de espera); recusa da agenda no instante da decisão |
| Retenção pelo grupo | Aeronave pronta em t + 180 s espera 135 s pelo passageiro |
| Erro de previsão | Bagagem de 60 s contra 45 s previstos: saída 15 s após o plano; informação perfeita sem desvio do plano |
| Previsão pessimista e valor da informação | Espera de 135 s até a saída planejada; nula com informação perfeita |
| Reserva da partida pela agenda | Toque adiado para 3075,8 s para não sobrepor a partida anterior |
| Decisão sem informação futura | Plano de A igual com e sem pedido posterior |
| Corte no horizonte | Voo pendente no horizonte; espera censurada no terminal |
| Balanço dos pedidos | Cancelados + recusados + desviados + decolados + pendentes = oferecidos (dia gerado e 48 células) |
| Capacidade física | TLOF, rota e stands sem sobreposição; TLOF sem uso durante a separação; servidores nunca excedidos |
| Ordem dos eventos de embarque | Início do embarque ≥ prontidão + 51,6 s; embarques do voo espaçados ≥ 124,6 s |
| Espera por estação igual entre Base e S4 sem recusas nem desvios | Casos montados à mão e verificação nas 48 células |
| Pareamento | Um único dia por réplica em todas as células; mesma demanda dentro da família |

## Constatações da verificação

1. **Ocupação do balcão.** Na configuração Base, ela reproduz a estimativa da especificação, descontados os 2,3% de passageiros que chegam após o horizonte e o acaso das sementes.
2. **Reserva da partida.** A agenda pode adiar um toque dentro da janela para não sobrepor partidas. O FCFS deixaria a aeronave pousar e esperar na partida.
3. **Erro de previsão.** Com janela de 300 s, um erro de previsão da bagagem se resolve pelo menos 241,6 s antes da saída do stand. Decisões posteriores já o conhecem. O erro atrasa o próprio voo, mas dificilmente se propaga a voos decididos depois.
4. **Execução agendada.** A interpretação está registrada na especificação, para revisão do autor: horários mínimos de toque e de saída, com prioridade pelo horário planejado.

## Limites

- A verificação confere a implementação contra a especificação. Ela não valida tempos empíricos nem estima efeitos.
- Nenhum contraste entre políticas ou configurações foi calculado. As réplicas e o dimensionamento pertencem à D4.3.
- A forma da distribuição de chegada continua SUPOSTA (uniforme), porque os parâmetros da beta de Feldhoff 2022 não foram encontrados.
