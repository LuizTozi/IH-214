# Plano de figuras do artigo

As figuras serão originais e reproduzíveis em LaTeX/TikZ ou geradas a partir de dados de simulação.
Imagens institucionais de Eve ou Joby podem ser consultadas para entendimento, mas não serão
republicadas sem licença explícita.

| ID | Figura | Pergunta que responde | Base | Estado |
|---|---|---|---|---|
| F1 | Rede acoplada passageiro--eVTOL | Onde ocorre a sincronização e quais são os resultados? | D2, EASA, fontes OEM | TikZ criado |
| F2 | Topologia modular regulatória | Quais recursos são exigidos no caso-base? | EASA PTS-VPT-DSN | Após fechar geometria aplicável |
| F3 | Máquina de estados do eVTOL | Como a aeronave transita entre pouso, stand, recarga e partida? | D2 e Schweiger et al. | Após definir regra de recarga |
| F4 | Processo obrigatório do passageiro | Como chegadas, check-in, inspeção e embarque se vinculam ao voo? | D2 e literatura de terminal | Após definir distribuições de serviço |
| F5 | Trade-off operacional | Como capacidade/coordenação alteram throughput, P95 e LoS? | Resultados do DES | Após experimentos |

## Linguagem visual

- Figuras conceituais: TikZ vetorial, paleta legível em impressão e rótulos em inglês no manuscrito.
- Gráficos: Matplotlib em PDF vetorial, paleta Okabe-Ito e intervalos de confiança.
- Rótulos de evidência: “regulatory constraint”, “literature input” e “scenario” quando necessário;
  não apresentar premissa como dado observado.
