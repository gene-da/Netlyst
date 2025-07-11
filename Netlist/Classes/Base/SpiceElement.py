from abc import ABC, abstractmethod
import math
import re
from typing import Union, Optional, Dict
import numpy as np
from Utilities.Converter import Conversion

class SpiceElement(ABC):
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def to_string(self) -> str:
        """Return the SPICE netlist line as a string."""
        pass
    
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
        Returns a SPICE-compatible node name like 'N001', 'N023', etc.

        Args:
            index (int | str): The index to format as a node name.

        Returns:
            str: Formatted node name starting with 'N' and followed by a zero-padded number.
        """
        if isinstance(index, str):
            if index.upper().startswith("N"):
                return index.upper()
            try:
                index = int(index)
            except ValueError:
                raise ValueError(f"Cannot convert string to node index: {index}")
        elif not isinstance(index, int):
            raise TypeError(f"Unsupported type for node index: {type(index).__name__}")

        return f"N{index:03d}"
            