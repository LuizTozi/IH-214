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

## Progresso em 25/11/2026 (tarde)

**Decisões do autor:**
- inspeção com ocupação única, reamostrando os tempos observados de Janssen;
- grupos maiores que 4 excluídos e a distribuição renormalizada;
- downloads de material aberto autorizados.

| ID | Fonte encontrada | Dado | Situação |
|---|---|---|---|
| PAR-046 (balcão) | K. Marintseva, Proc. National Aviation University 59(2), 97–104 (2014), DOI 10.18372/2306-1472.59.6799; Tab. 1, p. 100; observação no aeroporto de Boryspil | Balcão convencional (CUTE), por voo, média/DP/n em min: MOW 3,51/4,77/160; ALA 1,92/1,30/60; WAW 1,58/1,03/88; TLL 3,24/3,26/56. A autora conclui que o serviço é exponencial (Fig. 4). Média ponderada pelos 364 passageiros: 164 s. | **Resolvido**: exponencial com média de 164 s (ponderação pelos n da tabela). |
| PAR-054 (forma da chegada) | M. N. Postorino, L. Mantecchini, C. Malandri, F. Paganelli, Transp. Res. Procedia 37, 338–345 (2019), DOI 10.1016/j.trpro.2018.12.201, CC BY-NC-ND; dados do aeroporto de Bologna, 6 voos, semana de pico de inverno | Weibull escolhida pelo teste χ² entre Gauss, Poisson, Gamma e Lognormal (eq. 4, p. 343). Parâmetros da Fig. 4: manhã LCC α = 4, β = 5,3; FC α = 3,7, β = 6,5; tarde LCC α = 5,5, β = 13,4; FC α = 4,1, β = 6,3. | **Pendente**: confirmar a unidade de x (o eixo mostra ESD em horas, mas α = 4 h contradiz o texto). Ler a seção de método do PDF. |
| PAR-053 (ausência) | Lawrence, Hong e Cherrier, Proc. 9th ACM SIGKDD, 397–406 (2003), DOI 10.1145/956750.956796 (citado por terceiros com 6 a 10%) | — | **Pendente**: ler a fonte primária (sem cópia aberta no OpenAlex; testar o CiteSeerX). |
| PAR-045, PAR-048, PAR-043, PAR-044 | — | — | **Pendentes**. |

## Estado ao atingir o limite de uso (25/11/2026)

### Resolvido com fonte

| ID | Novo valor | Fonte |
|---|---|---|
| PAR-047 | Tempo próprio de inspeção reamostrado: média de 127,5 s, CV 0,52, n = 2.389 | `data/fontes/janssen_tempo_proprio.csv`, gerado por `scripts/fontes_janssen.py` |
| PAR-052 | Grupos de 1 a 4: 53,3 / 39,5 / 4,7 / 2,5% | Janssen et al. 2020 |
| PAR-046 | Balcão exponencial, média de 164 s | Marintseva 2014, Tab. 1 |
| PAR-054 | Chegada por Weibull, com ESD = 0,25 (x + 1) h, conferida pelos picos da Fig. 4; truncada em x ∈ [1, x_max] e comprimida linearmente para 15–60 min antes da STD | Postorino et al. 2019 |
| PAR-048 | Separação de 30 s | PAR-029, Preis e Hornung 2022, Tab. 3 e A1 |
| PAR-045 | Ocupação do TLOF na partida de 45 s | Preis e Hornung 2022 (Applied Sciences), §3.2 |
| PAR-043, PAR-044 | Distâncias de 15 m e 60 m mantidas como leiaute de desenho | Conferidas contra o mínimo da FATO da EASA (1,5 D; raio de 11,4 m com a Eve) |

**Perfis de chegada:**
- caso-base: convencional da manhã (α = 3,7, β = 6,5, x_max = 9);
- sensibilidade: baixo custo da tarde (α = 5,5, β = 13,4, x_max = 14).

**Ausência (PAR-053):** 0% no caso-base e 15% na sensibilidade. O valor de 15% é de Smith, Leimkuhler e Darrow (1992), citados por Vojtek et al. 2021, p. 124–125, para voos lotados.

### Próximos passos (não iniciados no código)

1. Reescrever `scripts/d4_dia.py` (versão 1.2 do gerador):
   - novos sorteios por reserva: `absence_u`, `lead_u`, `counter_u` e `security_u`;
   - `family_requests(day, rate, charge, absence=0.0, arrival="fc_morning", std_offset_s=900)`.

   Há um rascunho completo na conversa com o Claude.
2. `d4_param.py`: SEP = 30 000 ms; DEP_OCC = 45 000 ms; COUNTER_DECLARED = 164 000 ms; SECURITY_DECLARED igual à média do conjunto de tempos.
3. `d4_sim.py` e `d4_agenda.py`: janela de toque como parâmetro de `run_cell`, no lugar da constante `WINDOW`.
4. Famílias:
   - manter: referencia, demanda_baixa, demanda_alta, sem_recarga, recarga_longa;
   - acrescentar: ausencia_15, chegada_lcc_tarde, janela_150, janela_600, partida_600, partida_1200;
   - retirar: as de informação perfeita e servico_variavel ("menos é mais").
5. Atualizar os testes (os tempos esperados mudam com a separação e a partida), rodar de novo as 30 réplicas e o analisador.
6. Artigo:
   - foco único em stand ou balcão;
   - conferir se título e resumo correspondem ao texto;
   - parágrafo final comparando com os estudos de referência (Preis e Hornung, Feldhoff, Guerreiro, Onat, Halder e Gandhi);
   - fechar a D5 (*highlights* e periódico-alvo).
