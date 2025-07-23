from typing import Optional
from Netlist.Components import SpiceElement
from datetime import datetime
from textwrap import wrap

class TITLE(SpiceElement):
    def __init__(self, title: str, doc: Optional[str] = None) -> None:
        self.title = title.strip()
        self._doc = doc.strip() if doc else None
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super().__init__()
        self._width = 100

    def _wrap_lines(self, text: str) -> list[str]:
        """Wrap text to a specified width without breaking words."""
        wrapped = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                wrapped.append("*")
                continue
            wrapped.extend([f"* {l}" for l in wrap(line, width=self._width - 2)])
        return wrapped

    def to_string(self) -> str:
        lines = ["*" * self._width]
        lines.append('*')

        if self._doc:
            lines.extend(self._wrap_lines(self._doc))

        lines.append(f"* Generated: {self.timestamp}")
        lines.append('*')
        lines.append(f".TITLE {self.title[:self._width]}")
        lines.append('*')
        lines.append("*" * self._width)

        return "\n".join(lines)


    def to_line(self) -> str:
        """Single-line version without comments or timestamp."""
        return f".TITLE {self.title[:self._width]}"
        
class COMMENT(SpiceElement):
    def __init__(
        self,
        comment: str,
        doc: Optional[str] = None,
        width: int = 100
    ) -> None:
        self.comment = comment
        self._doc = doc if doc else None
        self._width = width
        super().__init__()

    def _wrap_lines(self, text: str) -> list[str]:
        """Wraps lines for SPICE comment formatting, preserving indentation and tabs."""
        wrapped = []

        for line in text.splitlines():
            if not line.strip():
                wrapped.append("*")
                continue

            # Expand tabs into 4 spaces
            expanded = line.replace('\t', '    ')
            
            # Get leading whitespace (spaces only, no tabs at this point)
            leading_ws = len(expanded) - len(expanded.lstrip())
            indent = ' ' * leading_ws
            content = expanded.lstrip()

            # Wrap the content portion
            wrapped_lines = wrap(content, width=self._width - 2)

            for i, l in enumerate(wrapped_lines):
                if i == 0:
                    wrapped.append(f"* {indent}{l}")
                else:
                    wrapped.append(f"* {indent}{l}")

        return wrapped

    def to_string(self) -> str:
        lines = []
        if self._doc:
            lines.extend(self._wrap_lines(self._doc))
        lines.extend(self._wrap_lines(self.comment))
        return "\n".join(lines)

    def to_line(self) -> str:
        """Single-line version is not implement for COMMENT. This is meant to be easily passed into NgSpice as an easy to parse no comments."""
        raise NotImplementedError("Single-line version is not implement for COMMENT. This is meant to be easily passed into NgSpice as an easy to parse no comments.")
    
class END(SpiceElement):
    def __init__(self, doc: Optional[str] = None) -> None:
        self._doc = doc
        super().__init__()

    def to_string(self):
        doc_line = f"* {self._doc}" if self._doc else ""
        return f"{doc_line}\n.END" if doc_line else ".END"

    def to_line(self):
        return self.to_string()