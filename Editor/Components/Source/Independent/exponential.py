from ..source import *
from typing import Optional, Union

"""
General form:
EXP(V1 V2 TD1 TAU1 TD2 TAU2)
"""

class EXP(IndependentSource):
    def __init__(
        self,
        v1: Union[float, int, str],
        v2: Union[float, int, str],
        td1: Optional[Union[float, int, str]] = None,
        tau1: Optional[Union[float, int, str]] = None,
        td2: Optional[Union[float, int, str]] = None,
        tau2: Optional[Union[float, int, str]] = None,
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.EXP
        )
        
        self._v1 = self._format_value(v1)
        self._v2 = self._format_value(v2)
        self._td1 = f'{self._format_value(td1)}s' if td1 is not None else '0s'
        self._tau1 = f'{self._format_value(tau1)}s' if tau1 is not None else '0s'
        self._td2 = f'{self._format_value(td2)}s' if td2 is not None else '0s'
        self._tau2 = f'{self._format_value(tau2)}s' if tau2 is not None else '0s'
        
        self._set_source_str([
            self._v1, self._v2, self._td1, 
            self._tau1, self._td2, self._tau2
        ])