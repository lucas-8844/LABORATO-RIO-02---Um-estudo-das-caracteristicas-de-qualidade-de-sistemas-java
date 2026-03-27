import pandas as pd
import subprocess
import os

df = pd.read_csv("../data/repositorios.csv")

os.makedirs("../repos", exist_ok=True)

for _, row in df.iterrows():
    nome = row["nome"]
    url = row["url"]

    path = f"../repos/{nome}"

    if not os.path.exists(path):
        subprocess.run(["git", "clone", url, path])