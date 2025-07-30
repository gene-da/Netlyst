from ...Base import *
from typing import Optional, Union
from enum import Enum

class Points(Enum):
    dec = 'dec'
    oct = 'oct'
    lin = 'lin'

class AC(SpiceElement):
    def __init__(
        self,
        variation: Points,
        pts: Union[str, int, float],
        fstart: Union[str, int, float],
        fstop: Union[str, int, float],
        doc: Optional[str] = None,
    ) -> None:
        super().__init__(
            doc=doc, 
        )
        
        if not isinstance(variation, Points):
            raise TypeError(f"Invalid type for variation: {type(variation)}. Expected Points Enum.")
        self._variation = variation
        self._pts = self._format_value(pts)
        self._fstart = self._format_value(fstart)
        self._fstop = self._format_value(fstop)
        
        self.id.etype = SpiceElementType.ANALYSIS

    @property
    def variation(self) -> Points:
        return self._variation
    @variation.setter
    def variation(self, value: Points) -> None:
        if not isinstance(value, Points):
            raise TypeError(f"Invalid type for variation: {type(value)}. Expected Points Enum.")
        self._variation = value

    @property
    def pts(self) -> Union[str, int, float]:
        return self._pts
    @pts.setter
    def pts(self, value: Union[str, int, float]) -> None:
        self._pts = self._format_value(value)
    
    @property
    def fstart(self) -> Union[str, int, float]:
        return self._fstart
    @fstart.setter
    def fstart(self, value: Union[str, int, float]) -> None:
        self._fstart = self._format_value(value)

    @property
    def fstop(self) -> Union[str, int, float]:
        return self._fstop
    @fstop.setter
    def fstop(self, value: Union[str, int, float]) -> None:
        self._fstop = self._format_value(value)

    def to_string(self) -> str:
        if self._doc:
            return f'{"\n".join(self._wrap_lines(self._doc))}\n.ac {self._variation.value} {self._pts} {self._fstart} {self._fstop}'
        return f'.ac {self._variation.value} {self._pts} {self._fstart} {self._fstop}'

    def to_line(self):
        return f'.ac {self._variation.value} {self._pts} {self._fstart} {self._fstop}'