# D4.6 — Traço de eventos: chegada bloqueada por falta de stand

Dia `dia_20001.json` (semente 20001), família de referência, FCFS. Pedido **R0014** em t = 10424.658 s; janela de toque até t + 300 s = 10724.658 s.
Gerado por `scripts/d4_traco.py`; tempos em segundos desde a abertura.

## S4 (4 stands): R0014 → diverted

| Stand | Voo que ocupa | Toque | Pronto para partir | Saída do stand |
|---:|---|---:|---:|---:|
| 1 | R0011 | 9941.152 | 12197.352 | 12197.352 |
| 2 | R0013 | 10329.913 | 12461.513 | 12461.513 |
| 3 | R0010 | 8979.952 | 11360.752 | 11360.752 |
| 4 | R0012 | 10070.094 | 12326.294 | 12326.294 |

Todos os stands seguem ocupados até 10724.658 s; a aeronave desvia em 10724.658 s e os passageiros do voo são avisados nesse instante.

## Base (5 stands): R0014 → departed

| Stand | Voo que ocupa | Toque | Pronto para partir | Saída do stand |
|---:|---|---:|---:|---:|
| 1 | R0011 | 9941.152 | 12197.352 | 12197.352 |
| 2 | R0013 | 10329.913 | 12461.513 | 12461.513 |
| 3 | R0010 | 8979.952 | 11360.752 | 11360.752 |
| 4 | R0012 | 10070.094 | 12326.294 | 12326.294 |
| 5 | R0014 **(este pedido)** | 10424.658 | 12556.258 | 12559.313 |

Toque em 10424.658 s no stand 5; decolagem em 12627.113 s, com 1 passageiro(s).

Mecanismo: com 4 stands, os ciclos com recarga de 30 min mantêm todas as posições ocupadas durante a janela de 300 s; o quinto stand absorve o pedido. É o bloqueio de chegada por estacionamento cheio discutido por Onat et al. (D001), aqui medido no cenário sintético.
