# D4 — Plano de análise dos resultados

A D4 deve explicar como a política de admissão e a quantidade de recursos do lado ar e do terminal afetam as partidas, a espera em cada estação do terminal e a retenção da aeronave pelo grupo no vertiporto simulado. O produto será uma seção de resultados e discussão em `sections/results.tex`, com comparação à literatura e implicações práticas. As conclusões gerais do artigo ficam para a D5.

## Fases de trabalho e repercussões nas entregas anteriores

O trabalho começa na D4.1. As fases abaixo organizam a execução da pesquisa. As subseções de resultados organizam a exposição dos achados ao leitor.

| Fase | Produto que permite avançar | Quando revisar a D2 (modelo e método) | Quando revisar a D3 (fundamentação) |
|---|---|---|---|
| D4.1 · Especificação | Matriz de cenários com fatores, hipóteses e entradas identificadas | Descrever a extensão do caso unitário para dois stands, a disputa pelo carregador e a informação disponível na admissão. Registrar a procedência de cada entrada. | Se uma escolha for atribuída à literatura, conferir se a fonte cobre o mecanismo nas condições propostas. Uma escolha sintética pode ser declarada na D2. |
| D4.2 · Implementação e verificação | Traços reproduzíveis que mostram a disputa entre aeronaves, a exclusividade de rota e carregador e os estados no horizonte | Se código e especificação divergirem, localizar a origem. Um erro de implementação exige correção e novo teste. Uma ambiguidade na regra de prioridade ou liberação exige também revisão do protocolo. | Se a verificação revelar ambiguidade em um conceito transferido, como reserva e ocupação física, conferir a definição na fonte e corrigir a síntese se necessário. |
| D4.3 · Piloto | Dispersão das diferenças pareadas, número planejado de réplicas e configuração definitiva | Registrar como foram escolhidos horizonte, demanda e precisão. Se quase nenhum voo decolar, verificar se a janela representa a operação pretendida e documentar eventual alteração antes das rodadas definitivas. | A frequência observada no piloto pertence ao desenho experimental. Revisitar a D3 se a justificativa de um parâmetro depender de uma população ou regime diferente do estudado pela fonte. |
| D4.4 · Experimentos | Réplicas pareadas arquivadas para as políticas, quantidades de stands e sensibilidades | Se uma entrada comum variar entre políticas por engano, corrigir a geração dos traços e repetir os pares afetados. Se for preciso alterar o desenho congelado, versionar a alteração e identificar as execuções afetadas. | Um efeito pequeno, incerto ou de sinal inesperado será levado à discussão da D4. |
| D4.5 · Análise dos mecanismos | Estimativas com intervalos, denominadores e sequência de eventos que permita examinar o gargalo | Se os registros não distinguirem espera pelo carregador de espera pela rota, acrescentar os eventos necessários ao dicionário e repetir as execuções que dependem deles. | Conferir a fronteira da comparação. Por exemplo, se a política reduzir o P95 entre embarcados e aumentar as recusas, rever na D3 qualquer afirmação que generalize essa espera a todos os passageiros. |
| D4.6 · Discussão e integração | Seção de resultados reproduzível, com alcance e limitações de cada comparação | Incorporar ao texto do método a configuração efetivamente executada e distinguir os traços de verificação dos cenários experimentais. | Corrigir atribuições ou condições de transferência identificadas na releitura. Se uma lacuna exigir busca complementar, documentar a pergunta, a busca e a extração como complemento à revisão original. |

Ao revisar uma entrega anterior, registrar a fase de origem, a evidência que motivou a mudança e os trechos, testes ou resultados afetados. Se uma regra do modelo mudar após as rodadas, verificar novamente o caso afetado antes de recalcular os contrastes. A interpretação de um resultado inesperado começa pelos eventos, pelas populações comparadas e pelas condições do cenário.

## D4.1 · Fechar o cenário experimental

**Versão 2 em 23/11/2026, após revisão crítica. A D4.2 aguarda a aprovação do autor.** A versão 1 não permitia observar a fila por estação nem a retenção pelo grupo. As esperas no terminal eram iguais em todas as configurações, e o grupo ficava pronto muito antes da aeronave. A [especificação](D4_1_cenarios.md) registra as quatro decisões da revisão:

- lado ar com 1 TLOF e 5 stands (Feldhoff 2022);
- contrastes de servidor no balcão e na inspeção;
- recusa comunicada na decisão;
- chegadas entre 15 e 60 min antes da partida programada.

O desenho experimental será redigido após a conclusão de todas as fases da D4.

## D4.2 · Preparar e verificar as execuções

Adaptar o simulador integrado para configurar os recursos escolhidos e produzir uma linha por cenário, política e réplica. Arquivar configuração, versão do código, semente e identificador do traço oferecido. Gerar pedidos, manifestos e durações antes da decisão de admissão, com valores vinculados aos respectivos pedidos e passageiros. Assim, uma recusa não desloca a sequência de sorteios para o próximo voo.

