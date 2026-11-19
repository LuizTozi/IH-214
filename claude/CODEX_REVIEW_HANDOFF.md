# Passagem de contexto — artigo IH-214

Este arquivo permite continuar o trabalho em uma nova conversa Codex aberta na pasta do repositório `IH-214`. Ele registra as decisões e o estado de trabalho relevantes da conversa anterior; não é uma transcrição literal do histórico do chat.

## Objetivo do artigo

Estudar teoria de filas e capacidade em um vertiporto de passageiros, conectando operações de eVTOL (lado ar) ao processamento e à espera dos passageiros (lado terra). O modelo será desenvolvido incrementalmente e comparará coordenação por agendamento/reserva com FCFS. A satisfação do passageiro não será inferida apenas a partir do tempo de espera; só poderá ser discutida como satisfação medida se houver instrumento/dados apropriados.

## Decisões de pesquisa registradas

- Usar uma topologia modular de documento técnico/regulatório, com um FATO–TLOF, taxiway/ground taxi-route e stand.
- Desenvolver o modelo em fases, começando pelo pouso e liberação/saída do TLOF e acrescentando recursos/processos conforme os dados e a verificação permitirem.
- Na versão integrada, todas as etapas definidas do processo de passageiros são obrigatórias.
- Caso-base de coordenação: agendamento/reserva; FCFS será benchmark.
- Aeronaves de referência: Eve eVTOL e Joby S4, configuradas para quatro passageiros mais piloto. Não tratar envergadura publicada como D regulatório.
- A fronteira operacional deixa voo, rota e energia de missão fora do escopo inicial.
- O Vertiporto Sarah é apenas estudo anterior: não citar, modelar nem incluir no artigo.
- Usar LaTeX/Overleaf. A organização por deliverables toma como referência o formato do documento de IT-212, sem copiar seu conteúdo.
- Redigir por decisões de modelagem e rastreabilidade de evidência, evitando uma lista de autores sem função no argumento. Toda afirmação, valor, regra e cenário deve ter fonte verificável ou ficar explicitamente como lacuna/undefined. Distinguir dado observado, valor de literatura, hipótese e cenário.
- Para LoS, seguir os critérios objetivos IATA ADRM de tempo de espera e espaço de fila conforme a fonte citada no projeto. LoS e satisfação são conceitos separados; não chamar LoS de proxy.

## Estado do repositório na revisão

Na conversa anterior, o repositório estava em `main`, sincronizado com `origin/main`, commit `ab88d62` (`claude: add handoff to Codex for review of Task 01 and author decisions`), sem alterações locais. Claude acrescentou a Tarefa 01 sobre passageiros, turnaround e recarga; adicionou referências LIT-023 a LIT-027; atualizou D2, dicionário, registro de parâmetros, matriz bibliográfica, log de busca e figura acoplada. D1 não foi alterada. O texto do artigo ainda não foi redigido. O handoff do Claude é `claude/HANDOFF_TO_CODEX.md`.

A revisão do Codex foi de consistência documental e visual; não reabriu independentemente todos os documentos-fonte e não executou build LaTeX. Nenhum arquivo foi alterado pela revisão.

## Problemas encontrados que devem ser lidos primeiro

