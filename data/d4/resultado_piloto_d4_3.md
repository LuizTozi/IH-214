# D4.3 — Resultado do piloto de precisão

Fonte: `data/d4/piloto_d4_3.csv`. Plano anterior aos dados: `data/d4/plano_piloto_d4_3.md`.

O piloto serve apenas ao dimensionamento. Suas médias não serão combinadas com as rodadas
definitivas nem tratadas como resultados do artigo.

| Contraste | Pares | Média | DP pareado | Semilargura 95% | Alvo | n requerido |
|---|---:|---:|---:|---:|---:|---:|
| agenda - FCFS, Base | 30 | -0.092 decolagens/h | 0.098 | 0.037 | 0.250 | 2 |
| Base - S4, FCFS | 30 | 0.496 decolagens/h | 0.162 | 0.061 | 0.250 | 2 |
| Base - S4, agenda | 30 | 0.508 decolagens/h | 0.164 | 0.061 | 0.250 | 2 |
| B2 - Base, FCFS | 30 | -136.085 s | 47.015 | 17.556 | 30.000 | 11 |
| B2 - Base, agenda | 30 | -123.944 s | 41.984 | 15.677 | 30.000 | 9 |
| I2 - Base, FCFS | 30 | 0.000 s | 0.000 | 0.000 | 30.000 | 2 |
| I2 - Base, agenda | 30 | 0.000 s | 0.000 | 0.000 | 30.000 | 2 |

Número fixado para a D4.4: **30 réplicas independentes**.

Critério limitante: mínimo predefinido de 30 réplicas; o maior requisito estimado foi 11.

O cálculo usa `ceil((t_0.975,29 × s / h)^2)`, com diferenças dentro da réplica.
A escolha é o maior requisito entre os contrastes e o mínimo de 30 réplicas.
