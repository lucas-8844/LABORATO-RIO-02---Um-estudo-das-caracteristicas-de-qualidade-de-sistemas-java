import subprocess
import pandas as pd
import os
import shutil

repo_name = "caffeine"

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
repo_path = os.path.join(base_dir, "repos", repo_name)
saida_path = os.path.join(base_dir, "resultados_ck")
output_path = os.path.join(base_dir, "data", "resultado_repo.csv")
ck_jar_path = os.path.join(base_dir, "ck", "ck.jar")

os.makedirs(saida_path, exist_ok=True)

# limpa a pasta de saída
for item in os.listdir(saida_path):
    item_path = os.path.join(saida_path, item)
    if os.path.isfile(item_path):
        os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

print(f"🚀 Rodando CK no repositório: {repo_name}")
print(f"Repo path: {repo_path}")
print(f"Saída CK: {saida_path}")

# executa o CK DENTRO da pasta de saída
resultado_execucao = subprocess.run([
    "java", "-jar", ck_jar_path,
    repo_path, "true", "0", "false"
], cwd=saida_path, capture_output=True, text=True)

print("STDOUT CK:")
print(resultado_execucao.stdout)

print("STDERR CK:")
print(resultado_execucao.stderr)

print("Arquivos gerados em resultados_ck:")
print(os.listdir(saida_path))

class_csv_path = os.path.join(saida_path, "class.csv")

if not os.path.exists(class_csv_path):
    raise FileNotFoundError("❌ class.csv não foi gerado em resultados_ck.")

print("📊 Lendo class.csv...")

df = pd.read_csv(class_csv_path)

print(f"Total de classes analisadas: {len(df)}")

for col in ["cbo", "dit", "lcom"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

resultado = {
    "repo": repo_name,

    "media_cbo": round(df["cbo"].mean(), 2),
    "mediana_cbo": round(df["cbo"].median(), 2),
    "desvio_padrao_cbo": round(df["cbo"].std(), 2) if not pd.isna(df["cbo"].std()) else 0.0,

    "media_dit": round(df["dit"].mean(), 2),
    "mediana_dit": round(df["dit"].median(), 2),
    "desvio_padrao_dit": round(df["dit"].std(), 2) if not pd.isna(df["dit"].std()) else 0.0,

    "media_lcom": round(df["lcom"].mean(), 2),
    "mediana_lcom": round(df["lcom"].median(), 2),
    "desvio_padrao_lcom": round(df["lcom"].std(), 2) if not pd.isna(df["lcom"].std()) else 0.0
}

pd.DataFrame([resultado]).to_csv(output_path, index=False)

print(f"✅ Resultado salvo em: {output_path}")