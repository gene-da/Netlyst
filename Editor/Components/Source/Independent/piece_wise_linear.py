from ..source import *
from typing import Optional, Union, List, Tuple
from dataclasses import dataclass

"""
General form:
PWL(T1 V1 <T2 V2 T3 V3 T4 V4 ...>) <r=value> <td=value>
Examples:
VCLOCK 7 5 PWL(0 -7 10NS -7 11NS -3 17NS -3 18NS -7 50NS -7)
+ r=0 td=15NS
"""

@dataclass
class _VT:
    t: Union[float, int, str]
    v: Union[float, int, str]
    
    def _format_value(self, val: Optional[Union[int, float, str]]) -> Optional[str]:
        if val is None:
            return None
        if isinstance(val, str):
            return Conversion.spice(val)
        return Conversion.spice(float(val))
    
    def to_string(self):
        if self.t == 0:
            time = '0'
        else:
            time = f'{self._format_value(self.t)}s'

        return f'{time} {self._format_value(self.v)}'

class PWL(IndependentSource):
    def __init__(
        self,
        tv: List[Tuple[Union[float, int, str], Union[float, int, str]]],
        r: Optional[Union[float, int, str]] = None,
        td: Optional[Union[float, int, str]] = None,
        
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.PIECE_WISE
        )
        values = []

        for t, v in tv:
            vt = _VT(t, v)
            values.append(vt.to_string())

        self._set_source_str(values)

        if r is not None:
            self._r = f'r={Conversion.spice(r)}'
        else:
            self._r = None
        
        if td is not None:
            self._td = f'td={Conversion.spice(td)}s'
        else:
            self._td = None
    
    def to_string(self) -> str:
        if self._r is None or self._td is None:
            return f'{self.source_type.value}({self.source_str})'
        else:
            extra = []
            if self._r is not None:
                extra.append(self._r)
            if self._td is not None:
                extra.append(self._td)

            return f'{self.source_type.value}({self.source_str}) {' '.join(extra)}'