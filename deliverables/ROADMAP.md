# Roteiro operacional do artigo

## Princípio de continuidade

Cada fase tem uma saída versionada, critérios técnicos de encerramento e uma fase sucessora
definida. Ao concluir e verificar uma fase, inicia-se a seguinte sem aguardar uma nova rodada de
planejamento. Perguntas, título e periódico permanecem provisórios até que a evidência acumulada
justifique sua estabilização.

## Escopo fixo

- Tema: teoria de filas aplicada às operações de vertiportos e à experiência de passageiros em
  serviços eVTOL.
- Unidade de análise: processos, recursos e fluxos de um vertiporto; não um sítio específico.
- Exclusão: o Vertiporto Sarah não é estudo de caso, fonte de dados, resultado ou citação.
- Estilo bibliográfico provisório: autor--data.

## Fluxo de trabalho

### Fase 0 — Fundação do projeto

**Situação:** concluída.

**Saídas:** repositório privado, estrutura LaTeX, banco BibTeX, diretórios de dados e scripts,
estilo autor--data provisório.

**Critério de encerramento:** `main.tex` compila e o repositório remoto contém o commit inicial.

**Próxima fase:** Fase 1.

### Fase 1 — Mapa de evidências e Deliverable 1

**Situação:** concluída em 18 de novembro de 2026.

**Objetivo:** transformar a pesquisa exploratória em uma base rastreável de literatura, normas e
parâmetros, sem redigir o manuscrito.

**Ações:**

1. Buscar sistematicamente estudos em cinco eixos: capacidade airside, turnaround e energia,
   processamento de passageiros, filas/redes/simulação e satisfação/aceitação.
2. Registrar cada fonte em `data/literature_matrix.csv` com escopo, método, dados, parâmetros,
   resultados, limitações e DOI/URL.
3. Extrair referências verificadas para `references/references.bib`.
4. Criar `data/parameter_registry.csv`, distinguindo valor observado, valor de literatura,
   hipótese e cenário.
5. Formular versões numeradas do tema e da pergunta de pesquisa em
   `deliverables/D1_framing.md`; nenhuma versão é definitiva nesta fase.

**Saídas:** matriz de literatura, registro de parâmetros, BibTeX validado e Deliverable 1 com
tema, pergunta provisória e referências essenciais.

**Critério de encerramento:** pelo menos 20 fontes acadêmicas pertinentes, cinco ou mais fontes
centrais verificadas, cobertura dos cinco eixos e ao menos uma lacuna sustentada por três fontes.

**Próxima fase:** Fase 2.

### Fase 2 — Modelo conceitual, dados e Deliverable 2

**Situação:** concluída em 19 de novembro de 2026 para o caso-base sintético. Diagrama, dicionário, parâmetros e protocolo disponíveis. As fases técnicas A a D passaram nos 18 testes de verificação.

**Objetivo:** definir exatamente o que será representado, medido e inferido antes de programar.

**Ações:**

1. Desenhar a rede acoplada: passageiros (chegada, processamento, espera, embarque) e eVTOLs
   (pad, stand/gate, turnaround, recarga, partida).
2. Definir entidades, recursos, capacidades finitas, regras de prioridade, eventos e estados.
3. Mapear cada variável a uma fonte ou classificá-la explicitamente como cenário.
4. Definir métricas operacionais: throughput, utilização, bloqueio, espera média, P95 e nível de
   serviço.
5. Definir métricas da experiência: probabilidade de atendimento dentro do limite, tempo total no
   vertiporto, confiabilidade e dispersão de espera.
6. Especificar o método: modelo analítico onde aplicável e simulação de eventos discretos quando
   houver bloqueio, sincronização ou recursos acoplados.

**Saídas:** diagrama conceitual, dicionário de dados, protocolo de cenários e Deliverable 2.

**Critério de encerramento:** toda variável tem unidade, definição, tipo de evidência e papel no
modelo; toda métrica responde a uma parte da pergunta provisória.

**Próxima fase:** Fase 3.

### Fase 3 — Base teórica e Deliverable 3

**Objetivo:** consolidar a sustentação conceitual sem antecipar resultados.

Por orientação do autor, a revisão da D3 seguirá o **Methodi Ordinatio**.
O acervo metodológico está em `/home/rique-tozi/Documentos/ITA/TESE/Methodi_Ordinatio`.
A matriz bibliográfica da D1 será o conjunto inicial para testar descritores
e verificar a recuperação de trabalhos conhecidos nos quatro blocos teóricos.

Registrar a pergunta, as buscas exploratórias, as expressões finais por base,
as datas, os resultados exportados, a deduplicação e os motivos de exclusão.
Para os artigos elegíveis, identificar ano, citações com fonte e data e
indicador do periódico com edição e procedência. Antes de ordenar o portfólio,
registrar a versão da equação e os pesos adotados. A versão 2.0 é a referência
inicial de trabalho. A variante NI será avaliada se a comparação entre áreas
exigir normalização. FInder e RankIn estão disponíveis no acervo local.

