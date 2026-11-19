# D3 · Protocolo de escopo e elegibilidade

**Passo 1 do Methodi Ordinatio · versão 1.1 fixada para o piloto · 19 de novembro de 2026**

## Intenção da revisão

**Pergunta operacional.** Em um vertiporto de passageiros, como variam as partidas de eVTOL por hora, a espera dos passageiros e o cumprimento dos limites de espera por estação quando se altera (a) o número de posições ou postos que podem atender simultaneamente ou (b) a regra de alocação desses mesmos recursos, comparando agendamento com atendimento por ordem de solicitação?

Esta formulação operacionaliza a pergunta provisória da D1. A unidade de análise é a operação local de um vertiporto genérico durante uma janela definida. A unidade de seleção bibliográfica é o estudo. A unidade de extração é o mecanismo ou a comparação que o estudo sustenta. Uma publicação pode sustentar mais de um mecanismo.

| Termo na revisão | Como reconhecer na D2 ou em uma fonte |
|---|---|
| Capacidade de atendimento simultâneo | Identificar o recurso, sua unidade e sua quantidade disponível. No lado ar, posições de pouso/decolagem, trechos de táxi com ocupação exclusiva, stands e posições de recarga. No terminal, postos de check-in, bagagem e inspeção. Uma pessoa adicional só altera essa capacidade quando torna possível outro atendimento simultâneo. |
| Política de alocação | Identificar qual pedido obtém qual recurso e quando. No agendamento, a admissão depende de janela e reserva compatíveis. Em FCFS, a ordem local segue o instante da solicitação. Escalas de trabalho e gestão de equipes ficam fora da pergunta. |
| Sincronização | Identificar eventos que precisam coincidir ou terminar antes de outra operação. Para embarcar, passageiro apto, aeronave pronta e gate disponível. Para partir, grupo embarcado, despacho e recursos de saída disponíveis. Na comparação principal, essas dependências valem para ambas as políticas. |
| Desempenho | Contar decolagens observadas por hora, medir a espera de fila por estação e o tempo individual da chegada ao terminal até o início do embarque. No LoS temporal, usar como denominador as visitas com espera observável em cada estação com limiar definido. Registrar também recusas, pendências e censura para interpretar as diferenças entre políticas. |

**Dois contrastes.** Para estudar capacidade, variar um recurso e conservar política, demanda, tempos de serviço e demais recursos. Para estudar alocação, manter configuração, pedidos, manifesto, durações e horizonte e variar a política. Um estudo que altera os dois fatores juntos informa o resultado do conjunto. Para identificar interação, comparar a diferença entre políticas em pelo menos duas configurações equivalentes nos demais fatores. Uma melhora no lado ar e uma piora no lado terra constituem um possível trade-off a investigar. A extração também admite melhora simultânea, ausência de diferença ou efeito incerto.

## Critérios para a triagem

- **Incluir como contribuição acadêmica** estudo identificável com método ou argumento verificável que sustente ao menos um eixo: filas e sincronização, operações em vertiportos, processamento de passageiros ou medição de qualidade de serviço. Registrar recurso, regra, mecanismo ou definição de métrica transferível. Estudos que medem um só lado contribuem para esse eixo. Para afirmar efeito conjunto, exigir evidência dos dois lados sob condições comparáveis.
- **Incluir como fundamento**, quando pertinente, teoria clássica de filas ou estudo de terminal aeroportuário que explicite hipóteses e fronteiras de medição. Registrar condições de transferência. Estudos de satisfação podem fundamentar a distinção entre percepção declarada e espera medida. A D2 mede a segunda.
- **Registrar à parte** regulamentos, especificações e conceitos de operação por autoridade, versão, dispositivo e decisão que esclarecem. Uma regra de exclusividade delimita o uso de uma posição. Uma duração numérica requer fonte própria.
- **Excluir da síntese operacional** trabalho exclusivamente sobre rota, espaço aéreo, energia de missão, dimensionamento de bateria, escala de pessoal ou demanda de rede sem mecanismo local transferível. Aplicar a exclusão de sítio já definida pelo autor. Outros estudos de caso podem contribuir quando o mecanismo for separável do local.
- Em título ou resumo insuficiente, encaminhar à leitura integral. Documentar indisponibilidade separadamente da exclusão temática. Relacionar versões de congresso e periódico do mesmo estudo e extrair cada resultado uma vez. A posição bibliométrica ordena os elegíveis para leitura.

