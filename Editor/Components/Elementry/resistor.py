from ..Base import *
from ..Directives.model import MODEL

from typing import Union, Optional, List, Tuple

class R(SpiceElement, Nodes):
    def __init__(
        self,
        name: Union[str, int],
        node_p: Union[int, str],
        node_n: Union[int, str],
        value: Optional[Union[float, int, str]] = None,
        ac: Optional[Union[float, int, str]] = None,
        m: Optional[Union[float, int, str]] = None,
        scale: Optional[Union[float, int, str]] = None,
        temp: Optional[Union[float, int, str]] = None,
        dtemp: Optional[Union[float, int, str]] = None,
        tc1: Optional[Union[float, int, str]] = None,
        tc2: Optional[Union[float, int, str]] = None,
        noisy: Optional[float] = None,
        mname: Optional[MODEL] = None,
        l: Optional[Union[float, int, str]] = None,
        w: Optional[Union[float, int, str]] = None,
        doc: Optional[str] = None,
        scope: str = 'global',
        expression: Optional[str] = None
    ) -> None:
        SpiceElement.__init__(
            self,
            comp_prefix='R',
            name=name,
            doc=doc,
            scope=scope,
        )
        Nodes.__init__(self, node_n=node_n, node_p=node_p)

        self._value = self._format_value(value)
        self._ac = self._format_value(ac)
        self._m = self._format_value(m)
        self._scale = self._format_value(scale)
        self._temp = self._format_value(temp)
        self._dtemp = self._format_value(dtemp)
        self._expression = expression
        self._tc1 = self._format_value(tc1)
        self._tc2 = self._format_value(tc2)
        self._noisy = self._validate_noisy(noisy)
        self._mname = mname.mname if mname else None
        self._l = self._format_value(l)
        self._w = self._format_value(w)

    def _include(self) -> Tuple[str, ...]:
        if self._expression:
            return ('expression', 'tc1', 'tc2', 'noisy')
        
        elif self._mname:
            return ('l', 'w', 'temp', 'dtemp', 'm', 'ac', 'scale', 'noisy')
            
        elif self._mname is None:
            return ('ac', 'm', 'scale', 'temp', 'dtemp', 'noisy', 'tc1', 'tc2')

