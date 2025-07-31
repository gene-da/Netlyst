from ..source import *
from typing import Optional, Union

"""TRRANDOM(TYPE TS <TD <PARAM1 <PARAM2>>>)"""

class TRRANDOM(IndependentSource):
    def __init__(
        self,
        type_: Union[str, int],
        ts: Union[float, int, str],
        td: Optional[Union[float, int, str]] = None,
        param1: Optional[Union[float, int, str]] = None,
        param2: Optional[Union[float, int, str]] = None
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.RAND_VOLT
        )
        
        self._type = type_
        self._ts = self._format_value(ts)
        
        if td == 0:
            self._td = '0'
        else:
            self._td = f'{self._format_value(td)}s'
            
        self._param1 = self._format_value(param1)
        self._param2 = self._format_value(param2)
        
        self._set_source_str([
            self._type, self._ts, self._td, 
            self._param1, self._param2
        ])