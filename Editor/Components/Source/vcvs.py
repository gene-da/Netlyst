"""
General form:
    HXXXXXXX N+ N- VNAM VALUE
Examples:
    HX 5 17 VZ 0.5K
"""

from ..Base import *
from .voltage import *
from typing import Optional, Union

class H(SpiceElement, Nodes):
    def __init__(
        self,
        name: Union[str, int],
        node_p: Union[int, str],
        node_n: Union[int, str],
        vnam: Union[V, str],
        value: Union[float, int, str],
        poly_nom: Optional[str] = None,
        doc: Optional[str] = None,
        scope: str = 'global',
    ) -> None:
        SpiceElement.__init__(
            self,
            comp_prefix='H',
            name=name,
            doc=doc,
            scope=scope,
        )
        Nodes.__init__(self, node_p=node_p, node_n=node_n)
        
        if poly_nom and value:
            raise ValueError('Cannot specify both poly_nom and value.')
        
        if isinstance(vnam, V):
            self._vnam = vnam.id.iname
        else:
            self._vnam = vnam

        self._value = self._format_value(value)
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
    def poly(self) -> Optional[str]:
        return self._poly
    @poly.setter
    def poly(self, poly: Optional[str]) -> None:
        if poly and self._value:
            raise ValueError('Cannot specify both poly_nom and value.')
        self._poly = poly