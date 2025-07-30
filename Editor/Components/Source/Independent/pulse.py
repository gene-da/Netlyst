from ..source import *
from typing import Optional, Union

"""
General form:
PULSE(V1 V2 TD TR TF PW PER NP)
Examples:
VIN 3 0 PULSE(-1 1 2NS 2NS 2NS 50NS 100NS 5)
"""

class PULSE(IndependentSource):
    def __init__(
        self,
        v1: Union[float, int, str],
        v2: Union[float, int, str],
        td: Optional[Union[float, int, str]] = None,
        tr: Optional[Union[float, int, str]] = None,
        tf: Optional[Union[float, int, str]] = None,
        pw: Optional[Union[float, int, str]] = None,
        per: Optional[Union[float, int, str]] = None,
        np: Optional[Union[float, int, str]] = None,
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.PULSE
        )
        
        self._v1 = self._format_value(v1)
        self._v2 = self._format_value(v2)
        self._td = f'{self._format_value(td)}s' if td is not None else '0s'
        self._tr = f'{self._format_value(tr)}s' if tr is not None else '0s'
        self._tf = f'{self._format_value(tf)}s' if tf is not None else '0s'
        self._pw = f'{self._format_value(pw)}s' if pw is not None else '0s'
        self._per = f'{self._format_value(per)}s' if per is not None else '0s'
        self._np = f'{self._format_value(np)}s' if np is not None else '0s'

        self._set_source_str([
            self._v1, self._v2, self._td, self._tr,
            self._tf, self._pw, self._per, self._np
        ])