import csv
import json
import os
import sys
import time
from mistralai import Mistral
import dotenv
import re
import requests
from shared.prompts import get_evaluation_prompt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

csv.field_size_limit(sys.maxsize)
dotenv.load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

client = Mistral()

INPUT_CSV = BASE_DIR / "../test_generation/test_generation_results.csv"
OUTPUT_CSV = BASE_DIR / "test_evaluation_results.csv"

MODEL_NAME = "mistral-large-latest"
SLEEP_SECONDS = 2  # ajuste conforme rate limit

def evaluate_test(rule, test_code):

    system_prompt = """
You are an expert in software architecture testing and ArchUnit.

You must evaluate generated architectural tests strictly and conservatively.
Do not assume correctness.
Base your judgment only on the provided rule and test code.
Be precise and technical.
"""

    user_prompt = get_evaluation_prompt(rule, test_code)
    try:

        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0
        }

        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()

        if "```" in content:
            content = re.sub(r"```json", "", content)
            content = re.sub(r"```", "", content)

        # Extrai apenas o trecho JSON (entre primeira { e última })
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            json_str = match.group()
            return json.loads(json_str)
        else:
            raise ValueError("JSON não encontrado na resposta")

    except Exception as e:
        print(f"Erro ao avaliar teste: {e}")
        return None

# --- EXECUÇÃO ---
with open(INPUT_CSV, newline='', encoding='utf-8') as infile, \
     open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)

    new_fields = [
        "syntactic_validity",
        "correct_archunit_usage",
        "semantic_alignment_score",
        "violation_detection_potential",
        "evaluation_explanation"
    ]

    fieldnames = reader.fieldnames + new_fields
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:

        rule = row.get("comment_body", "")
        test_code = row.get("generated_test", "")

        if not rule.strip() or not test_code.strip():
            print("Linha ignorada (regra ou teste vazio)")
            continue

        result = evaluate_test(rule, test_code)

        if result:
            row["syntactic_validity"] = result.get("syntactic_validity")
            row["correct_archunit_usage"] = result.get("correct_archunit_usage")
            row["semantic_alignment_score"] = result.get("semantic_alignment_score")
            row["violation_detection_potential"] = result.get("violation_detection_potential")
            row["evaluation_explanation"] = result.get("explanation")

        writer.writerow(row)

        print(f"✓ Avaliado")
        time.sleep(SLEEP_SECONDS)

print(f"\n✅ Classificação concluída! Resultados salvos em: {OUTPUT_CSV}")