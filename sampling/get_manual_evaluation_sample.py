import pandas as pd
import numpy as np

# -----------------------------
# CONFIGURAÇÃO
# -----------------------------

CSV_PATH = "test_generation_results.csv"

TARGET_COMMENTS = 270
MIN_COMMENTS_PER_PROJECT = 10
RANDOM_SEED = 42

PROJECT_COLUMN = "repository"


# -----------------------------
# CARREGAR DATASET
# -----------------------------

df = pd.read_csv(CSV_PATH)

print("Total de comentários no dataset:", len(df))
print("Total de projetos:", df[PROJECT_COLUMN].nunique())


# -----------------------------
# CONTAR COMENTÁRIOS POR PROJETO
# -----------------------------

project_counts = (
    df.groupby(PROJECT_COLUMN)
      .size()
      .reset_index(name="num_comments")
)

# filtrar projetos pequenos
project_counts = project_counts[
    project_counts["num_comments"] >= MIN_COMMENTS_PER_PROJECT
]

print("Projetos após filtro:", len(project_counts))


# -----------------------------
# EMBARALHAR PROJETOS
# -----------------------------

project_counts = project_counts.sample(
    frac=1,
    random_state=RANDOM_SEED
).reset_index(drop=True)


# -----------------------------
# SELECIONAR PROJETOS ATÉ ATINGIR TARGET
# -----------------------------

selected_projects = []
total_comments = 0

for _, row in project_counts.iterrows():

    project = row[PROJECT_COLUMN]
    n_comments = row["num_comments"]

    selected_projects.append(project)
    total_comments += n_comments

    if total_comments >= TARGET_COMMENTS:
        break


print("Projetos selecionados:", len(selected_projects))
print("Comentários estimados:", total_comments)


# -----------------------------
# EXTRAIR AMOSTRA FINAL
# -----------------------------

sample_df = df[df[PROJECT_COLUMN].isin(selected_projects)]

print("Comentários reais na amostra:", len(sample_df))


# -----------------------------
# SALVAR AMOSTRA
# -----------------------------

OUTPUT_PATH = "manual_evaluation_sample_2020.csv"

sample_df.to_csv(OUTPUT_PATH, index=False)

print("\nAmostra salva em:", OUTPUT_PATH)