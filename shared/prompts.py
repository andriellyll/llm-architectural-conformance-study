def get_design_rule_classification_prompt(comment):
    return f"""
You are analyzing a GitHub pull request comment.
Decide if it expresses an **explicit design rule** about the system's **static structure**.

A **design rule** is a prescriptive statement about how **classes, interfaces, modules, packages, or methods** should be **structured or related** (e.g., inheritance, dependencies, composition, abstraction).
It expresses **constraints or principles** that affect the organization or relationships between code elements.

**Design rule examples**

* "Don't use abstract classes to set behavior for classes."
* "Controllers should not depend directly on repositories."
* "Use composition instead of inheritance."

**Not design rules**

* "Use the `Color` enum instead of a string." (implementation detail)
* "Add more tests." (testing)
* "Improve performance." (non-structural)
* "Use 4-space indentation." (style)

Output only one word:

* Yes → expresses a design rule or constraint about structure or relationships.
* No → otherwise.

**Comment:** {comment}"""


def get_test_generation_prompt():
    return  f"""
You are an expert software architect and test engineer specialized in Java and ArchUnit.

Your task is to generate a single ArchUnit test that verifies whether an architectural design rule — derived from a code review comment — is satisfied in the codebase.

You will receive:
  - A code review comment that may contain suggestions, structural constraints, or design recommendations.
  - The file path where the comment was made.
  - Relevant excerpts of ArchUnit documentation retrieved through RAG.

The documentation is provided only to support correct usage of the ArchUnit API.

IMPORTANT:
Your goal is NOT to implement the suggestion in the comment.
Your goal is to generate a test that verifies whether the architectural constraint implied by the comment is satisfied.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. First, semantically analyze the comment and extract the core architectural or design rule being suggested.

2. The comment may:
   - Be phrased as an order or suggestion.
   - Contain code snippets.
   - Contain quoted previous messages (lines starting with ">").
     - Lines starting with ">" refer to previous comments and should NOT be treated as the main rule unless the current comment reinforces them.
     - Focus on what the current author is asserting.

3. If the comment includes example code, analyze it to infer the intended design rule.
   - Do NOT copy or duplicate the example code.
   - Infer the structural intent (e.g., inheritance hierarchy, dependency constraint, abstraction requirement, layering rule, etc.).

4. Identify All Architectural Constraints Implied by the Rule
Determine whether the extracted rule implies one or more of the following types of architectural constraints (this list is not exhaustive):
  - Class existence or absence
  - Class location (package placement)
  - Class visibility (public, abstract, final, etc.)
  - Inheritance or interface implementation
  - Field presence, absence, or location
  - Method presence, absence, or location
  - Method invocation constraints
  - Class dependency constraints
  - Package-level restrictions
  - Annotation usage constraints
  - Layered architecture constraints
  - Movement of elements (e.g., a method or field should be moved to another class)
  - Creation of new abstractions (e.g., introduce an abstract superclass)
  - Multiple independent architectural verifications

If the rule implies multiple structural constraints, generate separate assertions for each one inside the same ArchUnit test.

5. Generate an ArchUnit test that checks whether the rule is satisfied.
   - Use declarative ArchUnit APIs whenever possible.
   - The retrieved ArchUnit documentation must be treated as contextual guidance, not as mandatory code templates.
   - The test must verify compliance.
   - The test must not implement the suggestion.
   - The test must not restate the comment text.
   - The test must not include explanations.
   - The test must not describe how the code should be written.
   - The test must only verify whether the rule is followed.

6. If you cannot derive a clear architectural or structural rule from the comment,
   return exactly:

   NO_ARCHITECTURAL_TEST_POSSIBLE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### **Input (Design Rule)**:
> Classes in the `service` package must not depend on classes in the `controller` package.

### **Output (Java Test Code)**:
```java
import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

public class ServiceLayerArchitectureTest {{

    @Test
    public void servicesShouldNotDependOnControllers() {{
        JavaClasses importedClasses = new ClassFileImporter()
                .importPackages("com.example");

        ArchRule rule = noClasses()
                .that().resideInAPackage("..service..")
                .should().dependOnClassesThat().resideInAPackage("..controller..");

        rule.check(importedClasses);
    }}
}}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT RULES (STRICT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Output ONLY:
  - A complete Java test class using JUnit and ArchUnit
  OR
  - The exact string: NO_ARCHITECTURAL_TEST_POSSIBLE

- Do NOT include:
  - Explanations
  - Natural language descriptions
  - Markdown formatting
  - Comments outside the Java code
  - Any text before or after the test class
"""

def get_evaluation_prompt(rule, test_code):
    return f"""
Evaluate the following generated ArchUnit test.

Architectural Rule (natural language):
"{rule}"

Generated Test:
```java
{test_code}
```

Evaluation Criteria:

1. syntactic_validity (true/false)

* Is the test valid Java syntax?
* Ignore missing imports unless they break structure.

2. correct_archunit_usage (true/false)

* Are ArchUnit APIs used correctly?
* Are classes, layers, or dependencies expressed using valid ArchUnit constructs?

3. semantic_alignment_score (0-2)
   0 = The test does not represent the rule.
   1 = The test partially represents the rule but is incomplete, overly broad, or imprecise.
   2 = The test clearly and correctly represents the rule.

4. violation_detection_potential (0-2)
   0 = The test would not fail if the rule were violated.
   1 = The test might fail in some violation scenarios but lacks robustness.
   2 = The test would reliably fail if the rule were violated.

Important:

* Be strict.
* If unsure, prefer the lower score.
* Do not justify excessively.
* Return ONLY valid JSON.

Return ONLY valid JSON in this format:

{{
"syntactic_validity": true/false,
"correct_archunit_usage": true/false,
"semantic_alignment_score": 0-2,
"violation_detection_potential": 0-2,
"explanation": "technical explanation (max 3 sentences)"
}}
"""