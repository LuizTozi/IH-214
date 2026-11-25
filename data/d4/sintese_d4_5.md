# D4.5 — Síntese reproduzível dos contrastes (D4.1 v2.2)

Fonte: `../data/d4/resultados_d4_4.csv`. Analisador: `d2df0b1`. Cada estimativa usa as réplicas
independentes válidas; as diferenças são calculadas dentro da réplica e resumidas por
média e intervalo t bilateral de 95%. Proporções são médias das razões por réplica.
Todos os números desta síntese vêm de `resumo_celulas_d4_5.csv` e
`contrastes_d4_5.csv`.

## Contrastes principais na família de referência

| Contraste (sentido) | Política | Média [IC 95%] | Unidade |
|---|---|---:|---|
| Agenda − FCFS, Base | — | -0.033 [-0.066; -0.001] | decolagens com passageiros/h |
| Base − S4 | FCFS | 0.487 [0.439; 0.536] | decolagens com passageiros/h |
| Base − S4 | Agenda | 0.492 [0.440; 0.544] | decolagens com passageiros/h |
| B2 − Base | FCFS | -141.5 [-158.4; -124.7] | s |
| B2 − Base | Agenda | -125.3 [-140.5; -110.1] | s |

## Balanço e mecanismos por demanda na configuração-base

| Indicador por réplica | Política | 4 pedidos/h | 6 pedidos/h | 8 pedidos/h |
|---|---|---:|---:|---:|
| Pedidos oferecidos | FCFS | 28.70 [26.90; 30.50] | 43.77 [41.48; 46.05] | 57.97 [55.09; 60.84] |
| Pedidos oferecidos | Agenda | 28.70 [26.90; 30.50] | 43.77 [41.48; 46.05] | 57.97 [55.09; 60.84] |
| Recusados | FCFS | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] |
| Recusados | Agenda | 1.80 [1.23; 2.37] | 7.23 [6.01; 8.46] | 14.63 [12.74; 16.53] |
| Desviados | FCFS | 1.60 [1.08; 2.12] | 6.77 [5.67; 7.87] | 14.23 [12.42; 16.05] |
| Desviados | Agenda | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] |
| Decolados com passageiros (vazios à parte) | FCFS | 3.042 [2.866; 3.218] | 4.112 [3.949; 4.276] | 4.800 [4.640; 4.960] |
| Decolados com passageiros (vazios à parte) | Agenda | 3.017 [2.841; 3.192] | 4.079 [3.922; 4.236] | 4.763 [4.611; 4.914] |
| Decolagens vazias | FCFS | 0.53 [0.26; 0.81] | 0.87 [0.59; 1.14] | 1.10 [0.72; 1.48] |
| Decolagens vazias | Agenda | 0.53 [0.26; 0.81] | 0.83 [0.55; 1.11] | 1.13 [0.74; 1.52] |
| Pendentes no horizonte | FCFS | 2.23 [1.71; 2.76] | 3.23 [2.66; 3.80] | 4.23 [3.75; 4.72] |
| Pendentes no horizonte | Agenda | 2.23 [1.74; 2.73] | 3.07 [2.51; 3.62] | 4.10 [3.67; 4.53] |
| Cobertura dos oferecidos | FCFS | 0.852 [0.829; 0.874] | 0.757 [0.734; 0.781] | 0.669 [0.643; 0.694] |
| Cobertura dos oferecidos | Agenda | 0.845 [0.821; 0.868] | 0.752 [0.728; 0.776] | 0.664 [0.638; 0.690] |
| Espera média no balcão (s) | FCFS | 94.8 [76.7; 112.9] | 154.8 [136.6; 173.0] | 222.2 [194.6; 249.9] |
| Espera média no balcão (s) | Agenda | 89.6 [73.0; 106.3] | 137.7 [121.4; 154.0] | 186.4 [165.6; 207.2] |
| Conformidade ao limite do balcão (180 s) | FCFS | 0.805 [0.768; 0.843] | 0.677 [0.639; 0.715] | 0.563 [0.522; 0.604] |
| Conformidade ao limite do balcão (180 s) | Agenda | 0.814 [0.779; 0.850] | 0.701 [0.664; 0.738] | 0.611 [0.570; 0.652] |
| Fração retida pelo grupo | FCFS | 0.052 [0.034; 0.069] | 0.092 [0.070; 0.113] | 0.127 [0.100; 0.154] |
| Fração retida pelo grupo | Agenda | 0.048 [0.031; 0.065] | 0.079 [0.061; 0.096] | 0.098 [0.074; 0.122] |
| Espera após a inspeção, média (s) | FCFS | 1289.9 [1250.1; 1329.6] | 1255.5 [1217.7; 1293.3] | 1201.9 [1160.0; 1243.8] |
| Espera após a inspeção, média (s) | Agenda | 1302.6 [1263.4; 1341.7] | 1283.5 [1247.3; 1319.7] | 1245.8 [1204.0; 1287.6] |
| Bloqueio do stand após prontidão (s) | FCFS | 4.2 [2.8; 5.7] | 8.0 [6.3; 9.6] | 9.7 [8.2; 11.3] |
| Bloqueio do stand após prontidão (s) | Agenda | 1.5 [0.9; 2.2] | 2.4 [1.4; 3.5] | 2.4 [1.9; 3.0] |

