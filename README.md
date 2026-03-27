# Lab02 - Sprint 1

## Descrição:
Projeto para análise de métricas de qualidade de repositórios Java utilizando a ferramenta CK.

## Estrutura:
- data/: arquivos CSV de entrada e saída
- scripts/: automações
- repos/: repositórios clonados
- ck/: ferramenta CK
- resultados_ck/: métricas geradas

## Execução:

1. Coletar repositórios:
python scripts/coleta_repos.py

2. Clonar:
python scripts/clone_repos.py

3. Rodar CK:
python scripts/processa_ck.py