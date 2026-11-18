# Deliverable 2 — desenho conceitual, dados e método

## Situação

Em desenvolvimento. Este é um artefato de especificação; não é texto do artigo.

## Fronteira do sistema (versão 0)

Uma unidade de análise é um vertiporto de passageiros em uma janela operacional finita. O modelo
representará dois fluxos sincronizados:

```text
passageiro: chegada -> check-in/controle (opcional) -> espera -> gate -> embarque -> partida
eVTOL:     chegada -> TLOF/pad -> táxi -> stand/gate -> turnaround/recarga -> pad -> partida
```

O embarque só ocorre quando a aeronave, o gate/stand e os passageiros do voo estão elegíveis.
Assim, atraso de aeronave pode prolongar espera de passageiro; congestionamento no terminal pode,
por sua vez, atrasar a prontidão de partida. O modelo não representa rota completa, preço,
manutenção profunda, meteorologia ou um sítio real específico na primeira versão.

## Recursos e estados mínimos

| Camada | Recurso / estado | Capacidade | Regra inicial |
|---|---|---:|---|
| Coordenação | slot de chegada/partida | cenário | restringe liberação; não é tempo de serviço |
| Airside | TLOF/pad e rota de táxi | cenário | ocupação exclusiva e bloqueio físico |
| Interface | stand/gate | cenário | uma aeronave por posição; embarque/desembarque e energia podem requerê-lo |
| Energia | carregador | cenário | servidor finito; política de recarga será cenário |
| Terminal | check-in e controle | cenário | estações opcionais com filas finitas ou infinitas declaradas |
| Passageiro | grupo de voo | demanda | aguarda prontidão conjunta e tem limiar de LoS |

## Método proposto

1. Usar aproximações analíticas apenas para casos sem bloqueio (por exemplo, estabilidade e
   referência de fila multisservidor).
2. Usar simulação de eventos discretos para a rede acoplada, pois há capacidade finita,
   sincronização passageiro--aeronave e dependência entre recursos.
3. Declarar cada entrada como observada, de literatura, hipótese ou cenário. A primeira rodada
   será uma análise de cenários, não uma previsão de uma operação real.

## Métricas ligadas à pergunta de pesquisa

| Dimensão | Métrica | Definição operacional |
|---|---|---|
| Fluxo eVTOL | throughput | partidas concluídas por hora |
| Congestionamento | utilização e bloqueio | fração de ocupação por recurso; tempo ou ocorrência de bloqueio |
| Serviço do passageiro | espera até embarque | chegada ao vertiporto até início do embarque |
| Confiabilidade | P95 da espera e pontualidade | percentil 95; proporção que parte dentro da tolerância declarada |
| LoS / satisfação-proxy | atendimento ao limiar | proporção cuja espera e tempo total não excedem limiares de cenário |
| Equidade | dispersão por classe/coorte | diferença de espera entre grupos definidos no cenário |

Não será inferida satisfação psicológica a partir de tempo de espera. Na primeira versão, LoS e
espera percebida são *proxies* explícitos, sujeitos a análise de sensibilidade.

## Decisões ainda necessárias antes de implementação

- escolher a topologia-base e as capacidades de cenário;
- fixar qual processo terminal é obrigatório ou opcional;
- definir política de formação de grupos de passageiros e prioridade;
- escolher limiares de LoS/proxy e justificar suas faixas;
- definir horizonte, aquecimento, replicações e critérios de verificação.

O dicionário em `data/model_dictionary.csv` é a fonte de verdade para essas escolhas.
