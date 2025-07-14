from Netlist.Classes.Base.SpiceElement import SpiceElement, Nodes
from typing import Optional, List

class SUBCKT(SpiceElement, Nodes):
    def __init__(self, name: str, nodes: Nodes, circuit: List[SpiceElement], doc: Optional[str] = None) -> None:
        self.name = name.strip()
        self.nodes = nodes
        self.circuit = circuit
        self._doc = doc.strip() if doc else None
        super().__init__()