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