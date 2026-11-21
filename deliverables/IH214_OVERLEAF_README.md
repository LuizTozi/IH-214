# IH-214 — manuscrito incremental para Overleaf

Envie este ZIP como novo projeto no Overleaf. O arquivo principal é `main.tex`; a bibliografia usa BibTeX e `plainnat`. O PDF local foi compilado com pdfLaTeX, BibTeX e duas passagens adicionais de pdfLaTeX.

Esta versão contém somente os blocos D2 e D3. A D2 reúne desenho operacional e resultados de verificação sintética em `sections/model_and_design.tex` e `sections/verification_results.tex`. A D3 contém a base teórica em `sections/theoretical_basis.tex`. Introdução, discussão, conclusão, resumo e palavras-chave serão incorporados apenas quando suas etapas forem trabalhadas.

Ao obter um novo resultado da D2 ou da D3, atualize a respectiva seção, as fontes de dados ou referências correspondentes e recompile o PDF e o ZIP. Os traços da D2 são sintéticos; experimento comparativo com réplicas e calibração operacional ainda não foram executados.

Os CSVs, o JSON e a matriz de extração em `data/` acompanham o pacote para rastrear entradas do modelo e afirmações da literatura. Eles não são carregados automaticamente pelo manuscrito.
