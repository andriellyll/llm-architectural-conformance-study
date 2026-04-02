import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "sample_dataset_with_comment_year.csv"

df = pd.read_csv(CSV_PATH)

df_filtered = df[df["comment_year"] >= 2020]

print("Total comments:", len(df_filtered))

df_filtered.to_csv(BASE_DIR / "sample_dataset_filtered_2020.csv", index=False)