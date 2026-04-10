import os
import shutil
import subprocess
import tempfile
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

REPOS_CSV = os.path.join(BASE_DIR, "data", "repositorios.csv")
RESULTADO_FINAL = os.path.join(BASE_DIR, "data", "resultado_repo.csv")
CK_JAR = os.path.join(BASE_DIR, "ck", "ck.jar")

# caminhos curtos no Windows
WORK_BASE = r"C:\lab2tmp"
CK_OUT = os.path.join(WORK_BASE, "ck_out")

os.makedirs(WORK_BASE, exist_ok=True)
os.makedirs(CK_OUT, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)


def limpar_pasta(caminho):
    if os.path.exists(caminho):
        shutil.rmtree(caminho, ignore_errors=True)
    os.makedirs(caminho, exist_ok=True)


def rodar_comando(comando, cwd=None):
    return subprocess.run(
        comando,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )


def processar_repositorio(repo_nome, repo_url, indice, total):
    if not repo_url.endswith(".git"):
        repo_url += ".git"

    print(f"\n🚀 [{indice}/{total}] Processando: {repo_nome}")
    print(f"🔗 URL: {repo_url}")

    # cria uma pasta temporária nova para este repositório
    repo_temp_dir = tempfile.mkdtemp(prefix="repo_", dir=WORK_BASE)

    try:
        clone_result = rodar_comando(
            ["git", "clone", "--depth", "1", repo_url, repo_temp_dir]
        )

        if clone_result.returncode != 0:
            print(f"❌ Erro ao clonar {repo_nome}")
            print(clone_result.stderr)
            return None

        print("📥 Clone realizado com sucesso")

        # limpa saída anterior do CK
        limpar_pasta(CK_OUT)

        # roda CK dentro da pasta de saída
        ck_result = rodar_comando(
            ["java", "-jar", CK_JAR, repo_temp_dir, "true", "0", "false"],
            cwd=CK_OUT
        )

        print("STDOUT CK:")
        print(ck_result.stdout.strip())

        if ck_result.stderr.strip():
            print("STDERR CK:")
            print(ck_result.stderr.strip())

        class_csv = os.path.join(CK_OUT, "class.csv")

        if not os.path.exists(class_csv):
            print(f"❌ class.csv não foi gerado para {repo_nome}")
            return None

        try:
            df_ck = pd.read_csv(class_csv)
        except Exception as e:
            print(f"❌ Erro ao ler class.csv de {repo_nome}: {e}")
            return None

        print(f"📊 Total de classes analisadas: {len(df_ck)}")

        for col in ["cbo", "dit", "lcom"]:
            if col in df_ck.columns:
                df_ck[col] = pd.to_numeric(df_ck[col], errors="coerce").fillna(0)
            else:
                df_ck[col] = 0

        resultado = {
            "repo": repo_nome,
            "media_cbo": round(df_ck["cbo"].mean(), 2),
            "mediana_cbo": round(df_ck["cbo"].median(), 2),
            "desvio_padrao_cbo": round(df_ck["cbo"].std(), 2) if not pd.isna(df_ck["cbo"].std()) else 0.0,
            "media_dit": round(df_ck["dit"].mean(), 2),
            "mediana_dit": round(df_ck["dit"].median(), 2),
            "desvio_padrao_dit": round(df_ck["dit"].std(), 2) if not pd.isna(df_ck["dit"].std()) else 0.0,
            "media_lcom": round(df_ck["lcom"].mean(), 2),
            "mediana_lcom": round(df_ck["lcom"].median(), 2),
            "desvio_padrao_lcom": round(df_ck["lcom"].std(), 2) if not pd.isna(df_ck["lcom"].std()) else 0.0
        }

        return resultado

    finally:
        shutil.rmtree(repo_temp_dir, ignore_errors=True)
        print(f"🗑️ Repositório temporário removido: {repo_nome}")


def main():
    if not os.path.exists(REPOS_CSV):
        raise FileNotFoundError(f"Arquivo não encontrado: {REPOS_CSV}")

    if not os.path.exists(CK_JAR):
        raise FileNotFoundError(f"Arquivo CK não encontrado: {CK_JAR}")

    reset = input("Deseja recomeçar do zero? (s/n): ").strip().lower()

    if reset == "s":
        if os.path.exists(RESULTADO_FINAL):
            os.remove(RESULTADO_FINAL)
            print("🗑️ resultado_repo.csv apagado.")
        if os.path.exists(WORK_BASE):
            shutil.rmtree(WORK_BASE, ignore_errors=True)
            print("🗑️ Pasta temporária C:\\lab2tmp apagada.")
        os.makedirs(WORK_BASE, exist_ok=True)
        os.makedirs(CK_OUT, exist_ok=True)

    subprocess.run(
        ["git", "config", "--global", "core.longpaths", "true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("📄 Lendo repositorios.csv...")
    df_repos = pd.read_csv(REPOS_CSV)

    if "nome" not in df_repos.columns or "url" not in df_repos.columns:
        raise ValueError("O repositorios.csv precisa ter pelo menos as colunas: nome, url")

    total = len(df_repos)

    if os.path.exists(RESULTADO_FINAL):
        try:
            df_resultados = pd.read_csv(RESULTADO_FINAL)
            if "repo" not in df_resultados.columns:
                df_resultados = pd.DataFrame(columns=[
                    "repo",
                    "media_cbo", "mediana_cbo", "desvio_padrao_cbo",
                    "media_dit", "mediana_dit", "desvio_padrao_dit",
                    "media_lcom", "mediana_lcom", "desvio_padrao_lcom"
                ])
        except Exception:
            df_resultados = pd.DataFrame(columns=[
                "repo",
                "media_cbo", "mediana_cbo", "desvio_padrao_cbo",
                "media_dit", "mediana_dit", "desvio_padrao_dit",
                "media_lcom", "mediana_lcom", "desvio_padrao_lcom"
            ])
    else:
        df_resultados = pd.DataFrame(columns=[
            "repo",
            "media_cbo", "mediana_cbo", "desvio_padrao_cbo",
            "media_dit", "mediana_dit", "desvio_padrao_dit",
            "media_lcom", "mediana_lcom", "desvio_padrao_lcom"
        ])

    repos_ja_processados = set(df_resultados["repo"].astype(str).tolist())
    print(f"✅ Repositórios já processados: {len(repos_ja_processados)}")

    for idx, row in enumerate(df_repos.itertuples(index=False), start=1):
        nome = str(row.nome).strip()
        url = str(row.url).strip()

        if nome in repos_ja_processados:
            print(f"⏭️ [{idx}/{total}] Pulando {nome} (já processado)")
            continue

        try:
            resultado = processar_repositorio(nome, url, idx, total)

            if resultado is not None:
                df_resultados = pd.concat(
                    [df_resultados, pd.DataFrame([resultado])],
                    ignore_index=True
                )

                df_resultados = df_resultados.drop_duplicates(subset=["repo"], keep="last")
                df_resultados.to_csv(RESULTADO_FINAL, index=False)

                repos_ja_processados.add(nome)

                print(f"💾 Resultado salvo em: {RESULTADO_FINAL}")
                print(f"✅ Total acumulado: {len(df_resultados)}")

        except Exception as e:
            print(f"❌ Erro inesperado ao processar {nome}: {e}")
            continue

    print(f"\n🎉 Processo concluído.")
    print(f"✅ Resultado final salvo em: {RESULTADO_FINAL}")
    print(f"✅ Total processado com sucesso: {len(df_resultados)} de {total}")


if __name__ == "__main__":
    main()