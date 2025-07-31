from ..source import *
from typing import Optional, Union

class EXTERNAL(IndependentSource):
    def __init__(self, source_str: str) -> None:
        IndependentSource.__init__(
            self,
            SourceType.EXTERNAL
        )
        self._source_str = source_str

        self._set_source_str([self._source_str])
