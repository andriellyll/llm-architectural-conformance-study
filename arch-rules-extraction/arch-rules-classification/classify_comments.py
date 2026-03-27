import csv
from mistralai import Mistral
import dotenv
import time
import sys
from shared.prompts import get_design_rule_classification_prompt

csv.field_size_limit(sys.maxsize)

dotenv.load_dotenv()

client = Mistral()

INPUT_CSV = "../filter-dataset/matched_comments_from_dataset.csv"   # arquivo de entrada
OUTPUT_CSV = "classified_comments.csv"  # arquivo de saída

def classify_comment(comment):
    prompt = get_design_rule_classification_prompt(comment)

    try:
    
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao processar comentário: {e}")
        return "Error"

# --- EXECUÇÃO ---
with open(INPUT_CSV, newline='', encoding='utf-8') as infile, \
     open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["is_design_restriction"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        comment = row.get("comment_body", "")
        if not comment.strip():
            row["is_design_restriction"] = "Empty"
        else:
            label = classify_comment(comment)
            row["is_design_restriction"] = label
        writer.writerow(row)
        print(f"✓ Processado: {comment[:50]}... → {row['is_design_restriction']}")
        time.sleep(20)

print(f"\n✅ Classificação concluída! Resultados salvos em: {OUTPUT_CSV}")