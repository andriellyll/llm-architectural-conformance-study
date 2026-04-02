
# LLM-Based Architectural Conformance Study – Replication Package

This repository contains the replication package for our study on using Large Language Models (LLMs) to support **architectural conformance checking** through rule extraction and automatic test generation.

The package enables researchers and practitioners to **reproduce our pipeline**, inspect intermediate artifacts, and extend our approach.

---

## 📦 Repository Structure

```
.
├── arch_rules_extraction       # Rule extraction pipeline
├── datasets                    # Final and intermediate datasets
├── evaluation                  # Automatic evaluation scripts and results
├── sampling                    # Sampling for validation and manual analysis
├── shared                      # Prompts used across the pipeline
├── test_generation             # RAG-based test generation pipeline
├── requirements.txt
└── README.md

````

> ⚠️ Note: Sample files are included for demonstration purposes. The full dataset used in the study is described in the paper.

---

## ⚙️ Setup

### 1. Create virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### 2. Configure environment variables

Copy the example file and add your API keys:

```bash
cp .env.example .env
```

Then populate `.env` with:

* `MISTRAL_API_KEY`
* `GITHUB_TOKEN`

---

## ▶️ How to Run the Pipeline

> ⚠️ Run all commands from the **root directory** of the repository.

### Step 1 — Dataset Filtering

```bash
python3 -m arch_rules_extraction.filter_dataset.filter_json_dataset
python3 -m arch_rules_extraction.filter_dataset.filter_by_comment_year
```

This stage filters the original dataset and restricts comments by year.

---

### Step 2 — Architectural Rule Extraction

```bash
python3 -m arch_rules_extraction.arch_rules_classification.classify_comments
python3 -m arch_rules_extraction.arch_rules_classification.filter_architectural_rules_from_classification
```

This stage uses an LLM to identify comments that express architectural design rules.

---

### Step 3 — Setup Vector Database (PGVector)

```bash
docker run --name pgvector-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=archunit_docs \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
```

---

### Step 4 — Test Generation (RAG)

```bash
python3 -m test_generation.db_creation
python3 -m test_generation.test_generation
```

This stage builds the vector database from ArchUnit documentation and generates tests from extracted rules.

---

### Step 5 — Evaluation

```bash
python3 -m evaluation.automatic_evaluation
```

This stage evaluates the generated tests using an LLM-as-a-Judge approach.

---

## 📊 Datasets

This repository includes both **sample inputs for reproducibility** and **datasets generated in the study**.

### 🔹 Sample Input Data

The files in `arch_rules_extraction/filter_dataset/` (e.g., `mined_comments_sample.json`) correspond to a **small sample extracted from the original Kaggle dataset**.

These samples are provided to:
- Enable quick execution of the pipeline
- Avoid the overhead of processing the full dataset, which is large and time-consuming

All pipeline steps can be executed using these sample files.

---

### 🔹 Generated Datasets

Located in `datasets/`:

- `matched_comments_from_original_dataset.csv`  
  → Intermediate dataset obtained after applying **keyword-based filtering** to the original dataset

- `architectural_restrictions_dataset.csv`  
  → Final dataset produced in this study, containing **comments classified as design rules**

This final dataset corresponds to the output of the full pipeline when executed on the complete dataset.

---

### 🔹 Notes

- The **full original dataset** is not included due to its size, but can be obtained from Kaggle
- The provided sample ensures that the pipeline can be **validated end-to-end without requiring the full dataset**

---

## 🧩 Key Components

* `shared/prompts.py` → all prompts used in classification, generation, and evaluation
* `test_generation/archunit-docs/` → documentation used for retrieval (RAG)
* `evaluation/test_evaluation_results.csv` → example evaluation outputs
* `test_generation/test_generation_results.csv` → generated tests

---

## 🔁 Reproducibility Notes

* The pipeline is modular and can be executed partially (e.g., only classification or only test generation)
* Sample datasets are provided for quick execution
* Prompts and configurations are fully available

---

## 📌 Disclaimer

This repository is intended for **research and replication purposes only** and is not a production-ready solution.

<!-- ---

## 📚 Citation

If you use this repository, please cite our paper:

```
[TO BE FILLED AFTER PUBLICATION]
``` -->

---

## 📬 Contact

For questions or clarifications, please open an issue in this repository.