## Casos de fronteira para os revisores

| Situação | Decisão de extração |
|---|---|
| O artigo chama de capacidade o máximo de voos/h sob um limite de atraso. | Incluir se pertinente e registrar demanda, política e critério de atraso. Classificar voos/h como capacidade operacional estimada pelo artigo, separada da contagem de posições que entra no modelo. |
| Um segundo agente entra no mesmo balcão e reduz a duração do serviço. | Registrar mudança de tempo de atendimento. Só registrar posto adicional se houver dois atendimentos simultâneos. |
| O cenário agendado acrescenta um stand ou admite menos pedidos, e a espera média cai. | No primeiro caso, registrar alteração conjunta. No segundo, verificar demanda oferecida, recusas e população da média antes de atribuir a diferença à alocação. |
| Uma simulação muda apenas a duração de carga, mantendo um carregador. | Extrair como duração de serviço que altera ocupação e bloqueio. Preservar a quantidade do recurso no registro. |
| O artigo informa atraso de aeronaves e omite dados de passageiros. | Incluir a contribuição do lado ar e marcar o desfecho do passageiro como não medido. |

Para cada decisão guardar identificador, eixo, decisão e motivo. Para cada comparação elegível guardar recurso e unidade, fator alterado, condições fixas, demanda oferecida e admitida quando disponível, desfechos de cada lado, fronteira temporal, tipo de evidência, página e vínculo com a D2. Codex e Claude registrarão suas classificações separadamente na triagem. Divergências serão confrontadas com o texto original.

**Revisão do escopo com Claude.** Na extração registrar também margens de reserva, utilização (com denominador), limiar e população de cada indicador de LoS. Uma margem maior restringe a disponibilidade temporal mesmo quando o número físico de posições permanece constante. Um trade-off entre os lados pode aparecer em um único contraste que meça ambos os desfechos; o cruzamento de configurações e políticas responde à pergunta adicional sobre interação.

**Base documental.** [Questão do orientador e discussão de escopo](../codex-session-01a1eec0-4a69-71d2-94a8-5bba751b6315.md), trecho de 18 de novembro às 11h45. [Pergunta provisória da D1](D1_framing.md). [D2 encerrada no commit 8d508bf](D2_model_design.md). [Protocolo dos cenários](../data/scenario_protocol.md).

## Verificação de aplicabilidade e encerramento do passo 1

Aplicação dos critérios a seis registros já descritos na [matriz da D1](../data/literature_matrix.csv). As decisões abaixo documentam o uso pretendido de cada fonte e os limites da inferência. A seleção definitiva do portfólio ocorrerá após as buscas e a triagem.

| Registro | Decisão segundo o protocolo | Fronteira da contribuição |
|---|---|---|
| LIT-009 · Vascik e Hansman | Incluir no eixo de operações para explicar como posições e topologia condicionam o fluxo. | O envelope de capacidade é um resultado do modelo. Registrar separadamente as quantidades de posições usadas como entradas. |
| LIT-004 · Guerreiro et al. | Incluir no eixo de operações para fundamentar a alocação FCFS e seus gargalos. | Um cenário FCFS, sozinho, não estima o efeito de substituí-lo por agendamento. |
| LIT-002 · Feldhoff | Incluir no eixo de processamento para definir filas, postos e conformidade com limites de espera. | A contribuição é do terminal. Atribuir uma variação às partidas exige uma ligação demonstrada com o lado ar. |
| LIT-020 · Escribano Macias et al. | Incluir como fundamento de redes de filas pelo mecanismo de dimensionamento e utilização de servidores. | A espera de aeronaves tem população e marcos distintos da espera dos passageiros. |
| LIT-017 · Bennaceur et al. | Incluir como fundamento de qualidade de serviço para interpretar espera e diferenças entre classes. | Uma medida de espera na rede só é comparável à espera de uma estação se população e eventos inicial e final forem compatíveis. |
| LIT-013 · EASA | Registrar na trilha documental para caracterizar recursos físicos e sua disposição. | A especificação protótipo fundamenta restrições de projeto. Para quantificar um efeito sobre filas ou partidas é necessária evidência adicional. |

**Regra de manutenção.** A pergunta, a unidade de análise e os critérios acima constituem a referência de elegibilidade anterior às buscas. Qualquer ajuste decorrente do piloto terá data, justificativa e indicação dos registros que precisam ser reavaliados.
