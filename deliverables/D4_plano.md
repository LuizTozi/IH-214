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

As durações usadas nas estimativas de carga foram conferidas com o simulador da Fase D (`scripts/d4_1_conferencia.py`). Essa conferência não executa o experimento e não compara políticas.

O desenho experimental será redigido após a conclusão de todas as fases da D4.

## D4.2 · Preparar e verificar as execuções

**Andamento.** A D4.2 está dividida em cinco etapas, cada uma com seu commit: gerador do dia, terminal, lado ar com FCFS, agenda e testes de integração. Os scripts das fases A a D não são alterados.

- **Etapa 1 concluída em 23/11/2026:** o gerador do dia (`scripts/d4_dia.py`, testes em `scripts/test_d4_dia.py`).
  - Gera os pedidos a 8/h e os afina para 6/h e 4/h.
  - Sorteia, para cada passageiro, ausência, antecedência de chegada e duração da bagagem antes da política.
  - Usa um gerador próprio para cada fonte de acaso.
- **Etapa 2 concluída em 23/11/2026:** o terminal (`scripts/d4_terminal.py`, testes em `scripts/test_d4_terminal.py`), no ambiente Conda `ih214` (`environment.yml`: Python 3.12 e SimPy 4.1.2).
  - Balcão, bagagem e inspeção com um ou dois servidores, fila FCFS única e menor índice livre.
  - Saída por recusa ou desvio na fila (espera censurada), após o serviço em curso e na sala de espera. Quem ainda não chegou não comparece.
  - Os testes conferem servidores em paralelo, capacidade nunca excedida, as três formas de saída, limite inclusivo, censura no horizonte e determinismo.
  - Conferência de carga, só na configuração Base: a ocupação do balcão reproduz a estimativa, descontados os passageiros que chegam após o horizonte e o acaso das sementes.
- **Etapa 3 concluída em 23/11/2026:** o lado ar com FCFS (`scripts/d4_sim.py`, `scripts/d4_param.py`, testes em `scripts/test_d4_sim.py`).
  - TLOF com separação, rota unitária e N stands. Posse e ocupação física são registradas à parte.
  - A chegada exige TLOF, rota e stand ao mesmo tempo. A aeronave desvia se a chegada não começar até t + 300 s (janela inclusiva), e o terminal é avisado.
  - Embarque dos confirmados na ordem de prontidão. A espera da aeronave pelo grupo é a retenção.
  - O terminal ganhou sala de espera por voo e a previsão de prontidão que a agenda usará.
- **Etapa 4 concluída em 23/11/2026:** a agenda (`scripts/d4_agenda.py`, testes em `scripts/test_d4_sim.py`).
  - **Calendário:** atualizado na decisão com a previsão de cada voo admitido.
  - **Busca:** primeiro toque viável em [t, t + 300 s] e stand de menor índice. Sem toque viável, recusa com aviso ao terminal.
  - **Execução:** horários mínimos de toque e de saída, com prioridade pelo horário planejado.
  - **Previsão:** reservas não chegadas pelo fechamento mais as durações declaradas. A informação perfeita usa chegadas, bagagens e ausências realizadas.
  - **Verificação:**
    - recusa no instante da decisão;
    - reserva da partida;
    - espera até a saída planejada sob previsão pessimista, nula com informação perfeita;
    - saída posterior ao plano quando a bagagem excede a previsão;
    - decisão independente de pedidos futuros.
  - **Constatação:** com janela de 300 s, um erro de previsão de bagagem se resolve pelo menos 241,6 s antes da saída do stand. Uma decisão posterior que dependa dessa saída já vê o valor correto. Logo, o erro de previsão atrasa o próprio voo, mas dificilmente se propaga a voos decididos depois.
- **Etapa 5 concluída em 23/11/2026:** o executor do experimento (`scripts/d4_experimento.py`) e os testes de integração (`scripts/test_d4_experimento.py`).
  - Gera 48 células por réplica, com uma linha por célula, versão do código, semente e identificador do dia arquivado.
  - Os testes de integração verificam o pareamento, o balanço dos pedidos e os resultados próprios de cada política.
