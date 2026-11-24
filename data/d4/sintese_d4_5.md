# D4.5 — Síntese reproduzível dos contrastes

Fonte: `data/d4/resultados_d4_4.csv`. Analisador: `2c63f62`. Cada estimativa usa 30 réplicas
independentes; as diferenças são calculadas dentro da réplica e resumidas por média e
intervalo t bilateral de 95%.

## Contrastes principais na família de referência

| Contraste (sentido) | Política | Média [IC 95%] | Unidade |
|---|---|---:|---|
| Agenda − FCFS, Base | — | -0.129 [-0.179; -0.079] | decolagens/h |
| Base − S4 | FCFS | 0.504 [0.453; 0.555] | decolagens/h |
| Base − S4 | Agenda | 0.492 [0.440; 0.544] | decolagens/h |
| B2 − Base | FCFS | -141.530 [-158.382; -124.679] | s |
| B2 − Base | Agenda | -126.382 [-144.883; -107.882] | s |
| I2 − Base | FCFS | 0.000 [0.000; 0.000] | s |
| I2 − Base | Agenda | 0.000 [0.000; 0.000] | s |

## Populações e mecanismos na configuração-base

| Indicador por réplica | FCFS: média [IC 95%] | Agenda: média [IC 95%] |
|---|---:|---:|
| Pedidos oferecidos | 43.767 [41.483; 46.051] | 43.767 [41.483; 46.051] |
| Recusados | 0.000 [0.000; 0.000] | 7.900 [6.628; 9.172] |
| Desviados | 6.767 [5.667; 7.866] | 0.000 [0.000; 0.000] |
| Decolados | 33.767 [32.497; 35.036] | 32.733 [31.433; 34.034] |
| Pendentes no horizonte | 3.233 [2.664; 3.802] | 3.133 [2.590; 3.677] |
| Cobertura dos pedidos oferecidos | 0.777 [0.755; 0.800] | 0.754 [0.730; 0.777] |
| Espera média no balcão (s) | 154.816 [136.632; 172.999] | 138.686 [118.363; 159.009] |
| Fração de voos transportando passageiros retida pelo grupo | 0.092 [0.070; 0.113] | 0.078 [0.062; 0.095] |
| Retenção média pelo grupo (s) | 18.133 [11.941; 24.324] | 13.969 [9.066; 18.872] |
| Bloqueio médio do stand após prontidão para partir (s) | 7.961 [6.349; 9.572] | 75.902 [70.090; 81.714] |
| Ocupação física dos stands | 0.553 [0.532; 0.574] | 0.551 [0.530; 0.572] |

Os denominadores das médias condicionais estão em `resumo_celulas_d4_5.csv`. Na Base de
referência, a espera no balcão usa 2.529 atendimentos sob FCFS e 2.433 sob agenda; a
retenção usa 987 e 957 voos decolados transportando passageiros, respectivamente.

## Sensibilidade do contraste de política na Base

| Família | Agenda − FCFS, decolagens/h: média [IC 95%] |
|---|---:|
| 4 pedidos/h | -0.092 [-0.134; -0.049] |
| 6 pedidos/h, recarga 30 min | -0.129 [-0.179; -0.079] |
| 8 pedidos/h | -0.142 [-0.189; -0.095] |
| 6 pedidos/h, sem recarga | -0.050 [-0.084; -0.016] |
| 6 pedidos/h, recarga 60 min | -0.083 [-0.114; -0.052] |

## Informação perfeita na agenda

| Família e configuração | Perfeita − declarada, decolagens/h: média [IC 95%] |
|---|---:|
| Recarga 30 min, Base | 0.092 [0.049; 0.134] |
| Recarga 30 min, S4 | 0.083 [0.040; 0.126] |
| Recarga 30 min, B2 | 0.108 [0.063; 0.154] |
| Recarga 30 min, I2 | 0.092 [0.049; 0.134] |
| Sem recarga, Base | -0.008 [-0.020; 0.004] |
| Sem recarga, S4 | -0.008 [-0.020; 0.004] |
| Sem recarga, B2 | 0.000 [0.000; 0.000] |
| Sem recarga, I2 | -0.008 [-0.020; 0.004] |

## Leitura delimitada pelos dados

- Na família de referência, a agenda recusou pedidos antes da entrada completa no terminal,
  mas não aumentou a vazão: sua média ficou 0,129 decolagem/h abaixo do FCFS. O resultado
  coincide com maior bloqueio do stand após a prontidão para partir, pois a saída planejada
  funciona como horário mínimo na regra verificada da agenda.
- O quinto stand aumentou a vazão em aproximadamente 0,5 decolagem/h nas duas políticas e
  reduziu recusas ou desvios. Esse efeito pertence à topologia sintética e às durações
  adotadas; não estima a capacidade de um local real.
- O segundo balcão reduziu a espera média no balcão em mais de 120 s. Parte da espera foi
  deslocada para a inspeção (cerca de 8 s nas células B2), enquanto a Base tinha espera nula
  nessa estação. Acrescentar um segundo posto de inspeção à Base não alterou a espera porque
  não havia fila de inspeção a remover.
- Com recarga de 30 min, a informação perfeita recuperou cerca de 0,09 decolagem/h na Base;
  sem recarga, o intervalo incluiu zero. A comparação é de desenho informacional e não uma
  previsão do valor econômico de dados operacionais.

Os resultados são de um cenário sintético com chegadas uniformes supostas, recursos vazios
na abertura e horizonte terminante de 8 h. Médias de espera descrevem somente visitas com
início de atendimento observado e devem ser lidas junto às recusas, aos desvios, à censura e
aos denominadores arquivados.
