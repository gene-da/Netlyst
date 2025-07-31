"""
General form:
    BXXXXXXX n+ n- <i=expr> <v=expr> <tc1=value> <tc2=value>
+ <temp=value> <dtemp=value>
Examples:
    B1 0 1 I=cos(v(1))+sin(v(2))
    B2 0 1 V=ln(cos(log(v(1,2)^2)))-v(3)^4+v(2)^v(1)
    B3 3 4 I=17
    B4 3 4 V=exp(pi^i(vdd))
    B5 2 0 V = V(1) < {Vlow} ? {Vlow} :
    V(1) > {Vhigh} ? {Vhigh} : V(1)
"""

from ..Base import *

class B(SpiceElement, Nodes):
    def __init__(
        self,
        name: Union[str, int],
        node_p: Union[int, str],
        node_n: Union[int, str],
        i: Optional[str] = None,
        v: Optional[str] = None,
        tc1: Optional[Union[float, int, str]] = None,
        tc2: Optional[Union[float, int, str]] = None,
        scope: str = 'global',
        doc: Optional[str] = None,
    ) -> None:
        SpiceElement.__init__(
            self,
            comp_prefix='B',
            name=name,
            doc=doc,
            scope=scope,
        )
        Nodes.__init__(self, node_p=node_p, node_n=node_n)
        
        if i and v:
            raise ValueError('Cannot specify both i and v.')
        
        self._i = i if i else None
        self._v = v if v else None
        
        self._tc1 = self._format_value(tc1)
        self._tc2 = self._format_value(tc2)
        
        self.id.etype = SpiceElementType.SOURCE
        

    @property
    def i(self) -> Optional[str]:
        return self._i
    @i.setter
    def i(self, value: Optional[str]) -> None:
        if value and self._v:
            raise ValueError('Cannot specify both i and v.')
        self._i = value
    
    @property
    def v(self) -> Optional[str]:
        return self._v
    @v.setter
    def v(self, value: Optional[str]) -> None:
        if value and self._i:
            raise ValueError('Cannot specify both i and v.')
        self._v = value
        
    @header
    @property
    def _body(self) -> str:
        if self._i and self._v:
            raise ValueError('Cannot specify both i and v.')
        
        if self._i:
            return f'I={self.i}'
        
        if self._v:
            return f'V={self.v}'
        
    @header
    @property
    def _tail(self) -> Optional[str]:
        parts = []
        if self._tc1 is not None:
            parts.append(f'TC1={self._tc1}')
        if self._tc2 is not None:
            parts.append(f'TC2={self._tc2}')

        return ' '.join(parts) if parts else None
