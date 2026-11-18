# Espaço de colaboração com Claude

Este diretório é a interface assíncrona entre Claude e Codex. O Git é a fonte de verdade: toda entrega deve ser registrada em arquivos versionados e em um commit pequeno, descritivo e revisável.

## Contexto do projeto

O artigo estuda teoria de filas em vertiportos de passageiros, conectando operações eVTOL e nível de serviço do passageiro. Não redigir seções do artigo nesta etapa. O objetivo vigente é completar a Deliverable 2: especificar dados, estados, regras e cenários antes de implementar a simulação.

### Decisões já tomadas

- Unidade de análise: vertiporto genérico, não um sítio real.
- Exclusão absoluta: Vertiporto Sarah não pode ser usado, citado, modelado nem mencionado.
- Topologia-base: composição modular EASA PTS-VPT-DSN com um FATO--TLOF, uma taxiway/ground taxi-route e um stand; a Fase A começa em pouso no TLOF e termina na sua liberação.
- Implementação incremental: A TLOF; B táxi/stand; C turnaround/recarga; D processo obrigatório de passageiros completo.
- Coordenação: agendamento/reserva como caso-base; FCFS como benchmark.
- Aeronaves de referência: Eve eVTOL e Joby S4, configuração pilotada de 4 passageiros + 1 piloto.
- Não chamar envergadura publicada de “D regulatório”; D requer geometria certificada/AFM.
- Recarga: ainda não fixada. Deve ser informada por evidência de missão, energia e infraestrutura; não é obrigatória em todo pouso.
- LoS/satisfação: usar proxies explícitos de espera/confiabilidade; não alegar satisfação observada sem instrumento ou dado específico.

## Arquivos que devem ser lidos primeiro

1. `deliverables/D2_model_design.md`
2. `data/model_dictionary.csv`
3. `data/scenario_protocol.md`
4. `data/literature_matrix.csv`
5. `data/parameter_registry.csv`
6. `deliverables/GLOSSARY_VERTIDROME.md`
7. `data/oem_source_register.csv`
8. `claude/TASK_01_PASSENGER_TURNAROUND_EVIDENCE.md`

## Regras de trabalho

- Use fontes primárias, reguladores, editoras, DOI ou repositórios institucionais.
- Registre título, autores/instituição, ano, DOI/URL, páginas/seções e limitação antes de propor qualquer parâmetro.
- Classifique valores como `observed`, `literature`, `hypothesis` ou `scenario`.
- Não adicione fonte apenas por mencionar UAM; ela deve mudar uma decisão de modelo.
- Não transforme revisão em lista de autores. Sintetize por decisão de modelagem.
- Não sobrescreva ou reformate arquivos existentes sem necessidade. Escreva os resultados em `claude/outputs/` e só edite arquivos centrais se a evidência estiver completa e verificável.
- Não faça push forçado, rebase, reset ou alteração de commits alheios.

## Protocolo Git

1. Atualize sua cópia com `git pull --ff-only origin main`.
2. Trabalhe somente nos arquivos atribuídos em `claude/` e, se justificado, em arquivos de dados identificados na tarefa.
3. Execute verificações de CSV/BibTeX quando alterar esses arquivos.
4. Faça um commit com mensagem começando por `claude:`.
5. Faça push para `origin main` somente após o commit. Codex revisará o diff e integrará a evidência ao modelo.

## Entrega esperada

Use `claude/OUTPUT_TEMPLATE.md`. Uma entrega pode concluir que não há evidência suficiente para um parâmetro; isso é preferível a inventar uma faixa numérica.
