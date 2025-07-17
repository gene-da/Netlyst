from Netlist.Components import SpiceElement, Nodes, PARAM, Parameter
from Netlist.Components.Directives.start_end_line import COMMENT
from typing import Optional, List, Union

class SUBCKT(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self, name: str, 
        nodes: List[Union[int, str]],
        params: Optional[List[Parameter]] = None,
        circuit: List[SpiceElement] = [], 
        doc: Optional[str] = None,
        scope: str = "global"
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        # Name resolution
        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'R{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        # Instance registration
        if scope not in self._instances:
            self._instances[scope] = {}
        if resolved_name in self._instances[scope] and self._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate resistor name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name

        for node in nodes:
            format_node = self._format_node(node)
            self.nodes[format_node] = format_node
            
        self.params = params if params else None

        self.circuit = circuit
        self._doc = doc if doc else None

    @property
    def doc(self): return self._doc
    @doc.setter
    def doc(self, val): self._doc = str(val) if val else None

    def to_string(self) -> str:
        lines = []
        
        if self._doc:
            lines.append(f'{COMMENT(self._doc)}')
            lines.append('*')
        
        first_line = [f'.subckt {self.name}']
        
        for node in self.nodes:
            first_line.append(f'{self.nodes[node]}')
            
        if self.params:
            for param in self.params:
                first_line.append(f'{param}')
                
        lines.append(" ".join(first_line))
        
        if self.circuit:
            for element in self.circuit:
                lines.append(str(element))
                
        lines.append(f'.ends {self.name}')
        
        return '\n'.join(lines)
    
    def to_line(self) -> str:
        # Flat single-line subcircuit reference
        node_list = " ".join(self.nodes.values())
        return f"X{self.name} {node_list} {self.name}"

class X(SpiceElement, Nodes):
    _instances = {}
    
    def __init__(
        self,
        name:                   Union[str, int],
        nodes:                  List[Union[int, str]],
        subckt:                 SUBCKT,
        params:                 Optional[List[Parameter]] = None,
        scope:                  str = "global",
        doc:                    Optional[str] = None
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)
        
        if isinstance(name, str):
            resolved_name = name if name.startswith("X") else f"X{name}"
        elif isinstance(name, int):
            resolved_name = f"X{name}"
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in X._instances:
            X._instances[scope] = {}
        if resolved_name in X._instances[scope] and X._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate VCCS name in scope '{scope}': '{resolved_name}'")
        
        for node in nodes:
            format_node = self._format_node(node)
            self.nodes[format_node] = format_node
        
        self.name            = resolved_name
        self.scope           = scope
        self.subckt          = subckt
        self.params          = params if params else None
        self._doc            = doc if doc else None

    def to_string(self) -> str:
        lines = []
        
        if self._doc:
            lines.append(f'{COMMENT(self._doc)}')
            
        first_line = [f'{self.name}']
        
        for node in self.nodes:
            first_line.append(f'{self.nodes[node]}')
        
        first_line.append(f'{self.subckt.name}')
        if self.params:
            for param in self.params:
                first_line.append(f'{param}')

        lines.append(" ".join(first_line))
        
        return '\n'.join(lines)