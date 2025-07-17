from Netlist.Components import SpiceElement
from typing import Optional, Union, Tuple, List
from Netlist.Components.Directives.start_end_line import COMMENT

class Parameter:
    def __init__(self, ident:str, expr: str) -> None:
        self.ident = ident
        self.expr = expr
        
    def to_string(self) -> str:
        return f"{self.ident}={self.expr}"
    
    def __str__(self):
        return self.to_string()
    

class PARAM(SpiceElement):
    def __init__(
        self,
        param_list: List[Parameter],
        doc: Optional[str] = None,
        scope: str = "global"
    ) -> None:
        SpiceElement.__init__(self)
        
        self.scope = scope
        self.param_list = param_list
        self._doc = doc if doc else None

    def to_string(self) -> str:
        lines = []
        
        if self._doc:
            lines.append(f'{COMMENT(self._doc)}')
            lines.append(f'.param')
            
            for p in self.param_list:
                lines[1] += f' {p}'

            return '\n'.join(lines)
                
        else:
            lines.append(f'.param')
            for p in self.param_list:
                lines.append(f' {p}')
            return ' '.join(lines)

    def to_line(self) -> str:
        param_lines = " ".join([f"{name}={value}" for name, value in self.param_list])
        return f".param {param_lines}"
    
class CSPARAM(SpiceElement):
    def __init__(
        self,
        param: Parameter,
        doc: Optional[str] = None,
        scope: str = "global"
    ) -> None:
        SpiceElement.__init__(self)
        
        self.scope = scope
        self.param = param
        self._doc = doc if doc else None

    def to_string(self) -> str:
        lines = []
        
        if self._doc:
            lines.append(f'{COMMENT(self._doc)}')
            lines.append(f'.csparam {self.param}')
            return '\n'.join(lines)
                
        else:
            lines.append(f'csparam')
            lines.append(f'.csparam {self.param}')
            return ' '.join(lines)

    def to_line(self) -> str:
        return f".csparam {self.param}"