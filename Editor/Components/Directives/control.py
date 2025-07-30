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
        
        self.id.etype = SpiceElementType.CONTROL

    @property
    def controls(self) -> List[str]:
        return self._controls
    @controls.setter
    def controls(self, value: List[str]) -> None:
        self._controls = value

    def to_string(self) -> str:
        if self._doc:
            return f'{"\n".join(self._wrap_lines(self._doc))}\n{self.to_line()}'
        else:
            return f'.control {self.to_line()}'

    def to_line(self) -> str:
        lines = [f'.control']
        for line in self._controls:
            lines.append(f'    {line}')
        lines.append('.endc')
        return '\n'.join(lines)
