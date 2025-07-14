from typing import Optional, Union
from Netlist.Classes.Base import *

class SW(MODEL):
    _instances = {}

    def __init__(
        self,
        name: Union[str, int],
        vt: Optional[Union[float, int, str]] = None,
        vh: Optional[Union[float, int, str]] = None,
        ron: Optional[Union[float, int, str]] = None,
        roff: Optional[Union[float, int, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ):
        type = "SW"
        params = []
        if vt is not None:   params.append(f'vt={self._format_value(vt)}')
        if vh is not None:   params.append(f'vh={self._format_value(vh)}')
        if ron is not None:  params.append(f'ron={self._format_value(ron)}')
        if roff is not None: params.append(f'roff={self._format_value(roff)}')
        mod = " ".join(params)

        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'SWMOD{name:03d}'
        else:
            raise TypeError(f"Invalid model name: {type(name)}")

        if scope not in SW._instances:
            SW._instances[scope] = {}
        if resolved_name in SW._instances[scope] and SW._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate SW name in scope '{scope}': '{resolved_name}'")

        SW._instances[scope][resolved_name] = self
        self.name = resolved_name
        self.scope = scope

        super().__init__(self.name, type, mod, doc=doc)
        
class CSW(MODEL):
    _instances = {}

    def __init__(
        self,
        name: Union[str, int],
        it: Optional[Union[float, int, str]] = None,
        ih: Optional[Union[float, int, str]] = None,
        ron: Optional[Union[float, int, str]] = None,
        roff: Optional[Union[float, int, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ):
        type = "CSW"
        params = []
        if it is not None:   params.append(f'it={self._format_value(it)}')
        if ih is not None:   params.append(f'ih={self._format_value(ih)}')
        if ron is not None:  params.append(f'ron={self._format_value(ron)}')
        if roff is not None: params.append(f'roff={self._format_value(roff)}')
        mod = " ".join(params)

        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'CSWMOD{name:03d}'
        else:
            raise TypeError(f"Invalid model name: {type(name)}")

        if scope not in CSW._instances:
            CSW._instances[scope] = {}
        if resolved_name in CSW._instances[scope] and CSW._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate CSW name in scope '{scope}': '{resolved_name}'")

        CSW._instances[scope][resolved_name] = self
        self.name = resolved_name
        self.scope = scope

        super().__init__(self.name, type, mod, doc=doc)