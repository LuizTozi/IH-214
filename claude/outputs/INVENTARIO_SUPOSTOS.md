# Inventário dos valores supostos e plano de resolução (Claude), 25/11/2026

**Regra do autor (25/11/2026).** Nenhum valor pode ficar suposto. O que estiver na literatura vem da literatura; o que não estiver é criado a partir de dados (análise própria), com o procedimento registrado.

**Duas classes de entrada.**
- **Grandezas empíricas:** tempos, proporções, distribuições. Precisam de fonte ou de derivação a partir de dados.
- **Fatores de desenho do experimento:** níveis de demanda, número de stands, janela de observação, regras de política. São escolhas do experimento, não suposições sobre o mundo. Precisam de justificativa e, quando influenciam o resultado, de análise de sensibilidade. Não se "resolvem" com dados.

## A. Grandezas empíricas

| ID | Grandeza | Valor atual | Estado | Resolução |
|---|---|---|---|---|
| PAR-047, PAR-063 | Serviço da inspeção e sua variabilidade | 90 s determinístico; exponencial como limite | **Dados obtidos** | Janssen et al. 2020, dados abertos (4TU, CC BY 4.0), 2.402 passageiros. Tempo total por passageiro de 179,1 s, igual ao relatado no artigo (validação da leitura). Falta a decisão do autor sobre a transferência (ver abaixo). |
| PAR-052 | Reservas por pedido | 1 a 4, uniforme | **Resolvido pelos dados** | Grupos de viagem observados por Janssen et al., condicionados a até 4 assentos: 1 = 53,3%; 2 = 39,5%; 3 = 4,7%; 4 = 2,5%. Grupos maiores que 4 reúnem 3,5% dos passageiros. Média de cerca de 1,6 contra 2,5. |
| PAR-046 | Serviço do balcão | 180 s determinístico | **Aberto** | Não há dado no projeto além dos limites de Felix 2015 (40 a 60 s, sem distribuição). Buscar dados de tempo de atendimento no balcão (estudos de campo ou dados abertos); se não houver, derivar de Felix por análise própria. |
| PAR-054 | Forma da chegada antes da partida | Uniforme em 15 a 60 min | **Aberto** | Feldhoff usa uma beta sem publicar os parâmetros. Pedir os parâmetros à autora ou buscar dados abertos de antecedência de chegada (estudos de aeroporto); ajustar a distribuição. |
| PAR-053 | Probabilidade de ausência | 0,10 | **Aberto** | Buscar taxas de *no-show* publicadas (aviação comercial ou serviços sob demanda). |
| PAR-045 | Ocupação do TLOF na partida | 50 s | **Aberto** | Buscar nas fontes do lado ar (Preis e Hornung, Tab. A1; Wille; Vascik e Hansman). |
| PAR-048 | Separação após a saída do TLOF | 3 s | **Aberto** | Idem; ou norma (FAA EB-105A, EASA PTS). |
| PAR-043, PAR-044 | Distâncias no solo (15 m e 60 m) | Do autor | **Aberto** | Derivar da geometria da EASA PTS-VPT-DSN para a aeronave de referência (dimensões publicadas da Eve e da Joby). |

## B. Fatores de desenho

| ID | Fator | Valor | Tratamento proposto |
|---|---|---|---|
| PAR-050 | Janela de observação | 8 h | Justificar e manter. |
| PAR-051 | Demanda | 4, 6 e 8 pedidos/h | Já variada. |
| PAR-055 | Janela de toque | 300 s | Justificar pela janela de reserva do ConOps da NASA (§5.2.1.2) e criar uma família de sensibilidade. |
| PAR-056 | Deslocamento da partida programada | 900 s | Justificar pelo requisito de chegada de 15 min (Feldhoff; BLADE) e criar uma família de sensibilidade. |
| PAR-057 | Carregador e gate próprios por stand | — | Escolha de desenho: isola as perguntas estudadas. Manter declarada. |
| PAR-049 | Tolerância de pontualidade | 60 s | Indicador secundário; justificar. |

## Decisões do autor necessárias

1. **Transferência da inspeção.** Os dados de Janssen vêm de faixas de aeroporto com processamento em paralelo. O posto do vertiporto pode ser modelado como:
   - **(a) Ocupação única:** um passageiro por vez; serviço = tempo próprio de entrega, detector e retirada, reamostrado dos dados (média de cerca de 125 a 130 s).
   - **(b) Faixa em paralelo:** serviço efetivo = intervalo entre saídas com fila, de cerca de 16 a 23 s.
2. **Grupos maiores que 4.** Excluí-los e renormalizar (proposta), ou dividi-los em mais de um pedido.
3. **Autorização de downloads.** Baixar os artigos e dados abertos necessários para os itens em aberto.

## Saídas já geradas

- `scripts/fontes_janssen.py` (reprodutível; lê `data/raw/janssen2020/`, fora do Git, conferido pelo MD5).
- `data/fontes/janssen_servico_inspecao.csv`, `janssen_intervalos_inspecao.csv` e `janssen_tamanho_grupo.csv`.
