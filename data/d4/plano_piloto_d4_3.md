# D4.3 — Plano do piloto de precisão

Plano congelado em 24/11/2026, antes de observar os resultados do piloto.

## Decisão de continuidade

A instrução de continuar o trabalho a partir do ponto deixado pelo Claude preserva, para o
piloto, a interpretação da execução agendada verificada na D4.2: os horários planejados são
mínimos e definem prioridade entre solicitações prontas; um compromisso ainda não pronto não
bloqueia os seguintes. Essa é uma decisão do modelo, não uma validação empírica da regra.

## Escopo

- Cenário: família `referencia`, 6 pedidos/h no período de oferta, recarga de 30 min e janela
  terminante de 8 h, iniciada com recursos livres e filas vazias.
- Configuração-base: 5 stands, 1 balcão, 1 estação de bagagem e 1 posto de inspeção.
- Piloto: 30 réplicas independentes, com sementes inteiras de 10001 a 10030, inclusive.
- Pareamento: todas as células de uma réplica usam o mesmo dia oferecido, manifesto, chegadas e
  durações.
- Separação das rodadas: as sementes do piloto não integrarão as estimativas definitivas. As
  rodadas finais usarão sementes a partir de 20001, depois que o tamanho for fixado.

## Contrastes usados no dimensionamento

As diferenças são calculadas dentro de cada réplica. O piloto dimensionará pelas sete estimativas
abaixo, que cobrem os quatro tipos de contraste principal nas políticas em que se aplicam:

| Tipo | Diferença | Indicador | Unidade |
|---|---|---|---|
| Política | Agenda menos FCFS, na Base | Decolagens por hora | decolagens/h |
| Estacionamento | Base menos S4, sob FCFS | Decolagens por hora | decolagens/h |
| Estacionamento | Base menos S4, sob agenda | Decolagens por hora | decolagens/h |
| Balcão | B2 menos Base, sob FCFS | Espera média no balcão | s |
| Balcão | B2 menos Base, sob agenda | Espera média no balcão | s |
| Inspeção | I2 menos Base, sob FCFS | Espera média na inspeção | s |
| Inspeção | I2 menos Base, sob agenda | Espera média na inspeção | s |

## Precisão escolhida antes do piloto

- Decolagens: semilargura de 0,25 decolagem/h, equivalente a dois voos na janela de 8 h.
- Espera média: semilargura de 30 s, equivalente a um sexto do limite sintético de 180 s usado
  para balcão e inspeção.

Essas margens são escolhas operacionais dos autores para este cenário sintético; não são valores
empíricos nem são atribuídas às fontes da D3.

Para cada contraste, o desvio-padrão amostral das diferenças pareadas no piloto será `s`. O número
planejado será

`ceil((t_0.975,29 * s / h)^2)`,

em que `h` é a semilargura escolhida. O experimento definitivo usará o maior número entre as sete
estimativas e 30 réplicas. O relatório registrará também a semilargura efetivamente obtida no
piloto. Médias condicionais sem observação completa em alguma célula serão mantidas como
indefinidas e terão o número de pares válidos informado; decolagens/h permanecerá definido em
todas as réplicas.

