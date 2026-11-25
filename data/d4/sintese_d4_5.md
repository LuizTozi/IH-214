# D4.5 — Síntese reproduzível dos contrastes (D4.1 v2.4)

Fonte: `data/d4/resultados_d4_4.csv`. Analisador: `f169f52`. Cada estimativa usa as réplicas
independentes válidas; as diferenças são calculadas dentro da réplica e resumidas por
média e intervalo t bilateral de 95%. Proporções são médias das razões por réplica.
Todos os números desta síntese vêm de `resumo_celulas_d4_5.csv` e
`contrastes_d4_5.csv`.

## Contrastes principais na família de referência

| Contraste (sentido) | Política | Média [IC 95%] | Unidade |
|---|---|---:|---|
| Agenda − FCFS, Base | — | -0.096 [-0.132; -0.060] | decolagens com passageiros/h |
| Base − S4 | FCFS | 0.479 [0.422; 0.537] | decolagens com passageiros/h |
| Base − S4 | Agenda | 0.467 [0.404; 0.529] | decolagens com passageiros/h |
| B2 − Base | FCFS | -99.1 [-114.6; -83.7] | s |
| B2 − Base | Agenda | -95.2 [-109.6; -80.9] | s |

## Balanço e mecanismos por demanda na configuração-base

| Indicador por réplica | Política | 4 pedidos/h | 6 pedidos/h | 8 pedidos/h |
|---|---|---:|---:|---:|
| Pedidos oferecidos | FCFS | 28.70 [26.90; 30.50] | 43.77 [41.48; 46.05] | 57.97 [55.09; 60.84] |
| Pedidos oferecidos | Agenda | 28.70 [26.90; 30.50] | 43.77 [41.48; 46.05] | 57.97 [55.09; 60.84] |
| Recusados | FCFS | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] |
| Recusados | Agenda | 1.97 [1.37; 2.56] | 7.23 [6.17; 8.30] | 14.47 [12.68; 16.25] |
| Desviados | FCFS | 1.50 [0.99; 2.01] | 6.43 [5.35; 7.51] | 13.13 [11.42; 14.85] |
| Desviados | Agenda | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] |
| Decolados com passageiros (vazios à parte) | FCFS | 3.125 [2.955; 3.295] | 4.283 [4.115; 4.451] | 5.104 [4.944; 5.264] |
| Decolados com passageiros (vazios à parte) | Agenda | 3.083 [2.920; 3.247] | 4.188 [4.013; 4.362] | 4.946 [4.794; 5.098] |
| Decolagens vazias | FCFS | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] |
| Decolagens vazias | Agenda | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] | 0.00 [0.00; 0.00] |
| Pendentes no horizonte | FCFS | 2.20 [1.72; 2.68] | 3.07 [2.55; 3.58] | 4.00 [3.56; 4.44] |
| Pendentes no horizonte | Agenda | 2.07 [1.65; 2.48] | 3.03 [2.50; 3.57] | 3.93 [3.53; 4.34] |
| Cobertura dos oferecidos | FCFS | 0.875 [0.854; 0.897] | 0.788 [0.766; 0.810] | 0.711 [0.688; 0.733] |
| Cobertura dos oferecidos | Agenda | 0.865 [0.842; 0.888] | 0.771 [0.748; 0.793] | 0.689 [0.666; 0.712] |
| Espera média no balcão (s) | FCFS | 99.9 [74.4; 125.4] | 108.9 [90.9; 126.9] | 112.3 [95.9; 128.7] |
| Espera média no balcão (s) | Agenda | 99.4 [74.6; 124.2] | 104.3 [87.5; 121.1] | 114.9 [96.2; 133.5] |
| Conformidade ao limite do balcão (180 s) | FCFS | 0.820 [0.781; 0.859] | 0.789 [0.760; 0.819] | 0.765 [0.733; 0.798] |
| Conformidade ao limite do balcão (180 s) | Agenda | 0.821 [0.784; 0.858] | 0.795 [0.767; 0.822] | 0.761 [0.727; 0.795] |
| Fração retida pelo grupo | FCFS | 0.080 [0.051; 0.108] | 0.083 [0.058; 0.108] | 0.070 [0.051; 0.089] |
| Fração retida pelo grupo | Agenda | 0.067 [0.040; 0.094] | 0.069 [0.045; 0.092] | 0.068 [0.047; 0.089] |
| Espera após a inspeção, média (s) | FCFS | 665.8 [634.7; 696.9] | 664.2 [640.2; 688.2] | 665.6 [642.3; 688.8] |
| Espera após a inspeção, média (s) | Agenda | 682.8 [653.6; 711.9] | 683.8 [660.4; 707.3] | 683.2 [659.5; 706.9] |
| Bloqueio do stand após prontidão (s) | FCFS | 7.4 [5.2; 9.7] | 10.6 [8.4; 12.9] | 13.4 [10.4; 16.4] |
| Bloqueio do stand após prontidão (s) | Agenda | 1.5 [0.8; 2.1] | 1.8 [1.1; 2.5] | 2.3 [1.4; 3.2] |

A linha de decolados com passageiros está em decolagens/h (VAR-016).

## Terminal: Base e B2 na referência

