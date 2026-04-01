import pandas as pd

CSV_PATH = "sample_dataset_with_comment_year.csv"

df = pd.read_csv(CSV_PATH)

df_filtered = df[df["comment_year"] >= 2020]

print("Comentários:", len(df_filtered))
print("Projetos únicos:", df_filtered["repository"].nunique())

comments_per_repo = df_filtered.groupby("repository").size()

print(comments_per_repo.describe())

top_projects = df_filtered["repository"].value_counts().head(10)

print(top_projects)

print("Total comments:", len(df_filtered))
print("Total repositories:", df_filtered["repository"].nunique())
print("Median comments per repo:", df_filtered.groupby("repository").size().median())
print("Max comments in a repo:", df_filtered.groupby("repository").size().max())

df_filtered.to_csv("sample_dataset_filtered_2020.csv", index=False)