import os
import pandas as pd
import requests
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from dotenv import load_dotenv

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()


INPUT_CSV = BASE_DIR / "matched_comments_from_dataset_sample.csv"
OUTPUT_CSV = BASE_DIR / "sample_dataset_with_comment_year.csv"

CACHE_FILE = BASE_DIR / "comment_year_cache.json"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

MAX_WORKERS = 8

# -----------------------------
# Extrair partes da URL
# -----------------------------
def parse_comment_url(url):

    if not isinstance(url, str):
        return None, None, None

    pattern = r"github\.com/([^/]+)/([^/]+)/pull/\d+#discussion_r(\d+)"
    match = re.search(pattern, url)

    if match:
        owner = match.group(1)
        repo = match.group(2)
        comment_id = match.group(3)
        return owner, repo, comment_id

    return None, None, None


# -----------------------------
# Buscar ano
# -----------------------------
def fetch_comment_year(owner, repo, comment_id):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/comments/{comment_id}"

    while True:

        try:

            r = requests.get(url, headers=HEADERS)

            if r.status_code == 200:
                created = r.json()["created_at"]
                return int(created[:4])

            elif r.status_code == 403:
                print("Rate limit... esperando")
                time.sleep(60)

            else:
                return None

        except:
            time.sleep(2)


# -----------------------------
# Cache
# -----------------------------
try:
    with open(CACHE_FILE) as f:
        cache = json.load(f)
except:
    cache = {}


# -----------------------------
# Dataset
# -----------------------------
df = pd.read_csv(INPUT_CSV)

parsed = df["comment_url"].apply(parse_comment_url)

df["owner"] = parsed.apply(lambda x: x[0])
df["repo"] = parsed.apply(lambda x: x[1])
df["comment_id"] = parsed.apply(lambda x: x[2])


unique_comments = df[["owner","repo","comment_id"]].drop_duplicates()

tasks = []

for owner, repo, cid in unique_comments.itertuples(index=False):

    if cid not in cache:
        tasks.append((owner, repo, cid))

print("Consultas necessárias:", len(tasks))


# -----------------------------
# Paralelização
# -----------------------------
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = {}

    for owner, repo, cid in tasks:
        futures[executor.submit(fetch_comment_year, owner, repo, cid)] = cid

    for future in tqdm(as_completed(futures), total=len(futures)):

        cid = futures[future]

        try:
            year = future.result()
        except:
            year = None

        cache[cid] = year

        if len(cache) % 200 == 0:
            with open(CACHE_FILE, "w") as f:
                json.dump(cache, f)


with open(CACHE_FILE, "w") as f:
    json.dump(cache, f)


# -----------------------------
# Aplicar ao dataset
# -----------------------------
df["comment_year"] = df["comment_id"].map(cache)

print("Total comments before filtering:", len(df))

df_filtered = df[df["comment_year"] >= 2020]

print("Total comments after filtering:", len(df_filtered))

df_filtered.to_csv(BASE_DIR / "sample_dataset_filtered_2020.csv", index=False)

print("Filtered dataset saved:", OUTPUT_CSV)