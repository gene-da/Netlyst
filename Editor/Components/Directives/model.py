from typing import Optional
from ..Base import *

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

        self._type = mtype
        self._model = model
        self._name = name

        self.id.etype = SpiceElementType.MODEL
        
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        
    @property
    def type(self) -> str:
        return self._type
    @type.setter
    def type(self, value: str) -> None:
        self._type = value
        
    @property
    def model(self) -> str:
        return self._model
    @model.setter
    def model(self, value: str) -> None:
        self._model = value
        
    def to_string(self) -> str:
        lines = []
        
        if self._doc:
            lines.extend(self._format_doc_block())

        header = f'{".model":<8} {self._name:<8} {self._type:<8}'
        lines.append(header)

        lines.append(self._wrap_continuation_line(self._model))
        return "\n".join(lines)
    
    def _include(self) -> tuple[str, ...]:
        return ('',)

    def to_line(self) -> str:
        return f'.model {self._name} {self._type} ({self._model})'