Após a ordenação, localizar os textos integrais e extrair, por artigo, o
conceito sustentado, o trecho ou página e sua ligação com a rede da D2.
Regulamentos e documentos operacionais terão seleção por autoridade,
aplicabilidade e dispositivo pertinente, com rastreabilidade própria.

**Ações:**

1. Organizar a teoria em quatro blocos: teoria de filas, operações de vertiportos, processamento
   de passageiros e qualidade/satisfação do serviço.
2. Relacionar os blocos ao modelo conceitual, deixando explícitas as interfaces entre as duas
   redes.
3. Escrever a versão inicial, limitada ao tamanho exigido pela disciplina, com citações indiretas
   e referências rastreáveis.
4. Revisar coerência: nenhum conceito usado no método pode aparecer sem definição ou fonte.

**Saídas:** `sections/theoretical_basis.tex` e Deliverable 3 revisado.

**Critério de encerramento:** texto dentro do limite solicitado, todas as afirmações verificáveis
citadas e ligação explícita entre teoria, variáveis e método.

**Próxima fase:** Fase 4.

### Fase 4 — Implementação, verificação e experimentos

**Objetivo:** construir um modelo reproduzível antes de interpretar qualquer resultado.

**Ações:**

1. Implementar o protótipo em `scripts/` com configuração separada dos dados.
2. Verificar casos com solução conhecida: Little, Erlang e filas de um ou múltiplos servidores.
3. Implementar a sincronização passageiro--aeronave e o bloqueio por capacidade finita.
4. Executar replicações, aquecimento, sementes reprodutíveis e intervalos de confiança.
5. Rodar cenários de capacidade, demanda, turnaround e recarga; registrar todas as premissas.

**Saídas:** código, testes, tabelas brutas, log de cenários e figuras preliminares.

**Critério de encerramento:** testes analíticos passam, as simulações são reproduzíveis e nenhum
resultado é apresentado sem cenário e suposição associados.

**Próxima fase:** Fase 5.

### Fase 5 — Análise de resultados e Deliverable 4

**Objetivo:** responder empiricamente à pergunta provisória e, se necessário, revisá-la.

**Ações:**

1. Selecionar tabelas e figuras que expliquem gargalos, efeitos de capacidade e trade-offs entre
   eficiência e nível de serviço.
2. Comparar resultados com a literatura, distinguindo confirmação, divergência e hipótese nova.
3. Fazer análise de sensibilidade dos parâmetros com maior incerteza.
4. Revisar a pergunta de pesquisa apenas se os resultados demonstrarem que o enquadramento inicial
   é inadequado.
5. Escrever a análise e discussão no Deliverable 4.

**Saídas:** `sections/results.tex`, figuras finais, tabelas finais e Deliverable 4.

**Critério de encerramento:** cada conclusão tem resultado correspondente, cada resultado possui
incerteza ou condição de cenário e toda inferência respeita as limitações dos dados.

**Próxima fase:** Fase 6.

### Fase 6 — Integração do Deliverable 5

**Objetivo:** montar o manuscrito completo a partir de componentes já verificados.

**Ações:**

1. Escrever introdução, método, conclusões, resumo e highlights por último.
2. Integrar as seções em `main.tex`; incluir tabelas, figuras e referências apenas após serem
   apresentadas e discutidas no texto.
3. Revisar contribuição teórica, contribuição prática e limitações.
4. Adaptar título, resumo, palavras-chave e formatação ao periódico-alvo quando ele for definido.

**Saídas:** PDF do artigo completo e Deliverable 5.

**Critério de encerramento:** narrativa coerente de problema para contribuição; resumo contém
contexto, lacuna, método, resultados e conclusão; todas as citações resolvem no PDF.

**Próxima fase:** Fase 7.

### Fase 7 — Auditoria final e entrega

**Objetivo:** garantir rigor científico, reprodutibilidade e conformidade editorial.

**Ações:**

1. Validar DOI, metadados, chaves BibTeX e referências não citadas.
2. Revisar texto quanto a evidência, escopo, limitações e consistência de termos.
3. Reexecutar scripts a partir dos dados versionados e conferir figuras/tabelas.
4. Compilar o LaTeX limpo e inspecionar PDF, referências, legendas e numeração.
5. Aplicar o template e as regras do periódico-alvo, caso definidos.

**Saídas:** manuscrito pronto para avaliação, pacote reproduzível de dados/código permitido e
checklist de entrega.

**Critério de encerramento:** compilação sem referências pendentes, resultados reproduzíveis,
limitações declaradas e conformidade com a entrega da disciplina ou com o periódico-alvo.

## Regra de transição automática

Ao fechar uma fase, o agente deve: (1) registrar as saídas no repositório; (2) executar as
verificações indicadas; (3) fazer commit e push; e (4) iniciar a fase seguinte. Uma interrupção só
ocorre se faltar uma decisão que mude materialmente o escopo, se uma fonte essencial não puder ser
verificada ou se a validação técnica falhar repetidamente.
