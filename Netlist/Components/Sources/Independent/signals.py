from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from Utilities.Converter import Conversion


class SIGNAL(ABC):
    """Base class for signal sources."""
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
        return "SIGNAL"
    
@dataclass
class PULSE():
    def __init__(
        self,
        v1: Union[float, int, str],
        v2: Union[float, int, str],
        td: Union[float, int, str],
        tr: Union[float, int, str],
        tf: Union[float, int, str],
        pw: Union[float, int, str],
        per: Union[float, int, str],
        np: Union[float, int, str],
    ) -> None:
        """Pulse Source Parameters

        Args:
            v1 (Union[float, int, str]): Initial voltage.
            v2 (Union[float, int, str]): Final voltage.
            td (Union[float, int, str]): Delay time.
            tr (Union[float, int, str]): Rise time.
            tf (Union[float, int, str]): Fall time.
            pw (Union[float, int, str]): Pulse width.
            per (Union[float, int, str]): Period.
            np (Union[float, int, str]): Number of pulses.
        """
        super().__init__()
        self.v1 = Conversion.spice(v1)
        self.v2 = Conversion.spice(v2)
        self.td = Conversion.spice(td)
        self.tr = Conversion.spice(tr)
        self.tf = Conversion.spice(tf)
        self.pw = Conversion.spice(pw)
        self.per = Conversion.spice(per)
        self.np = Conversion.spice(np)

    def __str__(self) -> str:
        return f"PULSE {self.v1} {self.v2} {self.td} {self.tr} {self.tf} {self.pw} {self.per} {self.np}"