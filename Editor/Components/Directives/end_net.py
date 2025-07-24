from ..Base import *
from typing import Optional, Union

class END(SpiceElement):
    def __init__(
        self,
        doc: Optional[str] = None,
        scope: str = 'global',
    ) -> None:
        super().__init__(
            name='end_netlist',
            doc=doc,
            scope=scope,
        )
        
        self.id.etype = SpiceElementType.STRUCTURE
        
    def to_string(self) -> str:
        lines = []
        if self._doc:
            lines.extend(self._format_doc_block())
        lines.append('.end')
        return "\n".join(lines)
    
    def to_line(self) -> str:
        return '.end'