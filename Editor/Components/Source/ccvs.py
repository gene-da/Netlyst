"""
General form:
    EXXXXXXX N+ N- NC+ NC- VALUE
Examples:
    E1 2 3 14 1 2.0
"""

from ..Base import *
from .source import *
from typing import Optional, Union

class E(SpiceElement, Nodes):
    def __init__(
        self,
        name: Union[str, int],
        node_p: Union[int, str],
        node_n: Union[int, str],
        node_c_p: Union[int, str],
        node_c_n: Union[int, str],
        value: Union[float, int, str],
        poly_nom: Optional[str] = None,
        doc: Optional[str] = None,
        scope: str = 'global',
    ) -> None:
        SpiceElement.__init__(
            self,
            comp_prefix='E',
            name=name,
            doc=doc,
            scope=scope,
        )
        Nodes.__init__(self, node_p=node_p, node_n=node_n, node_c_p=node_c_p, node_c_n=node_c_n)
        if poly_nom and value:
            raise ValueError('Cannot specify both poly_nom and value.')

        self._value = self._format_value(value)
        self._poly = poly_nom if poly_nom else None
        
        self.id.etype = SpiceElementType.SOURCE
    
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