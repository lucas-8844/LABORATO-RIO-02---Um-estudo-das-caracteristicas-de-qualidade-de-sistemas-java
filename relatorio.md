# Características de Qualidade de Repositórios Java Populares no GitHub

## Autores

Lucas Carvalho e [Nome do colega]

---

# Sumário

1. Introdução
2. Hipóteses
3. Metodologia
    3.1 Seleção dos Repositórios
    3.2 Métricas Utilizadas
    3.3 Materiais e Ferramentas
    3.4 Processo Experimental
    3.5 Decisões de Implementação
4. Resultados
5. Discussão
6. Considerações Finais
7. Trabalhos Futuros

---

# 1. Introdução

No desenvolvimento de software open-source, a colaboração entre múltiplos desenvolvedores pode impactar diretamente atributos de qualidade interna, como modularidade, coesão e acoplamento.

Este trabalho tem como objetivo analisar a relação entre características do processo de desenvolvimento de repositórios Java populares no GitHub e suas métricas de qualidade interna, utilizando a ferramenta CK.

A análise considera os 1.000 repositórios Java mais populares, buscando identificar padrões entre métricas de processo e métricas estruturais do código.

---

# 2. Hipóteses

**RQ01 – Popularidade vs Qualidade**
Repositórios mais populares tendem a apresentar melhor qualidade interna.

**RQ02 – Maturidade vs Qualidade**
Repositórios mais antigos tendem a apresentar maior estabilidade estrutural.

**RQ03 – Atividade vs Qualidade**
Repositórios mais ativos tendem a apresentar melhor qualidade.

**RQ04 – Tamanho vs Qualidade**
Repositórios maiores tendem a apresentar maior complexidade estrutural.

---

# 3. Metodologia

## 3.1 Seleção dos Repositórios

Foram coletados os 1.000 repositórios Java mais populares do GitHub utilizando a API GraphQL, com base no número de estrelas.

---

## 3.2 Métricas Utilizadas

### Métricas de Processo

| Métrica      | Descrição            |
| ------------ | -------------------- |
| Popularidade | Número de estrelas   |
| Maturidade   | Idade do repositório |
| Atividade    | Número de releases   |

### Métricas de Qualidade

| Métrica | Descrição   |
| ------- | ----------- |
| CBO     | Acoplamento |
| DIT     | Herança     |
| LCOM    | Coesão      |

---

## 3.3 Materiais e Ferramentas

* Python
* Pandas
* Matplotlib
* API GitHub (GraphQL)
* Ferramenta CK

---

## 3.4 Processo Experimental

O experimento seguiu o fluxo:

```text
API → CSV → Clone → CK → Extração → Agregação → CSV final
```

Cada repositório foi processado individualmente, sendo removido após a análise para evitar sobrecarga no sistema.

---

## 3.5 Decisões de Implementação

* Processamento sequencial
* Remoção dos repositórios após uso
* Uso de métricas agregadas
* Tratamento de valores inconsistentes
* Desconsideração de outliers extremos na visualização

---

# 4. Resultados

## Maturidade vs LCOM

![Maturidade vs LCOM](../data/grafico_idade_lcom.png)

Observa-se que a maioria dos repositórios apresenta valores baixos de LCOM, indicando boa coesão. Entretanto, há presença de outliers extremos.

---

## Popularidade vs CBO

![Popularidade vs CBO](../data/grafico_popularidade_cbo.png)

Nota-se grande concentração de repositórios com poucos stars e valores moderados de CBO, sem correlação clara.

---

## Popularidade vs LCOM

![Popularidade vs LCOM](../data/grafico_popularidade_lcom.png)

A dispersão é alta, indicando ausência de relação direta entre popularidade e coesão.

---

## Atividade vs CBO

![Atividade vs CBO](../data/grafico_releases_cbo.png)

Repositórios com mais releases não apresentam redução significativa de acoplamento.

---

# 5. Discussão

Os resultados mostram que as relações entre métricas de processo e qualidade não são diretas.

A presença de outliers, especialmente em LCOM, indica que alguns repositórios possuem baixa coesão ou características específicas que impactam a análise.

Além disso, nem todos os repositórios classificados como Java possuem código significativo nessa linguagem, o que influencia os resultados.

A popularidade apresenta leve tendência de melhor organização, mas não é determinante.

A atividade contribui para manutenção, mas não garante qualidade estrutural.

---

# 6. Considerações Finais

O estudo permitiu analisar métricas de qualidade em larga escala.

Apesar das limitações, foi possível identificar padrões relevantes e compreender melhor a relação entre processo de desenvolvimento e qualidade.

---
