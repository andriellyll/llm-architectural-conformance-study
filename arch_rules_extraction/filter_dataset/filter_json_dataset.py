import ijson

import csv

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 🔑 Palavras-chave 
KEYWORDS = [
    "must implement", "should implement", "must use", "should use", "must not implement", "discouraged",
    "should not implement", "must not use", "should not use", "required by", "recommended", "avoid",
    "discouraged", "enforced", "expected to", "intended to", "not intended", "as intended",
    "violates design", "design intent", "consistent with design", "interface", "abstract class", "base class",
    "subclass", "extends", "implements", "override", "inherit", "contract", "API",
    "service interface", "factory"
]

# this is a sample for demonstration purpose. dowload original dataset from https://www.kaggle.com/datasets/pelmers/github-public-pull-request-comments (we used mined-comments-25stars-25prs-Java.json)

INPUT_JSON = BASE_DIR / "mined_comments_sample.json"
OUTPUT_CSV = BASE_DIR / "matched_comments_from_dataset_sample.csv"

def contains_keywords(text: str):
    """
    Retorna a lista de palavras-chave encontradas no texto.
    A verificação é case-insensitive.
    """
    if not text:
        return []

    text_lower = text.lower()
    return [kw for kw in KEYWORDS if kw in text_lower]

def process_large_json():
    with open(INPUT_JSON, "rb") as f, \
         open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as out:

        writer = csv.writer(out)
        writer.writerow([
            "repository",
            "comment_url",
            "author",
            "author_association",
            "file_path",
            "line",
            "comment_body",
            "matched_keywords"
        ])

        total = 0
        matched = 0
        current_repo = None

        # Parsing evento a evento
        for prefix, event, value in ijson.parse(f):

            # captura o nome do repositório
            if prefix == "root" and event == "map_key":
                current_repo = value

            # início de um comentário individual
            elif prefix.endswith(".item") and event == "start_map":
                comment = {}

            # campos dentro do comentário
            elif prefix.endswith(".item.body"):
                comment["body"] = value
            elif prefix.endswith(".item.html_url"):
                comment["html_url"] = value
            elif prefix.endswith(".item.user"):
                comment["user"] = value
            elif prefix.endswith(".item.author_association"):
                comment["author_association"] = value
            elif prefix.endswith(".item.path"):
                comment["path"] = value
            elif prefix.endswith(".item.line"):
                comment["line"] = value

            # fim do comentário → processa
            elif prefix.endswith(".item") and event == "end_map":
                total += 1
                body = comment.get("body", "")
                found = contains_keywords(body)

                if found:
                    matched += 1
                    writer.writerow([
                        current_repo,
                        comment.get("html_url", ""),
                        comment.get("user", ""),
                        comment.get("author_association", ""),
                        comment.get("path", ""),
                        comment.get("line", ""),
                        body.replace("\n", " ").strip(),
                        ", ".join(found)
                    ])

        print(f"Total analisado: {total}")
        print(f"Com match: {matched}")
        print(f"Arquivo gerado: {OUTPUT_CSV}")

if __name__ == "__main__":
    process_large_json()