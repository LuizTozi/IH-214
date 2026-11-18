# Deliverable 1 — enquadramento e evidências iniciais

## Situação

Em desenvolvimento. Este arquivo registra o enquadramento de pesquisa; não é uma seção do
manuscrito.

## Tema de trabalho

Teoria de filas aplicada à operação de vertiportos de passageiros e à relação entre desempenho
operacional de eVTOLs e nível de serviço percebido pelo passageiro.

## Pergunta de pesquisa

**RQ-v0 (provisória):** como a capacidade e a coordenação de recursos de um vertiporto afetam,
simultaneamente, o fluxo de eVTOLs e as métricas de espera e nível de serviço dos passageiros?

Esta formulação será revisada após a triagem do acervo e antes do fechamento do Deliverable 1.

## Síntese por decisão de modelagem e hipótese de lacuna

O acervo agora permite separar quatro decisões que precisam coexistir no modelo, sem apresentar
as fontes em sequência autor a autor:

1. recursos airside, stand, recarga e bloqueios determinam a capacidade e o atraso da aeronave;
2. chegada, processamento e embarque determinam a espera no terminal e o nível de serviço;
3. reserva, slots e balanceamento demanda--capacidade acoplam a rede externa ao estado local do
   vertiporto; e
4. espera percebida, confiabilidade e equidade podem alterar a resposta da demanda, não sendo
   apenas indicadores operacionais após a simulação.

As fontes regulatórias delimitam a geometria, segurança e coordenação admissíveis, mas não
oferecem tempos de serviço, limites de LoS ou métricas de satisfação. Assim, elas devem impor
restrições de cenário, e não calibrar filas ou comportamento de passageiros.

A hipótese de lacuna é que o acoplamento ainda é incompleto quando é preciso representar, ao
mesmo tempo, disponibilidade de stand/gate, recarga, reserva de recurso, atraso do eVTOL e uma
medida passageiro-cêntrica de espera percebida ou LoS. Ela é sustentada, mas ainda deve ser testada,
por estudos que tratam predominantemente a rede/recursos (por exemplo, `preisHornung2022`,
`escribanoMacias2023` e `onat2024`), por estudos que isolam processamento terminal
(`feldhoff2022`) e por estudos que tratam QoS/percepção fora do processo terminal
(`bennaceur2022` e `chen2024`).

Essa hipótese será testada, e não assumida como contribuição, nas leituras em texto completo que
vão definir o recorte final do modelo.

## Próximas referências a perseguir (somente se alterarem a modelagem)

- validação empírica de tempos de turnaround, carregamento e processamento de passageiros;
- medidas transferíveis de satisfação/valor do tempo aplicáveis a espera em mobilidade sob demanda;
- estudos que acoplem explicitamente operação airside, terminal e resposta comportamental.

## Critérios de fechamento

1. Matriz com 20 fontes pertinentes e rastreáveis. **Atendido.**
2. Cinco ou mais referências centrais validadas em texto completo ou fonte primária. **Atendido**
   (fontes acadêmicas lidas nas seções metodológicas/resultados e cinco documentos oficiais).
3. Cobertura dos cinco eixos definidos em `data/search_log.md`. **Atendido.**
4. Pelo menos uma lacuna explicitada e sustentada por três fontes. **Atendido como hipótese a
   testar, não como alegação definitiva.**
5. Referências selecionadas registradas em `references/references.bib` com metadados conferidos.
   **Atendido.**

## Decisão de fechamento

**Deliverable 1 concluída em 18 de novembro de 2026.** O próximo passo é fixar a fronteira do
modelo e a estratégia de dados no Deliverable 2; novas fontes entram apenas pela rotina de
evidências quando puderem mudar uma hipótese, parâmetro ou critério de validação.