- **D4.2 concluída em 23/11/2026.** São 60 testes no ambiente `ih214`, e o registro está em [`data/d4/verificacao_d4_2.md`](../data/d4/verificacao_d4_2.md). A próxima fase é a D4.3, o piloto. Antes dela, o autor deve revisar a interpretação da execução agendada registrada na especificação.
- **Levantamento de código aberto em 23/11/2026, antes da etapa 2.**
  - **VertiSim** (`eminb61/vertisim`, licença MIT; Onat, ligado a D001).
    - Usa SimPy, com tempo inteiro em milissegundos.
    - Tem `FilterStore` para stands e sala de espera e remove passageiros da sala por predicado ("spill").
    - Usa `PriorityResource` para a FATO e `Resource` para os carregadores.
    - A inspeção é só um tempo fixo. O parâmetro de número de servidores existe, mas não é usado. O VertiSim não modela fila nas estações do terminal.
  - **Agendador de superfície da KAIST** (`hoon7591/Vertiport-Surface-Scheduler`, sem licença, só leitura).
    - Cobre apenas o lado ar: otimização em Gurobi, horizonte deslizante e regras FCFS.
  - **Sem licença** (KAIST, Saxena e KRA33): o código não pode ser copiado nem adaptado. Servem só como leitura de ideias, com citação.
  - **Adaptação adotada:** padrões do VertiSim e da documentação da SimPy, ambos MIT, com atribuição no código. São eles: `Resource(capacity=c)` para estações com um ou dois servidores; espera da vez combinada com o evento de desvio do voo, para a saída da fila; e remoção da sala de espera por predicado.

Adaptar o simulador integrado para configurar os recursos escolhidos e produzir uma linha por cenário, política e réplica. Arquivar configuração, versão do código, semente e identificador do traço oferecido. Gerar pedidos, manifestos e durações antes da decisão de admissão, com valores vinculados aos respectivos pedidos e passageiros. Assim, uma recusa não desloca a sequência de sorteios para o próximo voo.

Rodar os testes das fases A–D e verificar manualmente um caso com disputa de recurso e outro com atendimento interrompido pelo horizonte. Conferir o balanço de pedidos entre cancelados, recusados, concluídos e pendentes, a capacidade física de cada recurso e a ordem dos eventos de embarque. A janela principal será terminante, com estado inicial declarado e contagem até o horizonte comum. Usar o período inteiro se o início vazio fizer parte da operação estudada.

## D4.3 · Dimensionar o experimento com o piloto

Registrar as taxas de demanda e a configuração-base antes das rodadas definitivas. Fazer um piloto para estimar a dispersão das diferenças pareadas nos quatro indicadores principais da [especificação](D4_1_cenarios.md): decolagens/h nos contrastes de política e de stands, espera média no balcão em B2 e espera média na inspeção em I2. Dimensionar as réplicas pelo indicador que exigir mais réplicas. Definir a margem de precisão operacionalmente relevante e dimensionar as réplicas independentes para um intervalo de confiança de 95% com essa semilargura. Documentar o número escolhido e a precisão efetivamente obtida.

**Plano congelado em 24/11/2026, antes da execução.** O protocolo, as sementes do piloto, as
semilarguras-alvo e a separação entre piloto e rodadas definitivas estão em
[`data/d4/plano_piloto_d4_3.md`](../data/d4/plano_piloto_d4_3.md). A instrução de continuidade
preserva para o piloto a interpretação da execução agendada verificada na D4.2; essa escolha
continua declarada como decisão do modelo, não como validação empírica.

**D4.3 concluída em 24/11/2026.** As 30 réplicas do piloto e os dias oferecidos estão arquivados
em `data/d4/`. Todos os sete contrastes tiveram 30 pares válidos. O maior requisito calculado foi
11 réplicas, para a espera no balcão sob FCFS; prevaleceu o mínimo predefinido de 30. A inspeção
teve diferença nula entre I2 e Base nas 30 réplicas, coerente com a hipótese registrada de ausência
de fila nessa estação sob o cenário de referência. Essa constatação serve para avaliar o desenho e
não será combinada às rodadas definitivas. O relatório é
[`data/d4/resultado_piloto_d4_3.md`](../data/d4/resultado_piloto_d4_3.md). A D4.4 usará 30
réplicas independentes, sementes 20001 a 20030.

