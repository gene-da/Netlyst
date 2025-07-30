from ..source import *
from typing import Optional, Union

"""
General Form:
SFFM(VO VA FM MDI FC TD PHASEM PHASEC)
Examples:
V1 12 0 SFFM(0 2 20 45 1k 1m 0 0)
"""

class SFFM(IndependentSource):
    def __init__(
        self,
        vo: Union[float, int, str],
        va: Union[float, int, str],
        fm: Union[float, int, str],
        mdi: Union[float, int, str],
        fc: Union[float, int, str],
        td: Optional[Union[float, int, str]] = None,
        phase_m: Optional[Union[float, int, str]] = None,
        phase_c: Optional[Union[float, int, str]] = None,
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.SING_FREQ_FM
        )
        
        self._vo = self._format_value(vo)
        self._va = self._format_value(va)
        self._fm = self._format_value(fm)
        self._mdi = self._format_value(mdi)
        self._fc = self._format_value(fc)
        self._td = f'{self._format_value(td)}s' if td is not None else '0s'
        self._phase_m = self._format_value(phase_m)
        self._phase_c = self._format_value(phase_c)
        
        self._set_source_str([
            self._vo, self._va, self._fm, 
            self._mdi, self._fc, self._td,
            self._phase_m, self._phase_c
        ])