from typing import Optional
from ..Base.spice_element import SpiceElement

class MODEL(SpiceElement):
    def __init__(
        self,
        name: str,
        mtype: str,
        model: str,
        doc: Optional[str] = None,
        scope: str = 'global',
    ) -> None:
        super().__init__(
            comp_prefix=None,
            name=name,
            doc=doc,
            scope=scope,
        )

        self.type = mtype
        self.model = model
        self.mname = name
        
    def to_string(self) -> str:
        lines = []
        
        if self._doc:
            lines.extend(self._format_doc_block())

        header = f'{".model":<8} {self.mname:<8} {self.type:<8}'
        lines.append(header)

        lines.append(self._wrap_continuation_line(self.model))
        return "\n".join(lines)
    
    def _include(self) -> tuple[str, ...]:
        return ('',)

    def to_line(self) -> str:
        return f'.model {self.mname} {self.type} ({self.model})'