Rodar os testes das fases A–D e verificar manualmente um caso com disputa de recurso e outro com atendimento interrompido pelo horizonte. Conferir o balanço de pedidos entre cancelados, recusados, concluídos e pendentes, a capacidade física de cada recurso e a ordem dos eventos de embarque. A janela principal será terminante, com estado inicial declarado e contagem até o horizonte comum. Usar o período inteiro se o início vazio fizer parte da operação estudada.

## D4.3 · Dimensionar o experimento com o piloto

Registrar as taxas de demanda e a configuração-base antes das rodadas definitivas. Fazer um piloto para estimar a dispersão das diferenças pareadas em partidas/h. Definir a margem de precisão operacionalmente relevante e dimensionar as réplicas independentes para um intervalo de confiança de 95% com essa semilargura. Documentar o número escolhido e a precisão efetivamente obtida.

## D4.4 · Executar os contrastes pareados

| Pergunta | Variação planejada | Comparação |
|---|---|---|
| Qual o efeito da admissão antecipada? | Agendamento e FCFS local | Mesmos recursos, pedidos oferecidos, passageiros e durações em cada par. A recusa altera a carga do terminal |
| Qual o efeito do estacionamento? | 5 stands (Base) contra 4 stands (S4) | Mesma política e mesma demanda em cada par. Repetir sob ambas as políticas |
| Qual o efeito de um servidor no terminal? | Segundo balcão (B2) e segundo posto de inspeção (I2), um por vez | Mesma política e mesma demanda. Medir a espera por estação, o deslocamento da fila e a retenção pelo grupo |
| Em que condições o efeito muda? | Demanda de 4, 6 e 8 pedidos/h. Recarga no stand de 0, 30 e 60 min. Informação perfeita na agenda | Variar um fator por vez a partir do caso-base. Preservar as demais etapas do turnaround |

## D4.5 · Medir desempenho e explicar o mecanismo

| Resultado | Cálculo e leitura |
|---|---|
| Partidas e atendimento da demanda | Decolagens observadas por hora e por pedido oferecido. Exibir ao lado cancelamentos, recusas e pendências para detectar seleção pela admissão |
| Atraso e pontualidade | Medir atraso em relação ao horário solicitado de partida. Informar partidas dentro da tolerância sobre decolagens observadas e o tamanho desse denominador |
| Serviço ao passageiro | Por estação, apresentar espera até início do serviço, conformidade ao limiar da D2, denominador, esperas censuradas e saídas por recusa. Para bagagem, apresentar a espera. Calcular o P95 chegada–início do embarque entre percursos observados, com o número de embarcados e perdidos |
| Retenção pelo grupo | Por voo, comparar o instante em que o último confirmado fica pronto com o instante em que a aeronave fica pronta para embarque. Relatar a fração de voos retidos e a duração da retenção. Verificar se B2 e I2 reduzem a retenção e se a espera se desloca entre estações |
| Gargalo | Confrontar ocupação física por recurso, tempo bloqueado e filas com os instantes de prontidão do grupo e da aeronave. Verificar se acrescentar o stand reduz o bloqueio e se a espera se desloca para outro recurso |

Calcular cada diferença dentro da réplica e resumir as diferenças entre réplicas com média e intervalo de confiança de 95%. Declarar o sentido da subtração nas tabelas. Se uma réplica terminar sem decolagens ou embarques, registrar o indicador condicional correspondente como indefinido e informar quantos pares permitem estimá-lo. Preservar essa réplica na análise de partidas/h.

## D4.6 · Redigir e conferir a entrega

1. Abrir a seção com uma tabela de cenários, horizonte, demanda oferecida e réplicas. Apresentar os efeitos das duas intervenções com estimativas, unidades e intervalos.
2. Selecionar uma figura que relacione partidas/h à demanda e uma tabela que mostre, para os mesmos cenários, recusas, pendências e espera no terminal. Usar um traço de eventos para explicar um bloqueio identificado nas réplicas.
3. Confrontar o mecanismo observado com o bloqueio por estacionamento em D001, com a alocação de recursos em D026 e D029 e com a comparação entre um e dois balcões de Feldhoff 2022, usando as fronteiras documentadas na [síntese da D3](../data/d3/sintese_mecanismos.md). Explicar convergências ou divergências e indicar em quais condições uma mudança de política ou infraestrutura teria implicação operacional.
4. Integrar a seção ao manuscrito, recompilar e reproduzir cada tabela e figura a partir dos resultados arquivados. Encerrar quando cada afirmação quantitativa puder ser ligada ao cenário, denominador e incerteza correspondentes.

## Estrutura da seção e passagem ao piloto

O [roteiro de redação em LaTeX](../sections/results.tex) organiza os contrastes em quatro configurações sob duas políticas. O contraste de estacionamento compara 5 e 4 stands, cada um com seu carregador. Os contrastes do terminal acrescentam um balcão ou um posto de inspeção com os stands fixos. Esse posto adicional de inspeção corresponde à hipótese da D3.

Ao fechar cada fase da D4, registrar o alcance do que foi verificado e revisar as implicações para a D2 e a D3 antes de iniciar a fase seguinte. A próxima fase é a D4.2.
