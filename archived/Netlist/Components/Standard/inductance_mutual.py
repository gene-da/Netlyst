from typing import Optional, Union
from Netlist.Components import SpiceElement, L

"""_summary_
KXXXXXXX LYYYYYYY LZZZZZZZ value
"""

class K(SpiceElement):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        inductor1: L,
        inductor2: L,
        coupling: Union[float, int, str],
        scope: str = "global",
        doc: Optional[str] = None
    ) -> None:
        super().__init__()

        # Name resolution
        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'K{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        # Instance registration
        if scope not in K._instances:
            K._instances[scope] = {}
        if resolved_name in K._instances[scope] and K._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate K-coupling name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        K._instances[scope][resolved_name] = self

        self.inductor1 = inductor1.name
        self.inductor2 = inductor2.name
        self._coupling = self._validate_coupling(coupling)
        self._doc = doc if doc else None

    # --- Coupling Validation ---
    @staticmethod
    def _validate_coupling(val):
        try:
            num = float(val)
        except (TypeError, ValueError):
            raise ValueError(f"K-coupling must be a float between 0 and 1: got {val}")

        if not (0 < num <= 1):
            raise ValueError(f"K-coupling must be in (0, 1], got {num}")

        return num

    @property
    def coupling(self): return self._coupling
    @coupling.setter
    def coupling(self, val): self._coupling = self._validate_coupling(val)

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        line = f"{self.name} {self.inductor1} {self.inductor2} {self.coupling}"
        return f"{doc_line}\n{line}" if doc_line else line

    to_line = to_string  # same logic