# IH-214 — manuscrito incremental para Overleaf

Envie este ZIP como novo projeto no Overleaf. O arquivo principal é `main.tex`; a bibliografia usa BibTeX e `plainnat`. O PDF local foi compilado com pdfLaTeX, BibTeX e duas passagens adicionais de pdfLaTeX.

Esta versão contém os blocos D2 a D4. A D2 reúne desenho operacional e resultados de verificação sintética em `sections/model_and_design.tex` e `sections/verification_results.tex`. A D3 contém a base teórica em `sections/theoretical_basis.tex`. A D4 apresenta os experimentos pareados, seus denominadores e limites em `sections/results.tex`, com três figuras vetoriais em `figures/` (vazão por demanda, contrastes pareados e deslocamento da espera), geradas no repositório por `figures/gen_fig_d4_*.py` a partir dos CSVs de `data/d4/`. Introdução, conclusão, resumo e palavras-chave do manuscrito serão incorporados quando a D5 for trabalhada.

Ao alterar uma seção, atualize as fontes de dados ou referências correspondentes e recompile o PDF e o ZIP. Os traços da D2 e os experimentos da D4 são sintéticos. O piloto da D4.3 não foi combinado às 30 réplicas definitivas. As tabelas reproduzíveis de célula e contraste acompanham o pacote em `data/d4/`.

Os CSVs, o JSON e a matriz de extração em `data/` acompanham o pacote para rastrear entradas do modelo e afirmações da literatura. Eles não são carregados automaticamente pelo manuscrito.

O manuscrito reúne a verificação da D2, a discussão teórica da D3 e os resultados da D4 sobre política de admissão, estacionamento e balcão. A especificação D4.1 v2.2 acompanha o projeto em `deliverables/D4_1_cenarios.md`; o traço de eventos da D4.6 está em `data/d4/traco_d4_6.md`.

## Resumo para o AERO2027

O pacote contém dois documentos principais:

- `main.tex`: o manuscrito do IH-214.
- `aero2027/resumo_aero2027.tex`: o resumo de uma página para o AERO2027 (Amsterdã, 24 a 26/06/2027; prazo em 25/12/2026).

Para compilar o resumo no Overleaf, vá em *Menu → Main document* e escolha `aero2027/resumo_aero2027.tex`. O formato reproduz o modelo oficial (`aero2027/modelo_oficial_AERO2027.docx`):

- Times New Roman, página única A4, margens de 2,54 cm;
- título em 14 pt, negrito e centralizado; autores em 12 pt; afiliações em 11 pt, itálico;
- texto em 12 pt, entrelinha 1,5 (simulada como no Word), justificado;
- até 6 palavras-chave, referências e biografia. O modelo permite 150 palavras de biografia, mas, com entrelinha 1,5, cabem cerca de 60 sem passar de uma página.

O arquivo `.docx` do modelo está em tamanho Carta e espaçamento simples, embora o texto de instrução peça A4 e 1,5. Convém confirmar com os organizadores.

O evento pede o envio final em Word: transponha o texto para o `.docx` oficial sem alterar os estilos. Os resultados da D4 já foram inseridos. Os trechos em vermelho (`\pendente{...}`) aguardam somente coautores, endereço, e-mail e biografia fornecidos pelo autor. As regras de escrita estão em `AGENTS.md` e em `deliverables/EVENTO_AERO2027.md`, no repositório.

## Artigo completo em inglês (rascunho)

`aero2027/artigo_en/artigo_aero2027_en.tex` reúne o artigo completo em inglês com a tipografia e a ordem de seções do modelo AERO2027 (o evento exige apenas o resumo; o formato do artigo completo é uma suposição declarada no arquivo). Para compilar no Overleaf, escolha esse arquivo em *Menu → Main document*. As referências estão em `aero2027/artigo_en/referencias_aero.tex`, geradas de `references/references.bib` por `gerar_referencias.py`, e as figuras em inglês são `figures/fig_d4_*_en.pdf`. Trechos em vermelho aguardam dados e aprovação dos autores.
