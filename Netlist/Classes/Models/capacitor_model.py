from Netlist.Classes.DotCommands import MODEL
from typing import Optional, Union

class CMOD(MODEL):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        cap: Optional[Union[float, int, str]] = None,
        cj: Optional[Union[float, int, str]] = None,
        cjsw: Optional[Union[float, int, str]] = None,
        defw: Optional[Union[float, int, str]] = None,
        defl: Optional[Union[float, int, str]] = None,
        narrow: Optional[Union[float, int, str]] = None,
        short: Optional[Union[float, int, str]] = None,
        tc1: Optional[Union[float, int, str]] = None,
        tc2: Optional[Union[float, int, str]] = None,
        tnom: Optional[Union[float, int, str]] = None,
        di: Optional[Union[float, int, str]] = None,
        thick: Optional[Union[float, int, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ):
        type = "C"

        params = []
        if cap is not None:    params.append(f'cap={self._format_value(cap)}')
        if cj is not None:     params.append(f'cj={self._format_value(cj)}')
        if cjsw is not None:   params.append(f'cjsw={self._format_value(cjsw)}')
        if defw is not None:   params.append(f'defw={self._format_value(defw)}')
        if defl is not None:   params.append(f'defl={self._format_value(defl)}')
        if narrow is not None: params.append(f'narrow={self._format_value(narrow)}')
        if short is not None:  params.append(f'short={self._format_value(short)}')
        if tc1 is not None:    params.append(f'tc1={self._format_value(tc1)}')
        if tc2 is not None:    params.append(f'tc2={self._format_value(tc2)}')
        if tnom is not None:   params.append(f'tnom={self._format_value(tnom)}')
        if di is not None:     params.append(f'di={self._format_value(di)}')
        if thick is not None:  params.append(f'thick={self._format_value(thick)}')

        mod = " ".join(params)

        # Model name resolution
        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'CMOD{name:03d}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in CMOD._instances:
            CMOD._instances[scope] = {}
        if resolved_name in CMOD._instances[scope] and CMOD._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate capacitor model name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        CMOD._instances[scope][resolved_name] = self

        super().__init__(self.name, type, mod, doc=doc)