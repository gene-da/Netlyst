from ..source import *
from typing import Optional, Union

"""DC 0 AC 1 portnum n1 <z0 n2>"""

class PORNUM(IndependentSource):
    def __init__(
        self,
        n1: Union[int],
        z0: Optional[Union[float, int, str]] = None,
        n2: Optional[Union[int]] = None
    ) -> None:
        IndependentSource.__init__(
            self,
            source_type=SourceType.RF_PORT
        )
        
        self._n1 = n1
        self._z0 = z0
        self._n2 = n2
        
        self._set_source_str([
            str(self._n1),
            f'z{self._format_value(self._z0)}',
            str(self._n2) if self._n2 is not None else None
        ])