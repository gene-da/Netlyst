from typing import Optional, Union
from Netlist.Components import SpiceElement, Nodes

"""
IYYYYYYY N+ N- <<DC> DC/TRAN VALUE> <AC <ACMAG <ACPHASE>>>
+ <DISTOF1 <F1MAG <F1PHASE>>> <DISTOF2 <F2MAG <F2PHASE>>>
"""

class I(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        dc: Optional[Union[float, int, str]] = None,
        ac: Optional[Union[float, int, str]] = None,
        acmag: Optional[Union[float, int, str]] = None,
        acphase: Optional[Union[float, int, str]] = None,
        distof1: Optional[str] = None,
        f1mag: Optional[Union[float, int, str]] = None,
        f1phase: Optional[Union[float, int, str]] = None,
        distof2: Optional[str] = None,
        f2mag: Optional[Union[float, int, str]] = None,
        f2phase: Optional[Union[float, int, str]] = None,
        value: Optional[Union[float, int, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        resolved_name = name if isinstance(name, str) else f'I{name}'
        if scope not in I._instances:
            I._instances[scope] = {}
        if resolved_name in I._instances[scope]:
            raise ValueError(f"Duplicate current source name in scope '{scope}': {resolved_name}")
        I._instances[scope][resolved_name] = self

        self.name = resolved_name
        self.scope = scope
        self._doc = doc

        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)

        self._dc = self._format_value(dc)
        self._ac = self._format_value(ac)
        self._acmag = self._format_value(acmag)
        self._acphase = self._format_value(acphase)
        self._distof1 = distof1
        self._f1mag = self._format_value(f1mag)
        self._f1phase = self._format_value(f1phase)
        self._distof2 = distof2
        self._f2mag = self._format_value(f2mag)
        self._f2phase = self._format_value(f2phase)
        self._value = self._format_value(value)

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}',
        ]

        if self._dc:
            parts.append(str(self._dc))
        elif self._value:
            parts.append(str(self._value))

        extras = []
        if self._ac: extras.append(f"AC={self._ac}")
        if self._acmag: extras.append(f"ACMAG={self._acmag}")
        if self._acphase: extras.append(f"ACPHASE={self._acphase}")
        if self._distof1: extras.append(f"DISTOF1={self._distof1}")
        if self._f1mag: extras.append(f"F1MAG={self._f1mag}")
        if self._f1phase: extras.append(f"F1PHASE={self._f1phase}")
        if self._distof2: extras.append(f"DISTOF2={self._distof2}")
        if self._f2mag: extras.append(f"F2MAG={self._f2mag}")
        if self._f2phase: extras.append(f"F2PHASE={self._f2phase}")

        base_line = " ".join(parts)
        if not extras:
            return f"{doc_line}\n{base_line}" if doc_line else base_line

        lines = []
        current = "+ "
        for e in extras:
            if len(current) + len(e) + 1 > 40:
                lines.append(current.strip())
                current = "+ "
            current += e + " "
        if current.strip() != "+":
            lines.append(current.strip())

        return f"{doc_line}\n{base_line}\n" + "\n".join(lines) if doc_line else f"{base_line}\n" + "\n".join(lines)

    def to_line(self) -> str:
        parts = [
            self.name,
            self.nodes["n+"],
            self.nodes["n-"],
        ]
        if self._dc:
            parts.append(str(self._dc))
        elif self._value:
            parts.append(str(self._value))

        extras = []
        if self._ac: extras.append(f"AC={self._ac}")
        if self._acmag: extras.append(f"ACMAG={self._acmag}")
        if self._acphase: extras.append(f"ACPHASE={self._acphase}")
        if self._distof1: extras.append(f"DISTOF1={self._distof1}")
        if self._f1mag: extras.append(f"F1MAG={self._f1mag}")
        if self._f1phase: extras.append(f"F1PHASE={self._f1phase}")
        if self._distof2: extras.append(f"DISTOF2={self._distof2}")
        if self._f2mag: extras.append(f"F2MAG={self._f2mag}")
        if self._f2phase: extras.append(f"F2PHASE={self._f2phase}")

        return " ".join(parts + extras)