1. **LoS: variável incompatível com a métrica.** `VAR-012` é a espera total entre chegada ao terminal e início do embarque. `VAR-014` guarda limites de espera por estação. Porém `VAR-015` diz comparar `VAR-012` com `VAR-014`. Criar/definir espera em fila por estação e calcular conformidade de LoS usando as medidas correspondentes. Arquivo: `data/model_dictionary.csv`.
2. **Recarga: regra e pendência se contradizem.** D2 diz que o tempo de recarga é declarado na reserva e aplicado a todo turnaround (0/30/60 min), mas mantém como pendentes localização e regra de necessidade. `VAR-022` também inclui a conclusão do tempo de recarga declarado como condição de prontidão. Os valores vêm de estudo com veículo e hipótese de embarque diferentes. Resolver se 0/30/60 são apenas cenários exploratórios ou decisão operacional adotada; não apresentar necessidade de recarga como fato sem evidência de missão. Arquivos: `deliverables/D2_model_design.md`, `data/model_dictionary.csv`, `data/parameter_registry.csv`.
3. **Decisões fechadas continuam abertas em outros registros.** D2 escolhe LoS fast-track (180/120/180 s), mas ainda lista a escolha do conjunto LoS como pendente. A D2 exclui troca de bateria, mas `TASK_01_PARAMETER_CANDIDATES.csv` ainda descreve essa decisão como pendente. Harmonizar os estados e preservar histórico sem reabrir escolhas já feitas.
4. **Massa versus estação de pesagem.** D2 exclui estação de pesagem, mas a síntese da Tarefa 01 mantém pesagem na sequência recomendada. Distinguir requisito de conhecer massa/CG antes do voo da decisão de simular uma estação de pesagem no terminal. Confirmar que a sequência obrigatória final está coerente com a decisão do autor.
5. **Parâmetros legados sem status claro.** `PAR-010` mantém 311 kW como potência de recarga não excluída, embora D2 diga que potência não será usada. `PAR-012` mantém turnaround/gate agregado de 10 min. Marcar como excluídos/legado para rastreabilidade ou especificar em que cenário/modelo ainda serão usados.
6. **Instruções internas desatualizadas.** `claude/README.md` ainda recomenda “proxies” para LoS, contra a decisão registrada no handoff e na D2. Atualizar essa orientação.
7. **Afirmação incorreta na entrega.** `claude/outputs/TASK_01_EVIDENCE.md` diz que nenhum arquivo central foi editado; o diff confirma alterações em arquivos centrais. Corrigir o registro para refletir o histórico.
8. **Figura conceitual:** legível, mas as setas de acoplamento, controle de slots e fluxo não têm legenda explícita. Considerar uma pequena legenda e deixar claro que se trata do modelo completo, não apenas da Fase A.

## Pendências de pesquisa que continuam legítimas

- Tempo de serviço de check-in e inspeção de segurança completa: ainda sem fonte/valor validado.
- Ordem entre checagem de bagagem e inspeção: não estabelecida pelas fontes lidas.
- Limite LoS para checagem de bagagem: não encontrado na evidência registrada.
- Regra para grupos incompletos, passageiros atrasados/no-show e assentos vazios: sem política/valor sustentado.
- Horizonte, aquecimento, replicações, sementes, faixas de demanda e distribuições sem evidência: ainda precisam ser especificados antes do protocolo experimental integrado.
- Não houve build LaTeX; antes de depender da bibliografia na compilação, validar BibTeX e compilar quando a estrutura do projeto estiver pronta.

## Como iniciar a próxima conversa

Abra uma nova conversa Codex com o diretório de trabalho `/home/rique-tozi/Documentos/ITA/IH-214` e cole:

> Continue o projeto do artigo IH-214 usando `claude/CODEX_REVIEW_HANDOFF.md` como passagem de contexto. Leia também `claude/HANDOFF_TO_CODEX.md`, `deliverables/D2_model_design.md`, `data/model_dictionary.csv`, `data/parameter_registry.csv`, `claude/outputs/TASK_01_EVIDENCE.md` e `claude/outputs/TASK_01_PARAMETER_CANDIDATES.csv`. Comece apresentando os problemas da revisão em ordem de prioridade para eu ler; depois proponha uma sequência de correção sem redigir o artigo. Não reabra decisões explícitas do autor sem apontar a evidência que exige isso. Preserve a regra de não citar nem modelar o Vertiporto Sarah e mantenha rastreabilidade de cada entrada do modelo.

Para levar também o histórico literal do chat, use a função de exportação/compartilhamento da interface e anexe o arquivo exportado à nova conversa. Este handoff resume o contexto relevante, mas não reproduz mensagens palavra por palavra.
