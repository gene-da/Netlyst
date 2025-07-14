from typing import Optional
from .Base import SpiceElement
from datetime import datetime
from textwrap import wrap

class TITLE(SpiceElement):
    def __init__(self, title: str, doc: Optional[str] = None) -> None:
        self.title = title.strip()
        self._doc = doc.strip() if doc else None
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super().__init__()

    def _wrap_lines(self, text: str, width: int = 60) -> list[str]:
        """Wrap text to a specified width without breaking words."""
        wrapped = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                wrapped.append("*")
                continue
            wrapped.extend([f"* {l}" for l in wrap(line, width=width - 2)])
        return wrapped

    def to_string(self) -> str:
        lines = ["*" * 60]

        if self._doc:
            lines.extend(self._wrap_lines(self._doc))

        lines.append(f"* Generated: {self.timestamp}")
        lines.append("*" * 60)
        lines.append(f".TITLE {self.title[:60]}")
        return "\n".join(lines)

    def to_line(self) -> str:
        """Single-line version without comments or timestamp."""
        return f".TITLE {self.title[:60]}"
        
class COMMENT(SpiceElement):
    def __init__(
        self, 
        comment: str, 
        doc: Optional[str] = None
    ) -> None:
        self.comment = comment
        self._doc = doc
        super().__init__()

    def to_string(self):
        doc_line = f"* {self._doc}" if self._doc else ""
        return f"{doc_line}\n* {self.comment}" if doc_line else f"* {self.comment}"

    def to_line(self):
        return self.to_string()
    
class END(SpiceElement):
    def __init__(self, doc: Optional[str] = None) -> None:
        self._doc = doc
        super().__init__()

    def to_string(self):
        doc_line = f"* {self._doc}" if self._doc else ""
        return f"{doc_line}\n.END" if doc_line else ".END"

    def to_line(self):
        return self.to_string()