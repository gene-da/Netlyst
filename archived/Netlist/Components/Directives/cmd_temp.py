from Netlist.Components.Base.SpiceElement import SpiceElement
from typing import Optional, Union

class TEMP(SpiceElement):
    def __init__(self, value: Optional[Union[float, int, str]] = None, doc: Optional[str] = None) -> None:
        super().__init__()
        self._doc = str(doc).strip() if doc else None
        self.value = self._parse_temp(value)

    @property
    def doc(self) -> Optional[str]:
        return self._doc

    @doc.setter
    def doc(self, value: Optional[str]):
        self._doc = value.strip() if value else None

    def _parse_temp(self, val: Optional[Union[str, float, int]]) -> float:
        """
        Parses a temperature input and returns Celsius as float.
        Accepts: float/int (assumes Celsius), str with units like '25C' or '298K'.
        """
        if val is None:
            return 27.0  # SPICE default

        if isinstance(val, (int, float)):
            return float(val)

        if isinstance(val, str):
            val = val.strip().upper()

            if val.endswith("C"):
                return float(val[:-1])
            elif val.endswith("K"):
                return float(val[:-1]) - 273.15
            elif val.endswith("F"):
                return (float(val[:-1]) - 32) * (5/9)
            else:
                # Assume raw Celsius
                try:
                    return float(val)
                except ValueError:
                    raise ValueError(f"Invalid temperature format: '{val}'")

        raise TypeError(f"TEMP value must be float, int, or temperature string, not {type(val)}")

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        temp_line = f".TEMP {self.value:.3f}"
        return f"{doc_line}\n{temp_line}" if doc_line else temp_line

    def to_line(self) -> str:
        return f".TEMP {self.value:.3f}"
