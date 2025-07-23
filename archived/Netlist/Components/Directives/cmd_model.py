from Netlist.Components import SpiceElement
from .start_end_line import COMMENT
from typing import Optional

"""
.model mname type(pname1=pval1 pname2=pval2 ... )
"""
class MODEL(SpiceElement):
    def __init__(self, name: str, type: str, mod: str, doc: Optional[str] = None) -> None:
        self.name = name
        self.type = type
        self.mod = mod
        self._doc = doc
        super().__init__()

    def to_string(self):
        lines = []

        # Reuse wrapped doc from COMMENT class if available
        if self._doc:
            doc_comment = COMMENT(self._doc)
            lines.append(doc_comment.to_string())

        header = f'{".model":<8} {self.name:<8} {self.type:<8}'
        lines.append(header)

        current_line = "+"
        for token in self.mod.split():
            if len(current_line) + len(token) + 1 > 80:
                lines.append(current_line)
                current_line = "+"
            current_line += f" {token}"

        if current_line.strip() != "+":
            lines.append(current_line)

        return "\n".join(lines)

    def to_line(self):
        doc_line = COMMENT(self._doc).to_line() if self._doc else ""
        model_line = f".MODEL {self.name} {self.type} ({self.mod})"
        return f"{doc_line}\n{model_line}" if doc_line else model_line