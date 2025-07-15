from Netlist.Components import SpiceElement, Nodes, PARAM
from typing import Optional, List, Union

class SUBCKT(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self, name: str, 
        nodes: List[Union[int, str]],
        parameters: Optional[PARAM] = None,
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
        self.parameters = parameters

        for element in nodes:
            self.nodes[self._format_node(element)] = self._format_node(element)

        self.circuit = circuit
        self._doc = doc if doc else None

    @property
    def doc(self): return self._doc
    @doc.setter
    def doc(self, val): self._doc = str(val) if val else None

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        base_line = f".SUBCKT {self.name} " + " ".join(self.nodes.values())

        if self.parameters:
            param_str = self.parameters.to_line() if hasattr(self.parameters, "to_line") else str(self.parameters)
            base_line += f" {param_str}"

        body_lines = [element.to_string() for element in self.circuit]
        end_line = ".ENDS " + self.name

        block = "\n".join([base_line] + body_lines + [end_line])
        return f"{doc_line}\n{block}" if doc_line else block

    def to_line(self) -> str:
        # Flat single-line subcircuit reference
        node_list = " ".join(self.nodes.values())
        return f"X{self.name} {node_list} {self.name}"
