import pandas as pd

# carregar arquivos
repos = pd.read_csv("../data/repositorios.csv")
metricas = pd.read_csv("../data/resultado_repo.csv")

# padronizar nome da coluna
repos = repos.rename(columns={"nome": "repo"})

# juntar os dados
df_final = pd.merge(repos, metricas, on="repo")

# salvar arquivo final
df_final.to_csv("../data/dados_finais.csv", index=False)

print("✅ dados_finais.csv criado com sucesso!")