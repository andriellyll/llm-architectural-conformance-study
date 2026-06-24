# Replication Package: Can LLMs Turn Design Discussions into Architectural Tests?

This repository contains the replication package for the paper:

> Andrielly Lucena, Everton L. G. Alves, and João Brunet.
> **Can LLMs Turn Design Discussions into Architectural Tests? An Exploratory Study with Codestral.**
> 20th European Conference on Software Architecture (ECSA 2026).

The package enables researchers to reproduce our pipeline, inspect intermediate artifacts, and extend the approach.

---

## Artifact Type

This is a **hybrid artifact** comprising:
- **Executable components**: Python scripts implementing the full pipeline (filtering, classification, test generation, evaluation).
- **Non-executable components**: Datasets, prompts, annotation guidelines, and keyword list used in the study.

---

## Repository Structure

```
.
├── arch_rules_extraction/
│   ├── filter_dataset/
│   │   ├── filter_json_dataset.py              # Step 1a: keyword-based filtering
│   │   ├── filter_by_comment_year.py           # Step 1b: temporal filtering via GitHub API
│   │   ├── keywords.txt                        # Complete keyword list used in filtering
│   │   ├── mined_comments_sample.json          # Sample input (subset of Kaggle dataset)
│   │   ├── matched_comments_from_dataset_sample.csv
│   │   └── sample_dataset_filtered_2020.csv
│   └── arch_rules_classification/
│       ├── classify_comments.py                # Step 2a: LLM-based design rule classification
│       ├── filter_architectural_rules_from_classification.py  # Step 2b: filter positives
│       ├── design_restrictions_only.csv
│       └── sample_classified_comments.csv
├── datasets/
│   ├── matched_comments_from_original_dataset.csv       # Intermediate: after keyword filtering
│   ├── architectural_restrictions_dataset.csv           # Final: ~24,977 classified design rules
│   └── classification_validation_sample_annotated.csv  # Manual annotation sample (one annotator)
├── evaluation/
│   ├── automatic_evaluation.py                 # Step 5: LLM-as-a-Judge evaluation
│   ├── annotation_guidelines.md               # Annotation guidelines used by human annotators
│   ├── test_evaluation_results.csv            # Full automated evaluation results (~10,500 records)
│   ├── manual_evaluation_results.csv          # Full manual evaluation results (270 records)
│   └── manual_evaluation_projects.md          # List of 13 projects in the manual evaluation sample
├── sampling/
│   ├── get_classification_validation_sample.py # Sampling for classification validation
│   └── get_manual_evaluation_sample.py         # Sampling for manual test evaluation
├── shared/
│   └── prompts.py                              # All LLM prompts used in the study
├── test_generation/
│   ├── constants.py                            # Database and embedding configuration
│   ├── db_creation.py                          # Step 3: vector DB setup (PGVector + RAG)
│   ├── test_generation.py                      # Step 4: ArchUnit test generation
│   ├── test_generation_results.csv             # Full generated tests (~10,500 records)
│   └── archunit-docs/                          # ArchUnit documentation (RAG corpus)
├── docker-compose.yml                          # Database setup
├── CITATION.cff                                # Citation metadata
├── requirements.txt
└── .env.example
```

---

## Paper Claims to Artifacts Mapping

The table below maps the main quantitative claims in the paper to the corresponding artifacts in this package.

| Paper Claim | Artifact |
|---|---|
| 10,500 design-related comments extracted | `datasets/architectural_restrictions_dataset.csv` |
| Classifier precision: 83.33% | `datasets/classification_validation_sample_annotated.csv` + `evaluation/annotation_guidelines.md` |
| 23.87% of outputs were NO\_ARCHITECTURAL\_TEST\_POSSIBLE | `test_generation/test_generation_results.csv` |
| 97.92% syntactic validity (automated) | `test_generation/test_generation_results.csv` + `evaluation/test_evaluation_results.csv` |
| 67.01% semantic alignment >= 1 (automated) | `evaluation/test_evaluation_results.csv` |
| Manual evaluation: 270 tests, 13 projects | `evaluation/manual_evaluation_results.csv` + `evaluation/manual_evaluation_projects.md` |
| All LLM prompts | `shared/prompts.py` |
| Keyword list | `arch_rules_extraction/filter_dataset/keywords.txt` |
| Classification annotation guidelines | `evaluation/annotation_guidelines.md` |
| Classification validation data (both annotators, divided sample) | `datasets/classification_validation_sample_annotated.csv` |

