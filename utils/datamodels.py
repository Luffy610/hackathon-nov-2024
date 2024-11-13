from dataclasses import field
from llmx import TextGenerationConfig
from pydantic.dataclasses import dataclass
from typing_extensions import Optional, List, Any


@dataclass
class Goal:
    question: str
    visualization: str
    rationale : str
    index: Optional[int] = 0

    def _repr_markdown_(self):
        return f"""
### Goal {self.index}

---

**Question:** {self.question}

**Visualization:** `{self.visualization}`

**Rationale:** {self.rationale}
"""


class Persona:
    persona: str
    rationale: str

    def _repr_markdown_(self):
        return f"""
### Persona
---

**Persona:** {self.persona}

**Rationale:** {self.rationale}

"""

@dataclass
class Summary:
    name: str
    file_name: str
    dataset_description: str
    field_names: List[Any]
    fields: Optional[List[Any]] = None

    def _repr_markdown_(self):
        field_lines = "\n".join([f"- **{name}:** {field}" for name,
                                field in zip(self.field_names, self.fields)])
        return f"""
## Dataset Summary

---

**Name:** {self.name}

**File Name:** {self.file_name}

**Dataset Description:**

{self.dataset_description}

**Fields:**

{field_lines}
"""
