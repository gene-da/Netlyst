from Netlist.Components import SpiceElement, Nodes
from typing import Optional, Union

class GLOBAL(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        nodes: list[Union[int, str]],
        doc: Optional[str] = None,
        scope: str = "global"
    ) -> None:
        super().__init__()
        self.scope = scope
        self._doc = doc if doc else None
        self.nodes = {}

        # Format and register nodes
        for element in nodes:
            node = self._format_node(element)
            self.nodes[node] = node

        if scope not in self._instances:
            self._instances[scope] = {}
        self._instances[scope].update(self.nodes)

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        base_line = ".GLOBAL " + " ".join(self.nodes.keys())
        return f"{doc_line}\n{base_line}" if doc_line else base_line

    def to_line(self) -> str:
        return ".GLOBAL " + " ".join(self.nodes.keys())