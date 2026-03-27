import os
import time
import requests
import pandas as pd

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN não foi encontrado.")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

query = """
query ($cursor: String) {
  search(query: "language:Java stars:>0 sort:stars-desc", type: REPOSITORY, first: 20, after: $cursor) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        name
        url
        stargazerCount
        createdAt
        releases {
          totalCount
        }
      }
    }
  }
}
"""

repos = []
cursor = None

while len(repos) < 1000:
    print(f"Buscando página... já coletados: {len(repos)}")

    variables = {"cursor": cursor}
    max_tentativas = 5
    sucesso = False

    for tentativa in range(1, max_tentativas + 1):
        try:
            response = requests.post(
                "https://api.github.com/graphql",
                json={"query": query, "variables": variables},
                headers=headers,
                timeout=30
            )

            print("Status HTTP:", response.status_code)

            if response.status_code in [502, 503, 504]:
                espera = tentativa * 5
                print(f"GitHub instável. Tentativa {tentativa}/{max_tentativas}. Aguardando {espera}s...")
                time.sleep(espera)
                continue

            if response.status_code != 200:
                print("Resposta da API:")
                print(response.text)
                raise Exception(f"Erro HTTP {response.status_code}")

            data = response.json()
            sucesso = True
            break

        except requests.exceptions.RequestException as e:
            espera = tentativa * 5
            print(f"Erro de conexão: {e}. Tentativa {tentativa}/{max_tentativas}. Aguardando {espera}s...")
            time.sleep(espera)

        except ValueError:
            espera = tentativa * 5
            print(f"Resposta não veio em JSON. Tentativa {tentativa}/{max_tentativas}. Aguardando {espera}s...")
            print("Conteúdo recebido:")
            print(response.text[:500])
            time.sleep(espera)

    if not sucesso:
        print("❌ Não foi possível obter resposta válida da API após várias tentativas.")
        break

    if "errors" in data:
        print("Erro retornado pela API:")
        print(data["errors"])
        break

    nodes = data["data"]["search"]["nodes"]

    if not nodes:
        print("Nenhum repositório retornado.")
        break

    for repo in nodes:
        repos.append({
            "nome": repo["name"],
            "url": repo["url"],
            "estrelas": repo["stargazerCount"],
            "created_at": repo["createdAt"],
            "releases": repo["releases"]["totalCount"]
        })

        if len(repos) >= 1000:
            break

    page_info = data["data"]["search"]["pageInfo"]

    if not page_info["hasNextPage"]:
        print("Não há mais páginas disponíveis.")
        break

    cursor = page_info["endCursor"]
    time.sleep(3)

if repos:
    output_path = "../data/repositorios.csv"
    pd.DataFrame(repos).to_csv(output_path, index=False)
    print(f"✅ CSV gerado com sucesso em: {output_path}")
    print(f"Total coletado: {len(repos)}")
else:
    print("❌ Nenhum repositório foi coletado. CSV não foi gerado.")
