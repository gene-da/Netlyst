from Netlist.Components.Base.SpiceElement import SpiceElement
from typing import Optional

class FUNC(SpiceElement):
    def __init__(
        self,
        indent: str,
        expression: str,
        doc: Optional[str] = None
    ) -> None:
        super().__init__()
        self.indent = indent.strip()
        self.expression = expression.strip()
        self._doc = doc.strip() if doc else None

    @property
    def doc(self) -> Optional[str]:
        return self._doc

    @doc.setter
    def doc(self, value: Optional[str]):
        self._doc = value.strip() if value else None

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        func_line = f"{self.indent} {self.expression}".strip()
        return f"{doc_line}\n{func_line}" if doc_line else func_line

    def to_line(self) -> str:
        return f"{self.indent} {self.expression}".strip()


if __name__ == "__main__":
    f = FUNC(
        indent=".FUNC",
        expression="Gain(x, y) = x * y + 1",
        doc="Defines a simple gain function"
    )

    print(f.to_string())
    # Output:
    # * Defines a simple gain function
    # .FUNC Gain(x, y) = x * y + 1

    print(f.to_line())
    # Output:
    # .FUNC Gain(x, y) = x * y + 1
