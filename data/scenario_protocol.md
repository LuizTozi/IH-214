# Protocolo inicial de cenários (D2)

## Propósito

Comparar como capacidade e coordenação afetam simultaneamente fluxo eVTOL e medidas de serviço do
passageiro. Cenários não são previsões nem dados observados.

## Fatores a variar

| Fator | Níveis iniciais | Classificação |
|---|---|---|
| demanda de passageiros e eVTOL | baixa, intermediária, alta | cenário |
| número de pads, stands e carregadores | topologias factíveis | cenário sujeito a restrição de projeto |
| turnaround e recarga | faixas da literatura, com sensibilidade | literatura/cenário |
| processamento terminal | bypass, processo enxuto, processo completo | hipótese de processo |
| coordenação | FCFS, reserva de slot, regra de prioridade declarada | cenário |
| limiar LoS | faixa de sensibilidade, não valor normativo | cenário |

## Comparações essenciais

1. desacoplado: aeronaves e passageiros sem sincronização de prontidão;
2. acoplado: gate/stand, passageiro e eVTOL sincronizados;
3. capacidade fixa: variar demanda e regra de coordenação;
4. demanda fixa: variar um recurso escasso por vez.

## Regras de interpretação

- Relatar média, P95 e intervalos de confiança de replicações para cada métrica.
- Não chamar uma redução de espera de aumento de satisfação sem uma medida ou hipótese explícita.
- Não usar restrições FAA/EASA/ANAC/DECEA como tempos de serviço ou calibração comportamental.
- Registrar toda alteração no dicionário antes de executá-la no código.
