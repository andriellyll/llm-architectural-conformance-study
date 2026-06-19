import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# =========================
# Configurações
# =========================
INPUT_CSV = BASE_DIR / "../arch_rules_extraction/arch_rules_classification/design_restrictions_only.csv"
OUTPUT_CSV = BASE_DIR / "classification_validation_sample.csv"

SAMPLE_SIZE = 270
RANDOM_SEED = 42  

# =========================
# Leitura do dataset
# =========================
df = pd.read_csv(INPUT_CSV)

print(f"Total de comentários classificados como regra de design pelo LLM: {len(df)}")

if len(df) < SAMPLE_SIZE:
    raise ValueError("O dataset é menor que o tamanho da amostra.")

# =========================
# Amostragem aleatória simples
# População = todos os comentários classificados como 'Yes' pelo LLM
# =========================
sample_df = df.sample(
    n=SAMPLE_SIZE,
    random_state=RANDOM_SEED
)

# =========================
# Remover colunas que não são necessárias para a anotação manual
# =========================
columns_to_remove = [
    "repository",
    "author",
    "author_association",
    "file_path",
    "line",
    "matched_keywords",
    "source_file",
    "is_design_restriction"
]

sample_df = sample_df.drop(columns=columns_to_remove, errors="ignore")

sample_df = sample_df.reset_index(drop=True)

# =========================
# Salvar amostra
# =========================
sample_df.to_csv(OUTPUT_CSV, index=False)

print(f"Amostra gerada com sucesso!")
print(f"Arquivo salvo em: {OUTPUT_CSV}")
