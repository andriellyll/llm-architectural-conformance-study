# Annotation Guidelines – Manual Validation of Comments Classified as Design Rules

## 1. Research Context

This activity is part of academic research in Software Engineering, investigating the ability of LLMs to generate architectural conformance tests for **design rules related to the static structure of systems** discussed in GitHub pull request comments.

A dataset of approximately 24,000 comments was built, extracted from real project pull requests and automatically classified by an LLM as design rules. This step aims to **manually validate the quality of this classification** from a statistically representative sample.

---

## 2. What is a "Design Rule" in This Study

In this work, a **design rule** is defined in a **restrictive and explicit** manner.

A comment **expresses a design rule** if it contains a **prescriptive statement about the system's static structure**, indicating how **classes, interfaces, modules, packages, or methods** should be **organized or related**.

These rules typically involve:

- Dependencies between components
- Inheritance or composition relationships
- Coupling restrictions
- Structural principles of code organization

### Concrete examples of design rules

- "Controllers should not depend directly on repositories."
- "Use composition instead of inheritance."
- "Don't use abstract classes to define behavior."
- "Move this class to package controller."

### Examples that are NOT design rules

- "Use the `Color` enum instead of a string." — implementation detail
- "Add more tests." — testing concern
- "Improve performance." — non-structural concern
- "Use 4-space indentation." — style concern

Comments that do not **clearly** express a structural rule or restriction **should not** be classified as design rules.

---

## 3. Dataset and Sampling

The complete dataset contains approximately 24,000 comments automatically classified by the model.

Since manual validation of the entire dataset is infeasible, a **random sample of approximately 380 comments** was selected, calculated using standard statistical criteria (95% confidence level, 5% margin of error).

This sample is representative of the total set, allowing a rigorous evaluation of the automatic classification reliability.

---

## 4. Annotation Procedure

For each comment, the annotator should:

1. Read the comment carefully.
2. Decide whether it **explicitly expresses a structural design rule**, according to the definition in this document.
3. Mark **one** option:
   - **Yes** → expresses a structural design rule.
   - **No** → does not express this type of rule.
4. (Optional) Flag ambiguous or difficult-to-classify cases with a note.

**Alignment phase:** Before individual annotation begins, annotators jointly analyze a small portion of the sample (20 comments) to align understanding of the design rule definition and establish common classification criteria. This step aims to reduce inter-annotator disagreement and increase the consistency of the manual validation.

**Inter-annotator agreement:** Annotators then independently classify the same 40 comments. Fleiss' kappa is computed. If agreement reaches κ ≥ 0.7, the remaining comments are distributed among participants for individual annotation.

During annotation, use **exclusively** the definition presented in this document when making decisions.

---

## 5. Final Considerations

There are no individually "correct" or "wrong" answers. The objective of this step is to evaluate the reliability of the automatic classification and identify patterns of model error.

---

## 6. Usage in the Study

The guidelines in this document were used in the **classification validation** phase of the study (Section 3.1 of the paper), in which a statistically representative sample of automatically classified comments was independently annotated by two evaluators: one of the paper's authors and one software engineering practitioner with five years of experience.

Agreement with the manual annotations yielded a classifier **precision of 83.33%**.

For the **test evaluation** phase (Section 3.2 of the paper), the evaluation criteria are defined in `shared/prompts.py` (function `get_evaluation_prompt()`), following the same four-criterion structure used by the automated LLM-as-a-Judge approach.
