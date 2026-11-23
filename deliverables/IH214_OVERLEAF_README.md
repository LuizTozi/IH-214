# IH-214 — manuscrito incremental para Overleaf

Envie este ZIP como novo projeto no Overleaf. O arquivo principal é `main.tex`; a bibliografia usa BibTeX e `plainnat`. O PDF local foi compilado com pdfLaTeX, BibTeX e duas passagens adicionais de pdfLaTeX.

Esta versão contém somente os blocos D2 e D3. A D2 reúne desenho operacional e resultados de verificação sintética em `sections/model_and_design.tex` e `sections/verification_results.tex`. A D3 contém a base teórica em `sections/theoretical_basis.tex`. Introdução, discussão, conclusão, resumo e palavras-chave serão incorporados apenas quando suas etapas forem trabalhadas.

Ao obter um novo resultado da D2 ou da D3, atualize a respectiva seção, as fontes de dados ou referências correspondentes e recompile o PDF e o ZIP. Os traços da D2 são sintéticos; experimento comparativo com réplicas e calibração operacional ainda não foram executados.

Os CSVs, o JSON e a matriz de extração em `data/` acompanham o pacote para rastrear entradas do modelo e afirmações da literatura. Eles não são carregados automaticamente pelo manuscrito.

O manuscrito reúne a verificação da D2 e a discussão teórica da D3 sobre estacionamento e inspeção. A especificação da D4.1, versão 2.1, acompanha o projeto como material para revisão em `deliverables/D4_1_cenarios.md`.

## Resumo para o AERO2027

O pacote contém dois documentos principais:

- `main.tex`: o manuscrito do IH-214.
- `aero2027/resumo_aero2027.tex`: o resumo de uma página para o AERO2027 (Amsterdã, 24 a 26/06/2027; prazo em 25/12/2026).

Para compilar o resumo no Overleaf, vá em *Menu → Main document* e escolha `aero2027/resumo_aero2027.tex`. O formato reproduz o modelo oficial (`aero2027/modelo_oficial_AERO2027.docx`):

- Times New Roman, página única A4, margens de 2,54 cm;
- título em 14 pt, negrito e centralizado; autores em 12 pt; afiliações em 11 pt, itálico;
- texto em 12 pt, entrelinha 1,5, justificado;
- até 6 palavras-chave, referências e biografia de até 150 palavras.

O evento pede o envio final em Word: transponha o texto para o `.docx` oficial sem alterar os estilos. Os trechos em vermelho (`\pendente{...}`) aguardam os resultados da D4 ou dados do autor. As regras de escrita estão em `AGENTS.md` e em `deliverables/EVENTO_AERO2027.md`, no repositório.

