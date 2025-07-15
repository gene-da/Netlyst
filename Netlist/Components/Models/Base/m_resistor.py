from Netlist.Components import MODEL
from typing import Optional, Union

class RMOD(MODEL):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        tc1: Optional[Union[float, int, str]] = None,
        tc2: Optional[Union[float, int, str]] = None,
        rsh: Optional[Union[float, int, str]] = None,
        defw: Optional[Union[float, int, str]] = None,
        narrow: Optional[Union[float, int, str]] = None,
        short: Optional[Union[float, int, str]] = None,
        tnom: Optional[Union[float, int, str]] = None,
        kf: Optional[Union[float, int, str]] = None,
        af: Optional[Union[float, int, str]] = None,
        wf: Optional[Union[float, int, str]] = None,
        lf: Optional[Union[float, int, str]] = None,
        ef: Optional[Union[float, int, str]] = None,
        res: Optional[Union[float, int, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ):
        type = "R"
        params = []

        if tc1 is not None: params.append(f'tc1={self._format_value(tc1)}')
        if tc2 is not None: params.append(f'tc2={self._format_value(tc2)}')
        if rsh is not None: params.append(f'rsh={self._format_value(rsh)}')
        if defw is not None: params.append(f'defw={self._format_value(defw)}')
        if narrow is not None: params.append(f'narrow={self._format_value(narrow)}')
        if short is not None: params.append(f'short={self._format_value(short)}')
        if tnom is not None: params.append(f'tnom={self._format_value(tnom)}')
        if kf is not None: params.append(f'kf={self._format_value(kf)}')
        if af is not None: params.append(f'af={self._format_value(af)}')
        if wf is not None: params.append(f'wf={self._format_value(wf)}')
        if lf is not None: params.append(f'lf={self._format_value(lf)}')
        if ef is not None: params.append(f'ef={self._format_value(ef)}')
        if res is not None: params.append(f'res={self._format_value(res)}')

        mod = " ".join(params)

        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'RMOD{name:03d}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in RMOD._instances:
            RMOD._instances[scope] = {}

        if resolved_name in RMOD._instances[scope] and RMOD._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate resistor model name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        RMOD._instances[scope][resolved_name] = self

        super().__init__(self.name, type, mod, doc=doc)