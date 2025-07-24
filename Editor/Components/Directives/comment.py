from ..Base import *
from typing import Optional, Union

class COMMENT(SpiceElement):
    _counter = 0
    def __init__(
        self,
        comment: str,
    ) -> None:
        COMMENT._counter += 1
        comment_id = f'{COMMENT._counter:03d}'
        super().__init__(
            comp_prefix='CMT',
            # comp_title='Comment',
            name=comment_id,
            doc=comment,
            scope='global',
        )
        
        self.id.etype = SpiceElementType.OTHER
        
    def to_string(self) -> str:
        lines = []
        lines.append('*' * self._width)
        lines.append('*')
        lines.extend(self._wrap_lines(self._doc))
        lines.append('*')
        lines.append('*' * self._width)
        return "\n".join(lines)
    
    def to_line(self) -> str:
        return ''