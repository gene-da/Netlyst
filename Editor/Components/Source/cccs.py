"""
General form:
    FXXXXXXX N+ N- VNAM VALUE <m=val>
Examples:
    F1 13 5 VSENS 5 m=2
"""

from ..Base import *
from .voltage import *
from typing import Optional, Union

class F(SpiceElement, Nodes):
    def __init__(
        self,
        name: Union[str, int],
        node_p: Union[int, str],
        node_n: Union[int, str],
        vnam: Union[V, str],
        value: Union[float, int, str],
        m: Optional[Union[float, int, str]] = None,
        poly_nom: Optional[str] = None,
        doc: Optional[str] = None,
        scope: str = 'global',
    ) -> None:
        SpiceElement.__init__(
            self,
            comp_prefix='F',
            name=name,
            doc=doc,
            scope=scope,
        )
        Nodes.__init__(self, node_p=node_p, node_n=node_n)
        
        if poly_nom and value or poly_nom and m:
            raise ValueError('Cannot specify both poly_nom and value/m.')

        if isinstance(vnam, V):
            self._vnam = vnam.id.iname
        else:
            self._vnam = vnam
        
        self._value = self._format_value(value)
        self._m = self._format_value(m)
        self._poly = poly_nom if poly_nom else None
        
        self.id.etype = SpiceElementType.SOURCE
    
    @header    
    @property
    def vnam(self) -> str:
        return self._vnam
    @vnam.setter
    def vnam(self, vnam: V) -> None:
        self._vnam = vnam.id.iname
    
    @header    
    @property
    def value(self) -> Union[float, int, str]:
        return self._value
    @value.setter
    def value(self, value: Union[float, int, str]) -> None:
        self._value = self._format_value(value)
        
    @header
    @property
    def m(self) -> Optional[Union[float, int, str]]:
        return f'm={self._m}'
    @m.setter
    def m(self, value: Optional[Union[float, int, str]]) -> None:
        self._m = self._format_value(value)
        
    @header
    @property
    def poly(self) -> Optional[str]:
        return self._poly
    @poly.setter
    def poly(self, poly: Optional[str]) -> None:
        if poly and self._value or poly and self._m:
            raise ValueError('Cannot specify both poly_nom and value/m.')
        self._poly = poly