| Indicador por réplica | Base FCFS | B2 FCFS | Base agenda | B2 agenda |
|---|---:|---:|---:|---:|
| Espera média no balcão (s) | 108.9 [90.9; 126.9] | 9.8 [6.3; 13.2] | 104.3 [87.5; 121.1] | 9.1 [5.8; 12.4] |
| P95 da espera no balcão (s) | 567.6 [469.7; 665.5] | 74.1 [38.5; 109.7] | 540.7 [453.1; 628.2] | 59.9 [28.9; 91.0] |
| Conformidade ao limite do balcão | 0.789 [0.760; 0.819] | 0.980 [0.971; 0.989] | 0.795 [0.767; 0.822] | 0.983 [0.974; 0.991] |
| Espera média na bagagem (s) | 2.9 [2.4; 3.5] | 3.7 [3.0; 4.5] | 3.0 [2.4; 3.6] | 3.8 [3.0; 4.6] |
| Espera média na inspeção (s) | 35.5 [28.5; 42.4] | 37.7 [29.7; 45.7] | 35.8 [28.8; 42.8] | 37.5 [30.3; 44.7] |
| Espera após a inspeção, média (s) | 664.2 [640.2; 688.2] | 748.9 [731.8; 766.0] | 683.8 [660.4; 707.3] | 769.7 [753.6; 785.9] |
| Espera após a inspeção, P95 (s) | 1108.8 [1080.7; 1136.8] | 1160.9 [1132.0; 1189.7] | 1124.2 [1100.1; 1148.4] | 1179.9 [1148.5; 1211.3] |
| Fração retida pelo grupo | 0.083 [0.058; 0.108] | 0.029 [0.017; 0.040] | 0.069 [0.045; 0.092] | 0.023 [0.011; 0.034] |

Contrastes pareados B2 − Base (exploratórios): conformidade ao limite do balcão 0.191 [0.166; 0.216] (FCFS) e 0.188 [0.162; 0.213] (agenda); espera média após a inspeção 84.7 [70.4; 98.9] s (FCFS) e 85.9 [71.2; 100.6] s (agenda).

Mesma população (embarcados), B2 − Base: espera no balcão -100.9 [-116.7; -85.1] s (FCFS) e -96.6 [-111.5; -81.8] s (agenda); chegada ao início do embarque -13.7 [-21.2; -6.3] s (FCFS) e -9.3 [-15.1; -3.5] s (agenda).

Denominadores totais (30 réplicas): espera no balcão Base FCFS 1.644, B2 FCFS 1.665, Base agenda 1.628, B2 agenda 1.649; voos com passageiros Base FCFS 1.028, B2 FCFS 1.035, Base agenda 1.005, B2 agenda 1.012.

## Sensibilidade do contraste de política na Base (exploratória)

| Família | Agenda − FCFS, decolagens com passageiros/h: média [IC 95%] |
|---|---:|
| 4 pedidos/h | -0.042 [-0.064; -0.019] |
| 6 pedidos/h, recarga 30 min (principal) | -0.096 [-0.132; -0.060] |
| 8 pedidos/h | -0.158 [-0.216; -0.101] |
| 6 pedidos/h, sem recarga | -0.146 [-0.206; -0.086] |
| 6 pedidos/h, recarga 60 min | -0.013 [-0.035; 0.010] |
| 15% de ausência | -0.071 [-0.113; -0.029] |
| Chegada LCC da tarde | -0.104 [-0.143; -0.065] |
| Janela de 150 s | -0.275 [-0.336; -0.214] |
| Janela de 600 s | -0.037 [-0.068; -0.007] |
| Partida deslocada 600 s | -0.083 [-0.123; -0.044] |
| Partida deslocada 1.200 s | -0.188 [-0.252; -0.123] |

## Quinto stand e segundo balcão em cada família

| Família | Stand FCFS (voos/h) | Stand agenda (voos/h) | Balcão FCFS (s) | Balcão agenda (s) |
|---|---:|---:|---:|---:|
| referencia | 0.479 [0.422; 0.537] | 0.467 [0.404; 0.529] | -99.1 [-114.6; -83.7] | -95.2 [-109.6; -80.9] |
| demanda_baixa | 0.221 [0.174; 0.268] | 0.200 [0.153; 0.247] | -89.7 [-111.0; -68.4] | -89.9 [-111.0; -68.8] |
| demanda_alta | 0.725 [0.655; 0.795] | 0.650 [0.585; 0.715] | -102.7 [-116.9; -88.5] | -106.1 [-122.8; -89.5] |
| sem_recarga | 0.017 [0.001; 0.033] | 0.013 [-0.002; 0.027] | -156.7 [-191.7; -121.7] | -150.6 [-182.2; -118.9] |
| recarga_longa | 0.463 [0.425; 0.500] | 0.463 [0.425; 0.500] | -67.4 [-83.0; -51.9] | -70.0 [-86.1; -53.9] |
| ausencia_15 | 0.454 [0.384; 0.524] | 0.433 [0.364; 0.502] | -92.2 [-108.5; -75.8] | -87.2 [-102.3; -72.1] |
| chegada_lcc_tarde | 0.487 [0.431; 0.544] | 0.471 [0.408; 0.534] | -118.7 [-137.6; -99.8] | -109.6 [-124.5; -94.6] |
| janela_150 | 0.517 [0.462; 0.571] | 0.388 [0.330; 0.445] | -100.2 [-117.5; -83.0] | -89.1 [-108.4; -69.7] |
| janela_600 | 0.446 [0.383; 0.509] | 0.467 [0.402; 0.531] | -106.9 [-123.5; -90.3] | -107.9 [-125.4; -90.4] |
| partida_600 | 0.492 [0.436; 0.548] | 0.483 [0.432; 0.535] | -102.8 [-119.5; -86.1] | -97.9 [-113.1; -82.6] |
| partida_1200 | 0.492 [0.438; 0.545] | 0.392 [0.337; 0.446] | -95.1 [-111.2; -79.0] | -87.9 [-104.6; -71.1] |

As esperas incluem apenas visitas cujo atendimento começou antes do horizonte.
Os contrastes family - reference do CSV comparam as sensibilidades à Base da referência
por semente e política. Intervalos exploratórios são individuais, sem ajuste de multiplicidade.