## D4.4 · Executar os contrastes pareados

**D4.4 refeita em 25/11/2026 sob a D4.1 v2.2.** A revisão de `claude/outputs/D4_REVISAO_CLAUDE.md` levou o autor a quatro decisões: saída planejada como prioridade, não horário mínimo; retirada da I2; vazão só com voos de passageiros; e espera após a inspeção no lugar do P95 chegada–embarque. Com as mesmas sementes e dias, foram executadas 36 células por réplica e 1.080 linhas, versão de código `1262bb2`. Os dias arquivados não mudaram. O balanço de pedidos fecha em todas as linhas, e os 72 testes passam.

**Primeira execução, 24/11/2026 (v2.1, substituída).** Foram executadas 30 réplicas independentes (sementes 20001 a
20030), 48 células por réplica e 1.440 linhas no total. O arquivo
`data/d4/resultados_d4_4.csv` registra a versão de código `954995e`; os 30 dias oferecidos estão
em `data/d4/dias_d4_4/`. A conferência pós-execução encontrou 1.440 chaves de célula distintas,
zero erros no balanço de pedidos, nenhuma recusa sob FCFS, nenhum desvio sob agenda, ocupações
entre zero e um e nenhuma média primária ausente. Os 69 testes, incluindo os do analisador da
D4.5, continuam passando. Esses controles verificam integridade; as estimativas e sua
interpretação pertencem à D4.5.

| Pergunta | Variação planejada | Comparação |
|---|---|---|
| Qual o efeito da admissão antecipada? | Agendamento e FCFS local | Mesmos recursos, pedidos oferecidos, passageiros e durações em cada par. A recusa altera a carga do terminal |
| Qual o efeito do estacionamento? | 5 stands (Base) contra 4 stands (S4) | Mesma política e mesma demanda em cada par. Repetir sob ambas as políticas |
| Qual o efeito de um servidor no terminal? | Segundo balcão (B2); o segundo posto de inspeção (I2) saiu na v2.2 por não ter fila a remover com serviços determinísticos | Mesma política e mesma demanda. Medir a espera por estação, o deslocamento da fila e a retenção pelo grupo |
| Em que condições o efeito muda? | Demanda de 4, 6 e 8 pedidos/h. Recarga no stand de 0, 30 e 60 min. Informação perfeita na agenda, com recarga de 30 e de 0 min | Variar um fator por vez a partir do caso-base. Preservar as demais etapas do turnaround |

## D4.5 · Medir desempenho e explicar o mecanismo

**D4.5 refeita em 25/11/2026 (v2.2).** O analisador produziu 1.332 resumos de célula e 79 contrastes, com 30 réplicas válidas. Contrastes principais só na família de referência. A síntese é gerada a partir das tabelas, sem números escritos no código, e inclui o balanço por demanda e a conformidade ao limite do balcão. A espera pelo horário mínimo deixou de existir; o bloqueio restante do stand é disputa de rota ou TLOF.

**Primeira análise, 24/11/2026 (v2.1, substituída).** O analisador versionado em `scripts/d4_analise.py` produziu
1.632 resumos de célula e 82 contrastes, todos com 30 réplicas válidas. As tabelas de máquina
estão em `data/d4/resumo_celulas_d4_5.csv` e `data/d4/contrastes_d4_5.csv`; a leitura com
sentidos, intervalos, populações e limites está em
[`data/d4/sintese_d4_5.md`](../data/d4/sintese_d4_5.md). A análise mantém as médias
condicionais ao lado de seus denominadores e de recusas, desvios e pendências. Os 70 testes passam.
Esses arquivos são a fonte quantitativa para a redação da D4.6 e do resumo AERO2027.

