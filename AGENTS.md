# AGENTS.md — IH-214

Instruções do projeto para agentes (Codex, Claude Code e outros). Complementam o `AGENTS.md` geral do usuário.

## Destino do trabalho

O artigo será submetido ao **AERO2027 — World Summit on Aerospace and Aeronautical Engineering** (Amsterdã, 24 a 26 de junho de 2027), eixo *Urban Air Mobility & eVTOL Technologies*, subtema *Smart Air Mobility Infrastructure*.

- **Prazo do resumo:** 25/12/2026.
- **Detalhes e lacunas** (anais, indexação e avaliação não informados pelo evento): `deliverables/EVENTO_AERO2027.md`.

São dois produtos:

1. **O manuscrito do IH-214** (`main.tex`, `sections/`), organizado pelas entregas D1 a D5.
2. **O resumo do evento** (`aero2027/resumo_aero2027.tex`), em uma página, no formato oficial abaixo.

## Formato oficial do resumo (obrigatório)

Fonte: modelo do evento em `aero2027/modelo_oficial_AERO2027.docx`, que deve ser seguido sem alterar os estilos. Resumos fora do formato são devolvidos.

**Página e arquivo**
- Uma página A4, margens normais (2,54 cm), em inglês, contando figuras e tabelas.
- Envio em Word, com os estilos do modelo. O `.tex` serve à redação no Overleaf; a versão final é transposta para o `.docx`.

**Tipografia** (sempre Times New Roman)

| Elemento | Formato |
|---|---|
| Título | 14 pt, negrito, centralizado, Iniciais Maiúsculas Em Cada Palavra |
| Autores | 12 pt, separados por vírgula; afiliação por número sobrescrito; correspondente com "*"; apresentador sublinhado |
| Afiliações | 11 pt, itálico |
| Texto | 12 pt, entrelinha 1,5, justificado nas duas margens |

**Ordem das seções**
1. Título.
2. Autores e afiliações.
3. **Abstract**.
4. **Keywords**: no máximo 6, 12 pt, itálico.
5. **References**.
6. **Biography**: até 150 palavras.

**Referências**, no estilo do modelo: iniciais e sobrenome dos autores, veículo, volume, páginas e (ano). Exemplo: `M. N. R. Ashfold, P. W. May, C. A. Rego, N. M. Everitt, Chem. Soc. Rev., 23, 21 – 30, (1994).` Usar os metadados de `references/references.bib`, nunca de memória.

## Como escrever para este evento

- **Público e enquadramento.** O público é de engenharia aeroespacial. Abrir pela decisão operacional (um stand a mais ou um balcão a mais; admissão antecipada ou FCFS), não pela revisão de literatura.
- **Estrutura do resumo:**
  1. Lacuna, em uma ou duas frases com fonte.
  2. Pergunta.
  3. Método, em uma ou duas frases (simulação de eventos discretos pareada, réplicas, configurações).
  4. Dois ou três resultados com números, unidades e IC 95%.
  5. Implicação operacional sob condição de demanda.
  6. Limite: cenário sintético, comparação de desenho, não previsão de um local.
- **Literatura.** É contexto curto. O protocolo da revisão (D3) não entra no resumo.
- **Números.** Só entram resultados arquivados, ligados à célula, ao denominador e à incerteza (`scripts/d4_experimento.py`). Enquanto não existirem, manter os marcadores `\pendente{...}` em vermelho. **Nunca inventar ou estimar resultados.**
- **Dados.** Todo dado vem de fonte: as bases do projeto (`data/parameter_registry.csv`, `references/references.bib`), depois a fonte oficial. Sem fonte, marcar como **suposto**, com o motivo, ou perguntar.
- **Termos.** O LoS da IATA tem critérios objetivos de tempo e espaço; não chamá-lo de proxy. A satisfação percebida exige uma medida declarada pelo passageiro.
- **Tom.** Afirmações proporcionais à evidência; não alegar ineditismo absoluto.

## Onde está cada coisa

| Assunto | Arquivo |
|---|---|
| Especificação do experimento (D4.1 v2.1) | `deliverables/D4_1_cenarios.md` |
| Plano e andamento da D4 | `deliverables/D4_plano.md` |
| Verificação do simulador (D4.2) | `data/d4/verificacao_d4_2.md` |
| Cadastro de parâmetros | `data/parameter_registry.csv` |
| Ambiente | Conda `ih214` (`environment.yml`). Testes: `cd scripts && python -m unittest` |
| Pacote do Overleaf | `deliverables/IH214_overleaf_estado_atual.zip` (manuscrito e resumo do evento) |

## Fluxo

- Explicar o plano antes de alterar código ou texto.
- Mudanças pequenas e verificáveis, com um commit por etapa.
- Após alterar uma seção ou o resumo, recompilar e atualizar o pacote do Overleaf.
