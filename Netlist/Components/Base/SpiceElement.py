from abc import ABC, abstractmethod
from typing import Union, Optional
from Utilities.Converter import Conversion

class SpiceElement(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def to_string(self) -> str:
        """Return the SPICE netlist element as a formatted string."""
        pass
    
    def to_line(self) -> str:
        """Return the SPICE netlist line as a single line string."""
        return self.to_string()
    
    def __str__(self) -> str:
        return self.to_string()
    
    def _format_value(self, val: Optional[Union[int, float, str]]) -> Optional[str]:
        if val is None:
            return None
        if isinstance(val, str):
            return Conversion.spice(val)
        return Conversion.spice(float(val))

class Nodes:
    def __init__(self) -> None:
        self.nodes = {}
        
    def _format_node(self, index: Union[int, str]) -> str:
        """
        Formats node identifiers for SPICE compatibility.
        - Converts 0 or '0' to 'GND'
        - Accepts alphanumeric labels like 'IN', 'VDD', 'N001'
        - Normalizes all to clean string
        """
        if isinstance(index, (int, float)) and index == 0:
            return "GND"
        if isinstance(index, str):
            if index.strip() == "0":
                return "GND"
            return index.strip()

        return f"N{index:03d}"
            