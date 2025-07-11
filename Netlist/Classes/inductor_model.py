from Netlist.Classes.Base.Model import *
from typing import Optional, Union

class LMOD(MODEL):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        ind: Optional[Union[float, int, str]] = None,
        csect: Optional[Union[float, int, str]] = None,
        dia: Optional[Union[float, int, str]] = None,
        length: Optional[Union[float, int, str]] = None,
        tc1: Optional[Union[float, int, str]] = None,
        tc2: Optional[Union[float, int, str]] = None,
        tnom: Optional[Union[float, int, str]] = None,
        nt: Optional[Union[float, int, str]] = None,
        mu: Optional[Union[float, int, str]] = None,
        scope: str = "global"
    ):
        type = "L"

        params = []
        if ind is not None:    params.append(f'ind={self._format_value(ind)}')
        if csect is not None:  params.append(f'csect={self._format_value(csect)}')
        if dia is not None:    params.append(f'dia={self._format_value(dia)}')
        if length is not None: params.append(f'length={self._format_value(length)}')
        if tc1 is not None:    params.append(f'tc1={self._format_value(tc1)}')
        if tc2 is not None:    params.append(f'tc2={self._format_value(tc2)}')
        if tnom is not None:   params.append(f'tnom={self._format_value(tnom)}')
        if nt is not None:     params.append(f'nt={self._format_value(nt)}')
        if mu is not None:     params.append(f'mu={self._format_value(mu)}')

        mod = " ".join(params)

        # Name resolution with 3-digit zero padding
        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'LMOD{name:03d}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in LMOD._instances:
            LMOD._instances[scope] = {}
        if resolved_name in LMOD._instances[scope] and LMOD._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate inductor model name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        LMOD._instances[scope][resolved_name] = self

        super().__init__(self.name, type, mod)
