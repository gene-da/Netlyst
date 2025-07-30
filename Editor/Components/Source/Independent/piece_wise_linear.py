from ..source import *
from typing import Optional, Union, List
from dataclasses import dataclass

"""
General form:
PWL(T1 V1 <T2 V2 T3 V3 T4 V4 ...>) <r=value> <td=value>
Examples:
VCLOCK 7 5 PWL(0 -7 10NS -7 11NS -3 17NS -3 18NS -7 50NS -7)
+ r=0 td=15NS
"""

@dataclass
class VT:
    t: Union[float, int, str]
    v: Union[float, int, str]
    
    def _format_value(self, val: Optional[Union[int, float, str]]) -> Optional[str]:
        if val is None:
            return None
        if isinstance(val, str):
            return Conversion.spice(val)
        return Conversion.spice(float(val))
    
    def to_string(self):
        return f'{self._format_value(self.v)} {self._format_value(self.t)}s'

class PWL(IndependentSource):
    def __init__(
        self,
        tv: VT,
        additional_values: Optional[List[VT]] = None,
        r: Optional[Union[float, int, str]] = None,
        td: Optional[Union[float, int, str]] = None,
        
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.PIECE_WISE
        )
        self._values = [tv.to_string()]

        if additional_values:
            for vt in additional_values:
                self._values.append(vt.to_string())

        if r:
            self._r = f'r={Conversion.spice(r)}'
        

        if td:
            self._td = f'td={Conversion.spice(td)}'

        self._set_source_str(self._values)

        def __str__(self):
            return f'PWL({self.to_string()}) {self._r} {self._td}'