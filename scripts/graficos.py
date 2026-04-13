import pandas as pd
import matplotlib.pyplot as plt

# carregar dados
df = pd.read_csv("../data/dados_finais.csv")

# converter data para idade
df["created_at"] = pd.to_datetime(df["created_at"])
df["idade"] = 2026 - df["created_at"].dt.year

# =========================
# GRÁFICO 1 - Popularidade vs CBO
# =========================
plt.figure()
plt.scatter(df["estrelas"], df["media_cbo"])
plt.xlabel("Estrelas")
plt.ylabel("CBO")
plt.title("Popularidade vs CBO")
plt.savefig("../data/grafico_popularidade_cbo.png")

# =========================
# GRÁFICO 2 - Maturidade vs LCOM
# =========================
plt.figure()
plt.scatter(df["idade"], df["media_lcom"])
plt.xlabel("Idade (anos)")
plt.ylabel("LCOM")
plt.title("Maturidade vs LCOM")
plt.savefig("../data/grafico_idade_lcom.png")

# =========================
# GRÁFICO 3 - Releases vs CBO
# =========================
plt.figure()
plt.scatter(df["releases"], df["media_cbo"])
plt.xlabel("Releases")
plt.ylabel("CBO")
plt.title("Atividade vs CBO")
plt.savefig("../data/grafico_releases_cbo.png")

# =========================
# GRÁFICO 4 - Popularidade vs LCOM
# =========================
plt.figure()
plt.scatter(df["estrelas"], df["media_lcom"])
plt.xlabel("Estrelas")
plt.ylabel("LCOM")
plt.title("Popularidade vs LCOM")
plt.savefig("../data/grafico_popularidade_lcom.png")

print("✅ Gráficos gerados com sucesso!")