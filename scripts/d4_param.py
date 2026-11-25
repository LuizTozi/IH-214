"""Durações e regras do lado ar da D4 (D4.1 v2.1), em milissegundos inteiros.

Valores do traço integrado da D2 (data/scenarios/phase_d_terminal_verification.json)
e do cadastro data/parameter_registry.csv. Conferidos em scripts/d4_1_conferencia.py.
"""

import csv
from pathlib import Path
from statistics import mean

SOURCES = Path(__file__).resolve().parents[1] / "data" / "fontes"
with (SOURCES / "janssen_tempo_proprio.csv").open() as source:
    SECURITY_TIMES_S = tuple(int(row["own_time_s"]) for row in csv.DictReader(source))
with (SOURCES / "janssen_tamanho_grupo.csv").open() as source:
    GROUP_WEIGHTS = {int(row["group_size"]): int(row["passengers"]) / int(row["group_size"])
                     for row in csv.DictReader(source) if 1 <= int(row["group_size"]) <= 4}

COUNTER_MEAN_S = 164
ARRIVAL_PROFILES = {"fc_morning": (3.7, 6.5, 9), "lcc_afternoon": (5.5, 13.4, 14)}

OCC_ARR = 37_700     # toque até liberar fisicamente o TLOF, rebocado (PAR-043)
SEP = 30_000          # separação após a saída do TLOF, chegada e partida (PAR-048)
TAXI = 22_800        # percurso na rota compartilhada, por trecho (PAR-044)
DETACH = 27_000      # retirar o rebocador no stand (PAR-037)
DEBOARD = 65_800     # desembarque do passageiro de chegada (PAR-009)
EXIT_GATE = 26_700   # saída pelo gate (PAR-024)
WALK = 31_900        # sala de espera até o gate, por passageiro (PAR-022)
ENTER = 19_700       # porta até a aeronave, por passageiro (PAR-023)
BOARD = 73_000       # embarque, por passageiro (PAR-008)
ATTACH = 27_000      # prender o rebocador para a partida (PAR-037)
DEP_OCC = 45_000     # entrada no TLOF até a decolagem (PAR-045)

WINDOW = 300_000     # janela de toque [t, t + 300 s], agenda e desvio no FCFS (PAR-055)
TOLERANCE = 60_000   # tolerância de pontualidade (PAR-049)

STAND_INBOUND = DETACH + DEBOARD + EXIT_GATE      # 119,5 s antes da recarga
PER_PAX = WALK + ENTER + BOARD                    # 124,6 s por embarcado
ARR_TLOF = OCC_ARR + SEP                          # TLOF indisponível na chegada
ARR_ROUTE = OCC_ARR + TAXI                        # rota reservada do toque à entrada no stand
DEP_ROUTE = TAXI                                  # rota na partida
DEP_TLOF = TAXI + DEP_OCC + SEP                   # TLOF reservado da saída do stand à separação

# Previsão da agenda (D4.1 v2.1): durações declaradas do terminal.
COUNTER_DECLARED = COUNTER_MEAN_S * 1000    # PAR-046
SECURITY_DECLARED = round(mean(SECURITY_TIMES_S) * 1000)    # PAR-047
BAG_FORECAST = 45_000         # média de U(30, 60) s (PAR-058)
BAG_LOW, BAG_HIGH = 30_000, 60_000   # PAR-028
