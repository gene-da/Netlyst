from ..Base import *
from typing import List, Optional

class CSPARAM(SpiceElement):
    def __init__(
        self,
        ident: str,
        expr: str,
        doc: Optional[str] = None,
    ) -> None:
        super().__init__(
            name='csparam',
            doc=doc,
        )
        
        self._ident = ident
        self._expr = expr
        
        self.id.etype = SpiceElementType.PARAMETER
    
    @property
    def ident(self) -> str:
        return self._ident
    @ident.setter
    def ident(self, value: str) -> None:
        self._ident = value
        
    @property
    def expr(self) -> str:
        return self._expr
    @expr.setter
    def expr(self, value: str) -> None:
        self._expr = value
        
    def to_string(self) -> str:
        doc = ' '.join(self._format_doc_block())
        if doc:
            return f'{doc}\n.csparam {self._ident}={self._expr}'

    def to_line(self) -> str:
        return f'.csparam {self._ident}={self._expr}'