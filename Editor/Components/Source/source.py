from enum import Enum
from typing import Optional, Union, List

from Utilities.Converter import Conversion

class SourceType(Enum):
    PULSE = 'PULSE'
    SINE = 'SIN'
    EXP = 'EXP'
    PIECE_WISE = 'PWL'
    SING_FREQ_FM = 'SFFM'
    AMP_MOD = 'AM'
    TR_NOISE = 'TRNOISE'
    RAND_VOLT = 'trrandom'
    EXTERNAL = 'external'
    RF_PORT = 'portnum'
    
    def __str__(self):
        return self.value
    

class IndependentSource:
    def __init__(self, source_type: SourceType) -> None:
        self.source_type = source_type
        self.source_str: str

    def _set_source_str(self, args: List[str]) -> None:
        self.source_str = ' '.join(str(a) for a in args if a is not None)

    def to_string(self) -> str:
        if self.source_type == SourceType.EXTERNAL or self.source_type == SourceType.RF_PORT:
            return f'{self.source_type.value} {self.source_str}'
        
        if self.source_type == SourceType.RAND_VOLT:
            return f'{self.source_type.value} ({self.source_str})'
        
        return f'{self.source_type.value}({self.source_str})'
    
    def __str__(self):
        return self.to_string()
    
    def _format_value(self, val: Optional[Union[int, float, str]]) -> Optional[str]:
        if val is None:
            return None
        if isinstance(val, str):
            return Conversion.spice(val)
        return Conversion.spice(float(val))

