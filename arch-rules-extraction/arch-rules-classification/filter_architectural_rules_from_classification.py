import pandas as pd
import os
from glob import glob

# pasta onde estão os csvs
INPUT_FOLDER = "results"
OUTPUT_FILE = "design_restrictions_only.csv"

all_dfs = []

# pega todos os csvs da pasta
csv_files = glob(os.path.join(INPUT_FOLDER, "*.csv"))

for file in csv_files:
    try:
        df = pd.read_csv(file)

        # garante que a coluna existe
        if "is_design_restriction" not in df.columns:
            print(f"[AVISO] Coluna ausente em {file}")
            continue

        # filtra linhas que contêm "Yes"
        filtered = df[
            df["is_design_restriction"]
            .astype(str)
            .str.contains("Yes", case=False, na=False)
        ]

        # opcional: guardar de qual arquivo veio
        filtered["source_file"] = os.path.basename(file)

        all_dfs.append(filtered)

    except Exception as e:
        print(f"[ERRO] Falha ao processar {file}: {e}")

# concatena tudo
if all_dfs:
    result = pd.concat(all_dfs, ignore_index=True)
    result.to_csv(OUTPUT_FILE, index=False)
    print(f"Arquivo gerado: {OUTPUT_FILE} ({len(result)} linhas)")
else:
    print("Nenhuma linha correspondente encontrada.")