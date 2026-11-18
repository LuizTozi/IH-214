# Tarefa 01 para Claude — evidência de passageiro, turnaround e recarga

## Objetivo

Encontrar evidência verificável que permita especificar a Fase D do modelo: processo obrigatório de passageiros, sincronização com aeronave, regras de turnaround e cenários de recarga. A meta não é ampliar a bibliografia; é reduzir incertezas no dicionário do modelo.

## Perguntas a responder

1. Quais etapas de processamento de passageiro em aeroportos, heliportos ou vertiportos são transferíveis à sequência `chegada → check-in → inspeção/acesso → espera → embarque`?
2. Quais regras operacionais ou de ground handling estabelecem pré-requisitos e ordem entre chegada, desembarque, embarque, carregamento/recarga e partida?
3. Que evidência permite representar passageiro atrasado, grupo incompleto, partida com assentos vazios, no-show ou janela de embarque sem inventar comportamento?
4. Para Eve e Joby, quais dados oficiais permitem inferir **apenas** a necessidade de uma classe de cenário de recarga? Procure capacidade/arquitetura de bateria, interface de carga, missão, limites de operação ou declaração explícita de ausência de dado. Não estime curva de carga.
5. Que fonte distingue com segurança vertistop de vertiporto no que se refere a recarga local?

## Fontes prioritárias

- EASA Easy Access Rules: Air Operations UAM.OP.MVCA.205 e Ground Handling.
- FAA AC 150/5390-2D e EB 105A, quando falarem de acesso/segurança/stands.
- FAA/NREL *Vertiport Electrical Infrastructure Study* (`solanki2023`).
- AIAA/Elsevier/Springer já presentes em `data/literature_matrix.csv`, sobretudo Feldhoff (2022), Feldhoff e Soares Roque (2021), Preis e Hornung (2022), Schweiger et al. (2022) e Onat et al. (2024).
- Materiais oficiais Eve e Joby apenas para capacidade e arquitetura; não usar marketing como calibração de fila.

## Exclusões

- Não usar Vertiporto Sarah.
- Não usar notícias, blogs ou páginas comerciais como única base de um parâmetro.
- Não propor satisfação psicológica a partir de espera sem uma fonte comportamental adequada.
- Não alegar que uma regra de aeroporto se aplica automaticamente a eVTOL; descreva-a como mecanismo transferível ou cenário, com sua limitação.

## Saídas exigidas

1. `claude/outputs/TASK_01_EVIDENCE.md`, preenchido com a síntese por decisão.
2. `claude/outputs/TASK_01_SOURCE_TABLE.csv`, uma linha por fonte útil, com metadados completos.
3. `claude/outputs/TASK_01_PARAMETER_CANDIDATES.csv`, apenas parâmetros/regras que tenham fonte, unidade/regra, tipo de evidência, aplicabilidade e limitação.
4. Se houver evidência suficiente, sugestão pontual de alteração para `data/model_dictionary.csv`; não editar diretamente o arquivo central sem explicar a alteração no relatório.

## Critério de conclusão

Uma fonte só é “útil” se levar a pelo menos uma destas decisões: etapa obrigatória, condição de prontidão, regra de sincronização, distribuição/faixa de serviço, política de recarga, limiar de segurança ou métrica de avaliação. Declare explicitamente lacunas restantes.
