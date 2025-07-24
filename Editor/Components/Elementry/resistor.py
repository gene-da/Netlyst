from ..Base import *
from ..Directives.model import MODEL
from ..Directives.Analysis import HasTemp

from typing import Union, Optional, List, Tuple

class R(SpiceElement, Nodes, HasTemp):
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
        
        self.id.etype = SpiceElementType.DEVICE
    
    @property
    def value(self) -> Optional[Union[float, int, str]]:
        return self._value
    @value.setter
    def value(self, value: Optional[Union[float, int, str]]) -> None:
        self._value = self._format_value(value)
        
    @property
    def ac(self) -> Optional[Union[float, int, str]]:
        return self._ac
    @ac.setter
    def ac(self, value: Optional[Union[float, int, str]]) -> None:
        self._ac = self._format_value(value)
        
    @property
    def m(self) -> Optional[Union[float, int, str]]:
        return self._m
    @m.setter
    def m(self, value: Optional[Union[float, int, str]]) -> None:
        self._m = self._format_value(value)
        
    @property
    def scale(self) -> Optional[Union[float, int, str]]:
        return self._scale
    @scale.setter
    def scale(self, value: Optional[Union[float, int, str]]) -> None:
        self._scale = self._format_value(value)
        
    @property
    def temp(self) -> Optional[Union[float, int, str]]:
        return self._temp
    @temp.setter
    def temp(self, value: Optional[Union[float, int, str]]) -> None:
        self._temp = self._format_value(value)
        
    @property
    def dtemp(self) -> Optional[Union[float, int, str]]:
        return self._dtemp
    @dtemp.setter
    def dtemp(self, value: Optional[Union[float, int, str]]) -> None:
        self._dtemp = self._format_value(value)
        
    @property
    def expression(self) -> Optional[str]:
        return self._expression
    @expression.setter
    def expression(self, value: Optional[str]) -> None:
        self._expression = value
        
    @property
    def tc1(self) -> Optional[Union[float, int, str]]:
        return self._tc1
    @tc1.setter
    def tc1(self, value: Optional[Union[float, int, str]]) -> None:
        self._tc1 = self._format_value(value)

    @property
    def tc2(self) -> Optional[Union[float, int, str]]:
        return self._tc2
    @tc2.setter
    def tc2(self, value: Optional[Union[float, int, str]]) -> None:
        self._tc2 = self._format_value(value)

    @property
    def noisy(self) -> Optional[float]:
        return self._noisy
    @noisy.setter
    def noisy(self, value: Optional[float]) -> None:
        self._noisy = self._validate_noisy(value)
        
    @property
    def mname(self) -> Optional[str]:
        return self._mname
    @mname.setter
    def mname(self, value: Optional[str]) -> None:
        self._mname = value
        
    @property
    def l(self) -> Optional[Union[float, int, str]]:
        return self._l
    @l.setter
    def l(self, value: Optional[Union[float, int, str]]) -> None:
        self._l = self._format_value(value)

    @property
    def w(self) -> Optional[Union[float, int, str]]:
        return self._w
    @w.setter
    def w(self, value: Optional[Union[float, int, str]]) -> None:
        self._w = self._format_value(value)

    def _include(self) -> Tuple[str, ...]:
        if self._expression:
            return ('expression', 'tc1', 'tc2', 'noisy')
        
        elif self._mname:
            return ('l', 'w', 'temp', 'dtemp', 'm', 'ac', 'scale', 'noisy')
            
        elif self._mname is None:
            return ('ac', 'm', 'scale', 'temp', 'dtemp', 'noisy', 'tc1', 'tc2')