A linha de decolados com passageiros está em decolagens/h (VAR-016).

## Terminal: Base e B2 na referência

| Indicador por réplica | Base FCFS | B2 FCFS | Base agenda | B2 agenda |
|---|---:|---:|---:|---:|
| Espera média no balcão (s) | 154.8 [136.6; 173.0] | 13.3 [11.2; 15.3] | 137.7 [121.4; 154.0] | 12.4 [10.5; 14.3] |
| P95 da espera no balcão (s) | 558.1 [502.5; 613.7] | 102.5 [88.0; 117.1] | 503.6 [446.3; 561.0] | 95.7 [82.7; 108.7] |
| Conformidade ao limite do balcão | 0.677 [0.639; 0.715] | 0.992 [0.987; 0.996] | 0.701 [0.664; 0.738] | 0.992 [0.989; 0.996] |
| Espera média na bagagem (s) | 0.0 [0.0; 0.0] | 2.4 [2.1; 2.7] | 0.0 [0.0; 0.0] | 2.4 [2.1; 2.7] |
| Espera média na inspeção (s) | 0.0 [0.0; 0.0] | 8.0 [7.4; 8.5] | 0.0 [0.0; 0.0] | 7.6 [7.1; 8.1] |
| Espera após a inspeção, média (s) | 1255.5 [1217.7; 1293.3] | 1380.2 [1349.1; 1411.4] | 1283.5 [1247.3; 1319.7] | 1396.3 [1365.5; 1427.1] |
| Espera após a inspeção, P95 (s) | 2420.4 [2388.0; 2452.8] | 2493.4 [2469.0; 2517.9] | 2438.1 [2407.0; 2469.2] | 2500.8 [2474.4; 2527.2] |
| Fração retida pelo grupo | 0.092 [0.070; 0.113] | 0.023 [0.014; 0.033] | 0.079 [0.061; 0.096] | 0.018 [0.011; 0.025] |

Contrastes pareados B2 − Base (exploratórios): conformidade ao limite do balcão 0.315 [0.277; 0.353] (FCFS) e 0.291 [0.254; 0.328] (agenda); espera média após a inspeção 124.7 [107.9; 141.5] s (FCFS) e 112.7 [98.3; 127.1] s (agenda).

Denominadores totais (30 réplicas): espera no balcão Base FCFS 2.529, B2 FCFS 2.608, Base agenda 2.468, B2 agenda 2.541; voos com passageiros Base FCFS 987, B2 FCFS 998, Base agenda 979, B2 agenda 986.

## Sensibilidade do contraste de política na Base (exploratória)

| Família | Agenda − FCFS, decolagens com passageiros/h: média [IC 95%] |
|---|---:|
| 4 pedidos/h | -0.025 [-0.044; -0.006] |
| 6 pedidos/h, recarga 30 min (principal) | -0.033 [-0.066; -0.001] |
| 8 pedidos/h | -0.037 [-0.080; 0.005] |
| 6 pedidos/h, sem recarga | -0.054 [-0.088; -0.020] |
| 6 pedidos/h, recarga 60 min | -0.013 [-0.027; 0.002] |

## Informação perfeita na agenda (exploratória)

| Família e configuração | Perfeita − declarada, decolagens com passageiros/h | Recusas por réplica |
|---|---:|---:|
| Recarga 30 min, Base | 0.004 [-0.015; 0.023] | 0.03 [-0.17; 0.24] |
| Recarga 30 min, S4 | 0.013 [-0.006; 0.031] | -0.03 [-0.19; 0.12] |
| Recarga 30 min, B2 | 0.004 [-0.015; 0.023] | 0.00 [-0.20; 0.20] |
| Sem recarga, Base | -0.004 [-0.013; 0.004] | 0.03 [-0.03; 0.10] |
| Sem recarga, S4 | -0.004 [-0.013; 0.004] | 0.03 [-0.03; 0.10] |
| Sem recarga, B2 | 0.000 (sem variação entre réplicas) | 0.00 (sem variação entre réplicas) |

Os resultados são de um cenário sintético com chegadas uniformes supostas, serviços
determinísticos no balcão e na inspeção, recursos vazios na abertura e horizonte
terminante de 8 h. Médias de espera descrevem somente visitas com início observado e
devem ser lidas junto às recusas, aos desvios, à censura e aos denominadores.
