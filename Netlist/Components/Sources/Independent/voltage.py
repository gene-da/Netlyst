from typing import Optional, Union
from Netlist.Components import SpiceElement, Nodes
from .source_analysis import DCT, ACA, DISTOF
from .signals import Signal

"""
VXXXXXXX N+ N- <<DC> DC/TRAN VALUE> <AC <ACMAG <ACPHASE>>>
+ <DISTOF1 <F1MAG <F1PHASE>>> <DISTOF2 <F2MAG <F2PHASE>>>
""" 

class V(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        dc: Optional[DCT] = None,
        ac: Optional[ACA] = None,
        distof1: Optional[DISTOF] = None,
        distof2: Optional[DISTOF] = None,
        signal: Optional[Signal] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'V{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in V._instances:
            V._instances[scope] = {}
        if resolved_name in V._instances[scope] and V._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate voltage source name in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        V._instances[scope][resolved_name] = self

        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)

        self._dc = dc
        self._ac = ac
        self._distof1 = distof1
        self._distof2 = distof2
        self._signal = signal
        self._doc = doc

    # --- Properties ---
    @property
    def dc(self) -> Optional[DCT]: 
        return self._dc
    @dc.setter
    def dc(self, dc: Optional[DCT]) -> None: 
        self._dc = dc

    @property
    def ac(self) -> Optional[ACA]: 
        return self._ac
    @ac.setter
    def ac(self, ac: Optional[ACA]) -> None: 
        self._ac = ac

    @property
    def distof1(self) -> Optional[DISTOF]: 
        return self._distof1
    @distof1.setter
    def distof1(self, distof1: Optional[DISTOF]) -> None: 
        self._distof1 = distof1

    @property
    def distof2(self) -> Optional[DISTOF]: 
        return self._distof2
    @distof2.setter
    def distof2(self, distof2: Optional[DISTOF]) -> None: 
        self._distof2 = distof2

    @property
    def signal(self) -> Optional[Signal]: 
        return self._signal
    @signal.setter
    def signal(self, signal: Optional[Signal]) -> None: 
        self._signal = signal

    # --- Output ---
    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}'
        ]

        if self.dc: parts.append(f'{str(self.dc):<8}')
        if self.ac: parts.append(f'{str(self.ac):<8}')
        if self.distof1: parts.append(f'{str(self.distof1):<8}')
        if self.distof2: parts.append(f'{str(self.distof2):<8}')
        if self.signal: parts.append(f'{str(self.signal):<8}')

        line = " ".join(parts)
        return f"{doc_line}\n{line}" if doc_line else line

    def to_line(self) -> str:
        parts = [
            f'{self.name}',
            f'{self.nodes["n+"]}',
            f'{self.nodes["n-"]}'
        ]

        extras = []
        if self.dc: extras.append(str(self.dc))
        if self.ac: extras.append(str(self.ac))
        if self.distof1: extras.append(str(self.distof1))
        if self.distof2: extras.append(str(self.distof2))
        if self.signal: extras.append(str(self.signal))

        return " ".join(parts + extras)