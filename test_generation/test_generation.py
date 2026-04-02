from sqlalchemy import make_url
from test_generation.constants import *
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Settings
from dotenv import load_dotenv
from llama_index.llms.mistralai import MistralAI
import time
import os
import csv
from shared.prompts import get_test_generation_prompt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()


def get_input(rule, file_path):
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File path where the comment was made:
<<FILE_PATH>>
{file_path}
<<END_FILE_PATH>>

Code review comment:
<<COMMENT_START>>
{rule}
<<COMMENT_END>>
"""

system_prompt = get_test_generation_prompt()

##### SETUP LLM #####
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5",
    device="cpu"
)

Settings.llm = MistralAI(
    model="codestral-latest",
    temperature=0,
    system_prompt=system_prompt
)

##### CREATING THE INDEX #####
url = make_url(connection_string)

hybrid_vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name=table_name,
    embed_dim=embed_dim,
    hybrid_search=True,
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)

hybrid_index = VectorStoreIndex.from_vector_store(vector_store=hybrid_vector_store)

hybrid_query_engine = hybrid_index.as_query_engine(
    vector_store_query_mode = "hybrid", sparse_top_k=2
)

START_AT = 1  # número da linha a partir da qual o processamento deve começar (1-based)

# =====================
# CSV STREAMING
# =====================
INPUT_CSV = BASE_DIR / "../arch_rules_extraction/arch_rules_classification/design_restrictions_only.csv"
OUTPUT_CSV = BASE_DIR / "test_generation_results.csv"

with open(INPUT_CSV, newline="", encoding="utf-8") as infile, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["generated_test"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    if os.stat(OUTPUT_CSV).st_size == 0:
        writer.writeheader()

    for idx, row in enumerate(reader, start=1):

        if idx < START_AT:
            continue  # pula linhas já processadas

        rule = row.get("comment_body", "").strip()
        file_path = row.get("file_path", "").strip()

        if not rule:
            row["generated_test"] = ""
            writer.writerow(row)
            continue

        print(f"[{idx}] Gerando teste...")
        print(f"  Regra (preview): {rule[:80]}...")

        try:
            response = hybrid_query_engine.query(get_input(rule, file_path))
            row["generated_test"] = str(response)
            print("  ✔ Teste gerado")

        except Exception as e:
            row["generated_test"] = ""
            print(f"  ✖ Erro: {e}")

        writer.writerow(row)
        outfile.flush()  # 🔐 garante escrita imediata no disco
        time.sleep(20)

print("Processamento finalizado.")
