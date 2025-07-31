from ..source import *
from typing import Optional, Union

"""TRNOISE(NA NT NALPHA NAMP RTSAM RTSCAPT RTSEMT)"""

class TRNOISE(IndependentSource):
    def __init__(
        self,
        na: Union[float, int, str],
        nt: Union[float, int, str],
        nalpha: Union[float, int, str],
        namp: Union[float, int, str],
        rtsam: Optional[Union[float, int, str]] = None,
        rtscapt: Optional[Union[float, int, str]] = None,
        rtsemnt: Optional[Union[float, int, str]] = None,
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.TR_NOISE
        )
        
        self._na = self._format_value(na)
        self._nt = self._format_value(nt)
        self._nalpha = self._format_value(nalpha)
        self._namp = self._format_value(namp)
        self._rtsam = self._format_value(rtsam)
        self._rtscapt = self._format_value(rtscapt)
        self._rtsemnt = self._format_value(rtsemnt)
        
        self._set_source_str([
            self._na, self._nt, self._nalpha, 
            self._namp, self._rtsam, 
            self._rtscapt, self._rtsemnt
        ])