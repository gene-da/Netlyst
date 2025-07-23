from typing import List, Optional, Tuple, Union
from Netlist.Components.Base.SpiceElement import SpiceElement

class IFBlock(SpiceElement):
    def __init__(
        self,
        if_condition: str,
        if_body: List[SpiceElement],
        elseif_blocks: Optional[List[Tuple[str, List[SpiceElement]]]] = None,
        else_body: Optional[List[SpiceElement]] = None,
        doc: Optional[str] = None
    ) -> None:
        super().__init__()
        self.if_condition = if_condition.strip()
        self.if_body = if_body
        self.elseif_blocks = elseif_blocks if elseif_blocks else []
        self.else_body = else_body if else_body else []
        self._doc = doc.strip() if doc else None

    @property
    def doc(self): return self._doc
    @doc.setter
    def doc(self, val): self._doc = str(val).strip() if val else None

    def to_string(self) -> str:
        lines = []
        if self._doc:
            lines.append(f"* {self._doc}")
        lines.append(f".if({self.if_condition})")
        lines.extend([el.to_string() for el in self.if_body])

        for condition, body in self.elseif_blocks:
            lines.append(f".elseif({condition})")
            lines.extend([el.to_string() for el in body])

        if self.else_body:
            lines.append(".else")
            lines.extend([el.to_string() for el in self.else_body])

        lines.append(".endif")
        return "\n".join(lines)

    def to_line(self) -> str:
        return f".if({self.if_condition}) ... .endif"
