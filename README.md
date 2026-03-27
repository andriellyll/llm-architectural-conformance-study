# LLM-Based Architectural Conformance Study – Replication Package

This repository contains the replication package for our study on using Large Language Models (LLMs) to support **architectural conformance checking** through the extraction of architectural rules and automatic test generation.

The goal of this package is to enable other researchers and practitioners to **reproduce our experiments**, inspect intermediate artifacts, and extend our approach.

---

## 📦 Repository Structure

```
├── LICENSE
├── README.md
├── arch-rules-extraction
│   ├── arch-rules-classification
│   │   ├── architectural_restrictions_dataset.csv
│   │   ├── classify_comments.py
│   │   └── filter_architectural_rules_from_classification.py
│   └── filter-dataset
│       ├── filter_by_comment_year.ipynb
│       ├── filter_json_dataset.py
│       ├── get_comment_year.py
│       └── matched_comments_from_dataset.csv
├── evaluation
│   └── automatic_evaluation.py
├── sampling
│   ├── get_classification_validation_sample.py
│   └── get_manual_evaluation_sample.py
├── shared
│   └── prompts.py
└── test-generation
    ├── archunit-docs
    │   └── archunit
    ├── constants.py
    ├── db-creation.py
    └── test-generation.py
```

---

## 🔍 Overview of the Pipeline

The study is organized into four main stages:

1. **Dataset Filtering**
2. **Architectural Rule Extraction**
3. **Test Generation**
4. **Evaluation**

---

## 🧹 1. Dataset Filtering

Located in: `arch-rules-extraction/filter-dataset`

This step prepares the dataset by filtering and preprocessing comments.

### Main scripts:

* `filter_json_dataset.py` – filters the raw dataset
* `get_comment_year.py` – extracts temporal metadata
* `filter_by_comment_year.ipynb` – optional filtering by time
* `matched_comments_from_dataset.csv` – resulting filtered dataset

---

## 🏗️ 2. Architectural Rule Extraction

Located in: `arch-rules-extraction/arch-rules-classification`

This stage identifies architectural rules from developer discussions using LLM-based classification.

### Main scripts:

* `classify_comments.py` – classifies comments using LLM prompts
* `filter_architectural_rules_from_classification.py` – extracts only relevant architectural rules

### Dataset:

* `architectural_restrictions_dataset.csv` – labeled dataset used in the study

---

## 🧪 3. Sampling

Located in: `sampling`

This module generates samples for validation and manual evaluation.

### Scripts:

* `get_classification_validation_sample.py` – sample for classification validation
* `get_manual_evaluation_sample.py` – sample for human evaluation

---

## 🤖 4. Test Generation

Located in: `test-generation`

This stage generates architectural conformance tests based on extracted rules.

### Components:

* `test-generation.py` – main test generation pipeline
* `db-creation.py` – prepares the vector database for retrieval
* `constants.py` – configuration parameters
* `archunit-docs/` – local documentation used for retrieval-augmented generation

---

## 📊 5. Evaluation

Located in: `evaluation`

This module performs automatic evaluation of the generated tests.

### Script:

* `automatic_evaluation.py` – evaluates generated outputs against expected criteria

---

## 🧩 Shared Components

Located in: `shared`

* `prompts.py` – contains all prompts used across different stages of the pipeline

---

## ▶️ How to Run

> ⚠️ Before running, ensure you have Python installed and all required dependencies configured.

### Suggested execution order:

1. Filter dataset
2. Run classification
3. Extract architectural rules
4. Generate samples (optional)
5. Run test generation
6. Execute evaluation

Each script can be run independently, depending on the stage you want to reproduce.

---

## 📄 Reproducibility Notes

* All prompts used in the study are available in `shared/prompts.py`
* Intermediate datasets are included when possible
* The pipeline is modular, allowing partial reproduction (e.g., only classification or only test generation)

---

## 📌 Disclaimer

This repository is intended for **research and replication purposes only**. It does not provide a production-ready solution for architectural conformance checking.

---

## 🤝 Contributions

Contributions are welcome for:

* Improving reproducibility
* Extending experiments
* Supporting additional tools or datasets

---

## 📬 Contact

For questions or clarifications, please open an issue in this repository.