---

## Setup

### Requirements

- Python 3.10 (tested on 3.10 on Linux/WSL2)
- Docker (for the vector database)
- Active [Mistral AI API key](https://console.mistral.ai/) (required for Steps 2, 4, and 5)
- GitHub personal access token (required for Step 1b only)

### 1. Create virtual environment and install dependencies

On Debian/Ubuntu (including WSL2), install the `venv` module for your Python version before creating the environment:

```bash
sudo apt install python3.10-venv   # replace 3.10 with your Python version (e.g. python3.11-venv)
```

```bash
python3 -m venv venv
source venv/bin/activate
```

Install PyTorch first (CPU-only):

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Then install the remaining dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values. All database variables have defaults that match `docker-compose.yml` and do not need to be changed unless you use a custom database setup.

### 3. Start the vector database

```bash
docker compose up -d
```

Wait for the container to be healthy before proceeding to Step 3 of the pipeline.

---

## Quick Verification (Smoke Test)

Run the two steps below to confirm that both the Python environment and the database container are correctly set up before running the full pipeline.

**Step 1 — Python environment** (no API key required, < 5 seconds)

```bash
python3 -m arch_rules_extraction.filter_dataset.filter_json_dataset
```

Expected output:
```
Total analisado: <N>
Com match: <M>
Arquivo gerado: arch_rules_extraction/filter_dataset/matched_comments_from_dataset_sample.csv
```

The script should complete in under 5 seconds and produce a non-empty CSV. If it fails, check that your virtual environment is active and dependencies are installed.

**Step 2 — Database container** (no API key required, < 1 minute)

```bash
docker compose up -d
docker compose ps
```

Expected output: the `pgvector` service listed with status `healthy`. If the container does not reach a healthy state within one minute, check that Docker is running and port 5432 is available.

> Steps 1 and 2 together confirm that the full environment is ready for the pipeline. API keys are only required from Step 2 of the pipeline onward (classification, test generation, and evaluation); they are not needed for the smoke test.

---

## Pipeline Execution

> Run all commands from the **root directory** of the repository.

### Step 1 — Dataset Filtering

**1a. Keyword-based filtering**

```bash
python3 -m arch_rules_extraction.filter_dataset.filter_json_dataset
```

Input: `arch_rules_extraction/filter_dataset/mined_comments_sample.json`
Output: `arch_rules_extraction/filter_dataset/matched_comments_from_dataset_sample.csv`

> For the full study, this script was run on the complete Kaggle dataset (see Datasets section). The sample file is provided for end-to-end validation without downloading the full dataset.

**1b. Temporal filtering (requires `GITHUB_TOKEN`)**

```bash
python3 -m arch_rules_extraction.filter_dataset.filter_by_comment_year
```

Filters to comments created from 2020 onward by querying the GitHub REST API.
Estimated time on sample: < 1 minute (depends on GitHub API rate limits).

---

### Step 2 — Architectural Rule Classification

**2a. LLM classification (requires `MISTRAL_API_KEY`)**

```bash
python3 -m arch_rules_extraction.arch_rules_classification.classify_comments
```

Model: `mistral-small-latest`. Rate-limited to 5 seconds per record.
Estimated time on sample (~50 records): ~5 minutes.
Estimated cost on sample: < $0.01 USD.

**2b. Filter positives**

```bash
python3 -m arch_rules_extraction.arch_rules_classification.filter_architectural_rules_from_classification
```

Output: `arch_rules_extraction/arch_rules_classification/design_restrictions_only.csv`

---

### Step 3 — Vector Database Creation

```bash
python3 -m test_generation.db_creation
```

Parses and indexes ArchUnit HTML documentation from `test_generation/archunit-docs/` using PGVector and the `BAAI/bge-large-en-v1.5` embedding model (1024 dimensions, runs on CPU).
Estimated time: 5–15 minutes (first run downloads the embedding model).

---

### Step 4 — ArchUnit Test Generation (requires `MISTRAL_API_KEY`)

```bash
python3 -m test_generation.test_generation
```

Model: `codestral-latest`. Rate-limited to 20 seconds per record.
Estimated time on sample (~50 records): ~17 minutes.
Estimated cost on sample: < $0.05 USD.
Output: appends to `test_generation/test_generation_results.csv`.

Expected output includes a `generated_test` column containing either a complete Java ArchUnit test class or the string `NO_ARCHITECTURAL_TEST_POSSIBLE`.

---

### Step 5 — Automated Evaluation (requires `MISTRAL_API_KEY`)

```bash
python3 -m evaluation.automatic_evaluation
```

Model: `mistral-large-latest`. Rate-limited to 2 seconds per record.
Estimated time on sample: ~5 minutes.
Estimated cost on sample: < $0.02 USD.
Output: appends to `evaluation/test_evaluation_results.csv`.

Expected output includes columns: `syntactic_validity`, `correct_archunit_usage`, `semantic_alignment_score` (0–2), `violation_detection_potential` (0–2), `evaluation_explanation`.

---

## Datasets

### Sample Input Data

`arch_rules_extraction/filter_dataset/mined_comments_sample.json` is a small subset of the original Kaggle dataset, provided to allow end-to-end pipeline execution without downloading the full data.

The full original dataset is available at:
> Elmers, P. (2023). *GitHub Public Pull Request Comments*. Kaggle.
> https://www.kaggle.com/datasets/pelmers/github-public-pull-request-comments
>
> File used: `mined-comments-25stars-25prs-Java.json`

### Generated Datasets (Study Outputs)

| File | Description | Rows |
|---|---|---|
| `datasets/matched_comments_from_original_dataset.csv` | After keyword-based filtering on full dataset | — |
| `datasets/architectural_restrictions_dataset.csv` | After LLM classification on full dataset | ~24,977 |
| `test_generation/test_generation_results.csv` | Full generated ArchUnit tests | ~10,500 |
| `evaluation/test_evaluation_results.csv` | Full automated evaluation results | ~10,500 |
| `evaluation/manual_evaluation_results.csv` | Manual evaluation of 270 tests (270 tests, 13 projects) | 270 |

---

## LLM Prompts

All prompts used in the study are available in `shared/prompts.py`:

- `get_design_rule_classification_prompt()` — used in Step 2 (Mistral Small)
- `get_test_generation_prompt()` — used in Step 4 (Codestral)
- `get_evaluation_prompt()` — used in Step 5 (Mistral Large)

---

## Manual Evaluation

The paper reports two manual evaluation phases:

**Classification validation** (Section 3.1): a statistically representative sample of automatically classified comments was annotated by two evaluators (one paper author and one software engineering practitioner with 5 years of experience), who divided the sample between them. The annotation guidelines are in `evaluation/annotation_guidelines.md`. The combined annotations from both evaluators are available in `datasets/classification_validation_sample_annotated.csv` (columns: `comment_url`, `comment_body`, `is_design_rule`, `annotator_notes`). Agreement with the manual annotations yielded a classifier precision of **83.33%**.

**Test evaluation** (Section 3.2): a stratified random sample of 270 generated tests from 13 projects was evaluated manually following the same four criteria used in the automated phase (defined in `shared/prompts.py` → `get_evaluation_prompt()`). The sampling script is in `sampling/get_manual_evaluation_sample.py`. The full manual evaluation data — including LLM-as-a-Judge scores, human annotations, mutation test results, and annotator agreement columns — is in `evaluation/manual_evaluation_results.csv`. The list of 13 projects covered by the sample is in `evaluation/manual_evaluation_projects.md`.

---

## Reproducibility Notes

- The pipeline is modular: each step can be run independently.
- LLM outputs are non-deterministic. Results may vary slightly across runs, but should remain within the ranges reported in the paper (e.g., syntactic validity ~97%, semantic alignment >= 1 ~67%).
- Rate limits are built into the scripts; do not remove them to avoid API quota errors.
- The embedding model (`BAAI/bge-large-en-v1.5`) is downloaded automatically on first run via HuggingFace.

---

## Citation

If you use this artifact, please cite:

```bibtex
@inproceedings{lucena2026llm,
  title     = {Can {LLMs} Turn Design Discussions into Architectural Tests?
               An Exploratory Study with Codestral},
  author    = {Lucena, Andrielly and Alves, Everton L. G. and Brunet, Jo{\~a}o},
  booktitle = {Proceedings of the 20th European Conference on Software Architecture (ECSA 2026)},
  year      = {2026}
}
```

---

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contact

For questions or clarifications, please open an issue in this repository.
