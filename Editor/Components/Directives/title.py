from ..Base import *
from typing import Optional, Union

from datetime import datetime

class TITLE(SpiceElement):
    def __init__(
        self,
        title: str,
        doc: Optional[str] = None,
    ) -> None:
        super().__init__(
            name='title',
            doc=doc,
            scope='global',
        )
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.title = title.strip() if title else 'Untitled Circuit'
        
    def to_string(self) -> str:
        lines = []
        lines.append('*' * self._width)
        lines.append('*')
        lines.append(f"* Generated: {self.timestamp}")
        lines.append('*')
        lines.extend(self._wrap_lines(self._doc))
        lines.append('*')
        lines.append(f'.TITLE {self.title[:self._width]}')
        lines.append('*')
        lines.append('*' * self._width)
        return "\n".join(lines)
    
    def to_line(self) -> None:
        return f'.TITLE {self.title[:self._width]}'
