# IH-214

Repositório privado do artigo sobre teoria de filas aplicada a operações de vertiportos e à experiência de passageiros.

O manuscrito será desenvolvido em LaTeX e organizado por entregáveis. O Vertiporto Sarah não integra o escopo, os dados, o estudo de caso ou as citações do artigo.

## Estrutura

- `main.tex`: ponto de entrada do projeto Overleaf.
- `sections/`: seções do manuscrito quando forem aprovadas.
- `deliverables/`: materiais de planejamento dos cinco entregáveis.
- `references/`: banco bibliográfico BibTeX.
- `data/`: matrizes de literatura, parâmetros e dados que forem autorizados.
- `scripts/`: rotinas reproduzíveis de preparação e análise.
- `figures/`: figuras finais do manuscrito.

Nenhuma pergunta de pesquisa, hipótese ou resultado está fixado neste estágio.

## Ambiente e execução

Os scripts da D4 usam o ambiente Conda `ih214`, descrito em `environment.yml` (Python 3.12 e SimPy).

```bash
conda env create -f environment.yml   # cria o ambiente uma vez
conda activate ih214                  # ativa o ambiente
cd scripts && python -m unittest      # roda todos os testes
```

Experimento da D4: uma linha por célula (48 por réplica), com os dias arquivados.

```bash
cd scripts && python d4_experimento.py --seeds 1 2 3 --out ../data/d4/resultados.csv --days-dir ../data/d4/dias
```

O registro da verificação está em `data/d4/verificacao_d4_2.md`.
O piloto de precisão da D4.3 está em `data/d4/resultado_piloto_d4_3.md`; ele fixou 30 réplicas
independentes para a D4.4, sem combinar as sementes do piloto com o experimento definitivo.
As rodadas definitivas da D4.4 estão em `data/d4/resultados_d4_4.csv`, com os dias arquivados em
`data/d4/dias_d4_4/`. A análise pareada e a redação pertencem à D4.5 e à D4.6.

