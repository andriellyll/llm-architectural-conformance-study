import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# pasta onde estão os csvs
INPUT_FILE = BASE_DIR / "sample_classified_comments.csv"
OUTPUT_FILE = BASE_DIR / "design_restrictions_only.csv"

try:
    df = pd.read_csv(INPUT_FILE)

    # garante que a coluna existe
    if "is_design_restriction" not in df.columns:
        print(f"[AVISO] Coluna ausente em {INPUT_FILE}")

    # filtra linhas que contêm "Yes"
    filtered = df[
        df["is_design_restriction"]
        .astype(str)
        .str.contains("Yes", case=False, na=False)
    ]

except Exception as e:
    print(f"[ERRO] Falha ao processar {INPUT_FILE}: {e}")

# concatena tudo
if not filtered.empty:
    filtered.to_csv(OUTPUT_FILE, index=False)
    print(f"Arquivo gerado: {OUTPUT_FILE} ({len(filtered)} linhas)")
else:
    print("Nenhuma linha correspondente encontrada.")