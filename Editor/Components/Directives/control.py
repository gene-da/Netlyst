from ..Base import *
from typing import List, Optional

class CONTROL(SpiceElement):
    def __init__(
        self,
        controls: List[str],
        doc: Optional[str] = None,
    ) -> None:
        super().__init__(
            comp_prefix='control',
            name='control',
            doc=doc,
        )
        self._controls = controls

    @property
    def controls(self) -> List[str]:
        return self._controls
    @controls.setter
    def controls(self, value: List[str]) -> None:
        self._controls = value

    def to_string(self) -> str:
        doc = ' '.join(self._format_doc_block())
        if doc:
            return f'{doc}\n.control {self._controls}'
        lines = [f'.control']
        lines.extend(self._controls)
        lines.append('.endc')
        
        return f'{doc}\n{'\n'.join(lines)}'

    def to_line(self) -> str:
        lines = [f'.control']
        lines.extend(self._controls)
        lines.append('.endc')
        return '\n'.join(lines)
