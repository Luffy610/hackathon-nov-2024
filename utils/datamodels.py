import base64
from dataclasses import field
from llmx import TextGenerationConfig
from pydantic.dataclasses import dataclass
from typing import Optional, List, Any, Union, Dict


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

@dataclass
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

@dataclass
class ChartExecutorResponse:

    spec: Optional[Union[str, Dict]]
    status: bool
    raster: Optional[str]
    code: str
    library: str
    error: Optional[Dict] = None

    def _repr_mimebundle(self, include=None, exclude=None):
        bundle = {"text/plain": self.code}
        if self.raster is not None:
            bundle["image/png"] = self.raster
        if self.spec is not None:
            bundle["application/vnd.vegalite.v5+json"] = self.spec

        return bundle

    def savefig(self, path):
        if self.raster:
            with open(path, 'wb') as f:
                f.write(base64.b64decode(self.raster))
        else:
            raise FileNotFoundError("No ratser image to save")