# D3 — síntese dos mecanismos e alcance da evidência

**Fechamento da leitura dirigida, 20/11/2026.** A unidade de comparação da D2 é um vertiporto sintético com demanda oferecida e recursos simultâneos identificados. Uma posição ou posto é entrada do modelo; partidas por hora, atrasos e conformidade temporal são resultados. A matriz de extração registra a versão e o localizador de cada fonte citada abaixo.

| Eixo | Evidência e mecanismo | Transferência à D2 |
|---|---|---|
| Filas e sincronização | Little fixa unidade, fronteira e média de longo prazo. Onat D001 mostra bloqueio da chegada quando falta estacionamento. D002 calcula filas de **aeronaves** em pads de pouso, recarga, armazenamento e decolagem sob regime estacionário de pico, reconhecendo que a demanda diária pode ser bimodal. | Identificar em cada fila quem espera e os dois eventos que delimitam a espera. A D2 usa janela terminante; recusas e pendências são relatadas além das médias. A estacionariedade e os tempos de D002 não são presumidos na D2. |
| Operações de vertiporto | Guerreiro D026 reserva recursos em linhas de tempo sob FCFS e mostra gargalos físicos distintos. D029 compara FCFS com reordenação de partidas em redes de três e quatro vertiportos com infraestrutura fixa; mede voos concluídos e ociosidade. Wille D003 mostra que prioridade pode alterar distribuição dos atrasos sem mudança comparável da capacidade prática. Preis e Hornung D023 condicionam a capacidade prática a uma configuração e a um limiar de atraso. | Separar contagem de posições da regra que aloca pedidos. Reserva técnica depois do pedido (D026), reordenação de partidas (D029), prioridade energética (D003) e **admissão antecipada** (D2) são políticas distintas. Não transportar os ganhos ou a capacidade operacional das fontes como parâmetros. |
| Processamento de passageiros e ligação ao lado ar | NUAIR/NASA LIT-008 vincula abertura do gate à aeronave; Saxena D021 vincula prontidão à conclusão do embarque. Preis e Hornung D036 já acoplam pad/gate e atraso agregado do passageiro, inclusive espera no terminal por aeronave. Preis S4382766441 relaciona lotação e simultaneidade a passageiros/h. D029 representa processamento no lounge, mas mede voos e ociosidade; o texto explicita simplificações de tempos de embarque/desembarque. | A lacuna investigada é estreita: fila **por estação** do terminal, prontidão do grupo e retenção do stand, com desfechos dos dois lados sob contrastes controlados. D036 impede alegar ausência geral de acoplamento entre aeronave e passageiro. A ocupação dos assentos e as regras de sincronização permanecem explícitas. |
| Qualidade de serviço | Feldhoff S4283220962 diferencia espera na estação, tempo de percurso e excedências; Bennaceur D052 mede intervalo agregado chegada–partida; Qin W7171717774 liga capacidade e congestionamento à escolha de horário no resumo do editor. D040/D044 tratam construtos subjetivos por instrumentos próprios. | Reportar denominador, marcos e limiar de cada medida. O LoS temporal da D2 é proporção de visitas observáveis sob o limite da estação; a espera chegada–embarque é outro indicador. Nenhuma dessas medidas, isoladamente, estima satisfação declarada. Qin fundamenta apenas escopo, pois o texto integral não foi obtido. |

## Conclusão argumentativa para a seção teórica

Há evidência anterior tanto de gargalos físicos quanto de efeitos de políticas sob recursos fixos; D029 é uma comparação direta de FCFS com sequenciamento alternativo. Há também evidência anterior de ligação entre operações de pad/gate e atraso de passageiros (D036). A contribuição investigável da D2 é combinar **os dois contrastes definidos no protocolo** com a observação local das filas de passageiros, o instante de prontidão do grupo, a retenção do stand e as partidas, mantendo população e condições de comparação explícitas. Essa formulação descreve um recorte analítico, não reivindica exclusividade ou superioridade empírica.

O modelo e os traços da D2 são sintéticos e foram estipulados pelos autores. O desenho dos experimentos posteriores deve emparelhar pedidos, duração de serviço, manifesto, horizonte e configuração entre políticas; variar um recurso por vez para o contraste de atendimento simultâneo; registrar recusas, pendências e o denominador efetivamente observado. O sinal de cada efeito, inclusive um possível deslocamento da espera entre estações do terminal ou para a sala de embarque, é hipótese de teste. Na D4.1 v2.1, esse deslocamento é observável pelos contrastes de servidor no balcão e na inspeção.

## Repercussão da D4.1 · 23/11/2026

A versão 1 da D4.1 não observava a lacuna desta síntese. As filas do terminal eram iguais em todas as configurações, e o grupo ficava pronto antes da aeronave sempre que havia recarga. A versão 2 alinha o experimento à lacuna com quatro escolhas:

- **Contrastes de servidor no terminal:** um segundo balcão e um segundo posto de inspeção, avaliados um por vez.
- **Recusa comunicada na decisão:** a política passa a alterar a carga das estações.
- **Chegadas entre 15 e 60 min antes da partida programada:** janela de Feldhoff S4283220962. A forma uniforme é suposta.
- **Escala de 1 TLOF e 5 stands:** topologia da mesma fonte.

Transferências e seus limites:

- **D001** fundamenta o bloqueio de chegada por falta de posição no contraste de 5 contra 4 stands.
- **Feldhoff** compara um e dois balcões sem lado ar e atribui a espera baixa na inspeção ao atraso no balcão (p. 10). A D4 testa essas comparações com o acoplamento ao stand.
- **Topologia de 5 stands:** veio de uma análise com turnaround de 300 s (Ref. [8] da fonte, LIT-009). Transfere-se a topologia, não a conclusão sobre eficiência.
- **Recursos por stand:** o carregador e o gate próprios de cada stand são hipótese do modelo.

O deslocamento da espera entre estações e a retenção do stand pelo grupo continuam hipóteses de teste.

## Repercussão da D4 (v2.2) · 25/11/2026

As rodadas definitivas ([síntese D4.5](../d4/sintese_d4_5.md)) testaram as hipóteses desta síntese no cenário sintético:

- **Deslocamento da espera:** observado. O segundo balcão reduziu a espera no balcão e aumentou a espera depois da inspeção, à espera da aeronave na sala de embarque, além de criar pequenas esperas na bagagem e na inspeção. Isso é coerente com a explicação de Feldhoff (p. 10) para a espera baixa nas estações seguintes ao balcão.
- **Retenção pelo grupo:** diminuiu com o segundo balcão, sem ganho de vazão comparável.
- **Servidor adicional na inspeção:** retirado das hipóteses. Com serviços determinísticos e um balcão mais lento que a inspeção, não se forma fila na inspeção; o contraste não testava a hipótese.
- **Política sob recursos fixos:** a admissão antecipada ficou ligeiramente abaixo do FCFS em decolagens com passageiros. D029 (Halder e Gandhi) encontrou ganho de um sequenciamento por regras sobre o FCFS, mas com outra regra: reordena partidas, não admite pedidos antecipadamente. As duas evidências não se contradizem; mostram que o efeito depende da regra comparada.
- **Bloqueio por estacionamento (D001):** observado no contraste de 5 contra 4 stands, com o traço de eventos em `data/d4/traco_d4_6.md`.
