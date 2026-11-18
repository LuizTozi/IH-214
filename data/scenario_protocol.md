# Protocolo inicial de cenários (D2)

## Propósito

Comparar como capacidade e coordenação afetam simultaneamente fluxo eVTOL e medidas de serviço do
passageiro. Cenários não são previsões nem dados observados.

## Fatores a variar

| Fator | Níveis iniciais | Classificação |
|---|---|---|
| demanda de passageiros e eVTOL | baixa, intermediária, alta | cenário |
| número de pads, stands e carregadores | base regulatória unitária; expansões factíveis | cenário sujeito a restrição de projeto |
| turnaround e recarga | faixas da literatura, com sensibilidade | literatura/cenário |
| processamento terminal | bypass, processo enxuto, processo completo | hipótese de processo |
| coordenação | agendamento/reserva de slot como base; FCFS como benchmark | cenário |
| passageiros por voo | 1 a 4; piloto excluído da demanda | cenário baseado nas aeronaves de referência |
| recarga | ausente na Fase A; no stand, adjacente dedicada ou ausente na Fase C | cenário baseado em evidência de missão e infraestrutura |
| limiar LoS | faixa de sensibilidade, não valor normativo | cenário |

## Comparações essenciais

1. núcleo A: pouso e saída do TLOF com capacidade unitária e exclusão mútua;
2. progressão A→D: inserir recursos e processos somente após verificação da fase anterior;
3. desacoplado: aeronaves e passageiros sem sincronização de prontidão;
4. acoplado: gate/stand, passageiro e eVTOL sincronizados;
5. capacidade fixa: variar demanda e regra de coordenação;
6. demanda fixa: variar um recurso escasso por vez.
7. sincronização: comparar partida com grupo completo e política declarada para ausência/atraso; não sobrepor recarga e embarque no caso-base.

## Regras de interpretação

- Relatar média, P95 e intervalos de confiança de replicações para cada métrica.
- Não chamar uma redução de espera de aumento de satisfação sem uma medida ou hipótese explícita.
- Não usar restrições FAA/EASA/ANAC/DECEA como tempos de serviço ou calibração comportamental.
- Registrar toda alteração no dicionário antes de executá-la no código.
