from typing import Union, Optional, List, Tuple
from Netlist.Components.Base.SpiceElement import SpiceElement, Nodes

"""
Gxxxx: Linear Voltage-Controlled Current Sources (VCCS)
General form:
    GXXXXXXX N+ N- NC+ NC- VALUE <m=val>
Examples:
    G1 2    0 5      0 0.1
n+ and n- are the positive and negative nodes, respectively. Current ﬂow is from the positive
node, through the source, to the negative
node. nc+ and nc- are the positive and negative controlling nodes, respectively. value is the
transconductance (in mhos). m is an optional multiplier to the output current. val may be a
numerical value or an expression according to 2.11.5 containing references to other parameters.
Instance parameters are listed in chapt. 27.3.6.
"""

class G(SpiceElement, Nodes):
    """
    Voltage-Controlled Current Source (VCCS)

    GXXXXXXX N+ N- NC+ NC- VALUE <m=val>

    n+ and n- are output terminals, nc+ and nc- are control terminals.
    VALUE is the transconductance in mhos (A/V).
    """
    _instances = {}

    def __init__(
        self,
        name: Union[int, float, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        node_cp: Union[int, str],
        node_cn: Union[int, str],
        value: Union[int, float, str],
        scope: str = "global",
        doc: Optional[str] = None,
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'G{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in G._instances:
            G._instances[scope] = {}
        if resolved_name in G._instances[scope] and G._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate VCCS name in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        G._instances[scope][resolved_name] = self

        self.nodes["n+"]    = self._format_node(node_p)
        self.nodes["n-"]    = self._format_node(node_n)
        self.nodes["nc+"]   = self._format_node(node_cp)
        self.nodes["nc-"]   = self._format_node(node_cn)

        self_value          = value
        self._doc           = doc

    @property
    def value(self) -> Union[int, float, str]:
        return self._value

    @value.setter
    def value(self, val: Union[int, float, str]) -> None:
        self._value = val

    @property
    def doc(self) -> Optional[str]:
        return self._doc

    @doc.setter
    def doc(self, val: Optional[str]) -> None:
        self._doc = val

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}',
            f'{self.nodes["nc+"]:<8}',
            f'{self.nodes["nc-"]:<8}',
            f'{self._format_value(self.value):<8}'
        ]
        line = " ".join(parts)
        return f"{doc_line}\n{line}" if doc_line else line

    def to_line(self) -> str:
        return " ".join([
            self.name,
            self.nodes["n+"],
            self.nodes["n-"],
            self.nodes["nc+"],
            self.nodes["nc-"],
            str(self._format_value(self.value))
        ])