from Netlist.Components import SpiceElement
from typing import Optional, Union, Tuple, List

class PARAM(SpiceElement):
    def __init__(
        self,
        param_list: List[Tuple[str, Union[str, float]]],
        doc: Optional[str] = None,
        scope: str = "global"
    ) -> None:
        SpiceElement.__init__(self)
        
        self.scope = scope
        self.param_list = param_list
        self.__doc = doc if doc else None

    def to_string(self) -> str:
        doc_line = f"* {self.__doc}\n" if self.__doc else ""
        scope_prefix = f".param" if self.scope == "global" else "+param"
        param_lines = " ".join([f"{name}={value}" for name, value in self.param_list])
        return f"{doc_line}{scope_prefix} {param_lines}"

    def to_line(self) -> str:
        param_lines = " ".join([f"{name}={value}" for name, value in self.param_list])
        return f".param {param_lines}"
    
class CSPARAM(SpiceElement):
    def __init__(
        self,
        param_list: List[Tuple[str, Union[str, float]]],
        doc: Optional[str] = None,
        scope: str = "global"
    ) -> None:
        SpiceElement.__init__(self)
        
        self.scope = scope
        self.param_list = param_list
        self.__doc = doc if doc else None

    def to_string(self) -> str:
        doc_line = f"* {self.__doc}\n" if self.__doc else ""
        scope_prefix = f".csparam" if self.scope == "global" else "+param"
        param_lines = " ".join([f"{name}={value}" for name, value in self.param_list])
        return f"{doc_line}{scope_prefix} {param_lines}"

    def to_line(self) -> str:
        param_lines = " ".join([f"{name}={value}" for name, value in self.param_list])
        return f".csparam {param_lines}"