| Resultado | Cálculo e leitura |
|---|---|
| Partidas e atendimento da demanda | Decolagens observadas por hora e por pedido oferecido. Exibir ao lado cancelamentos, recusas (agenda), desvios (FCFS) e pendências para detectar seleção pela admissão |
| Atraso e pontualidade | Medir atraso em relação ao horário solicitado de partida. Informar partidas dentro da tolerância sobre decolagens observadas e o tamanho desse denominador |
| Serviço ao passageiro | Por estação, apresentar espera até início do serviço, conformidade ao limiar da D2, denominador, esperas censuradas e saídas por recusa. Para bagagem, apresentar a espera. Calcular a espera do fim da inspeção ao início do embarque (média e P95, VAR-045), com o número de embarcados e perdidos. O P95 chegada–início do embarque saiu da comparação na v2.2 |
| Retenção pelo grupo | Por voo, comparar o instante em que o último confirmado fica pronto com o instante em que a aeronave fica pronta para embarque. Relatar a fração de voos retidos e a duração da retenção. Verificar se B2 reduz a retenção e se a espera se desloca entre estações |
| Gargalo | Confrontar ocupação física por recurso, tempo bloqueado e filas com os instantes de prontidão do grupo e da aeronave. Verificar se acrescentar o stand reduz o bloqueio e se a espera se desloca para outro recurso |

Calcular cada diferença dentro da réplica e resumir as diferenças entre réplicas com média e intervalo de confiança de 95%. Declarar o sentido da subtração nas tabelas. Se uma réplica terminar sem decolagens ou embarques, registrar o indicador condicional correspondente como indefinido e informar quantos pares permitem estimá-lo. Preservar essa réplica na análise de partidas/h.

## D4.6 · Redigir e conferir a entrega

**D4.6 refeita em 25/11/2026 (v2.2).** A seção de resultados foi reescrita com as rodadas da v2.2. Inclui a tabela por demanda que acompanha a figura, o traço de eventos (`data/d4/traco_d4_6.md`, gerado por `scripts/d4_traco.py`), a conformidade ao limite do balcão, a espera após a inspeção e o confronto com D029.

**Primeira redação, 24/11/2026 (v2.1, substituída).** `sections/results.tex` foi substituído pelo relato das rodadas
executadas, com a figura de vazão por demanda, tabelas de balanço e efeitos, denominadores,
sensibilidades e limites. A seção foi incluída em `main.tex`. O resumo AERO2027 recebeu os
resultados arquivados; permanecem pendentes apenas dados humanos de autoria, afiliação e
biografia. Manuscrito e resumo compilam sem avisos e o pacote do Overleaf foi atualizado.

1. Abrir a seção com uma tabela de cenários, horizonte, demanda oferecida e réplicas. Apresentar os efeitos das duas intervenções com estimativas, unidades e intervalos.
2. Selecionar uma figura que relacione partidas/h à demanda e uma tabela que mostre, para os mesmos cenários, recusas, pendências e espera no terminal. Usar um traço de eventos para explicar um bloqueio identificado nas réplicas.
3. Confrontar o mecanismo observado com o bloqueio por estacionamento em D001, com a alocação de recursos em D026 e D029 e com a comparação entre um e dois balcões de Feldhoff 2022, usando as fronteiras documentadas na [síntese da D3](../data/d3/sintese_mecanismos.md). Explicar convergências ou divergências e indicar em quais condições uma mudança de política ou infraestrutura teria implicação operacional.
4. Integrar a seção ao manuscrito, recompilar e reproduzir cada tabela e figura a partir dos resultados arquivados. Encerrar quando cada afirmação quantitativa puder ser ligada ao cenário, denominador e incerteza correspondentes.

## Estrutura da seção e passagem ao piloto

O [roteiro de redação em LaTeX](../sections/results.tex) organiza os contrastes em quatro configurações sob duas políticas. O contraste de estacionamento compara 5 e 4 stands, cada um com seu carregador. Os contrastes do terminal acrescentam um balcão ou um posto de inspeção com os stands fixos. Esse posto adicional de inspeção corresponde à hipótese da D3.

Ao fechar cada fase da D4, registrar o alcance do que foi verificado e revisar as implicações para a D2 e a D3 antes de iniciar a fase seguinte. A D4 está concluída; a próxima entrega do manuscrito é a D5.
