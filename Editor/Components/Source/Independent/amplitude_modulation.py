from ..source import *
from typing import Optional, Union, List, Tuple
from dataclasses import dataclass

"""AM(VO VMO VMA FM FC TD PHASEM PHASEC)"""

class AM(IndependentSource):
    def __init__(
        self,
        vo: Union[float, int, str],
        vmo: Union[float, int, str],
        vma: Optional[Union[float, int, str]] = None,
        fm: Optional[Union[float, int, str]] = None,
        fc: Optional[Union[float, int, str]] = None,
        td: Optional[Union[float, int, str]] = None,
        phase_m: Optional[Union[float, int, str]] = None,
        phase_c: Optional[Union[float, int, str]] = None,
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.AMP_MOD
        )
        
        self._vo = self._format_value(vo)
        self._vmo = self._format_value(vmo)
        self._vma = self._format_value(vma)
        self._fm = self._format_value(fm)
        self._fc = self._format_value(fc)
        self._td = self._format_value(td)
        self._phase_m = self._format_value(phase_m)
        self._phase_c = self._format_value(phase_c)
        
        self._set_source_str([
            self._vo, self._vmo, self._vma, 
            self._fm, self._fc, f'{self._td}s', 
            self._phase_m, self._phase_c
        ])