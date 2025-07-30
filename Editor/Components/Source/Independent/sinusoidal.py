from ..source import *
from typing import Optional, Union

""""
General form:
SIN(VO VA FREQ TD THETA PHASE)
"""

class SIN(IndependentSource):
    def __init__(
        self,
        vo: Union[float, int, str],
        va: Union[float, int, str],
        freq: Union[float, int, str],
        td: Optional[Union[float, int, str]] = None,
        theta: Optional[Union[float, int, str]] = None,
        phase: Optional[Union[float, int, str]] = None,
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.SINE
        )
        
        self._vo = self._format_value(vo)
        self._va = self._format_value(va)
        self._freq = self._format_value(freq)
        self._td = f'{self._format_value(td)}s' if td is not None else '0s'
        self._theta = self._format_value(theta)
        self._phase = self._format_value(phase)
        
        self._set_source_str([
            self._vo, self._va, self._freq, 
            self._td, self._theta, self._phase
        ])