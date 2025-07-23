from typing import Union, Optional
from Netlist.Components.Base.SpiceElement import SpiceElement, Nodes
from Netlist.Components.Sources.Independent.voltage import V

"""
4.2.1 Gxxxx: Linear Voltage-Controlled Current Sources (VCCS)
General form:
    GXXXXXXX N+ N- NC+ NC- VALUE <m=val>
Examples:
    G1 2 0 5 0 0.1
n+ and n- are the positive and negative nodes, respectively. Current flow is from the positive
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
        m: Optional[Union[int, float, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None,
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name if name.startswith("G") else f"G{name}"
        elif isinstance(name, int):
            resolved_name = f"G{name}"
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in G._instances:
            G._instances[scope] = {}
        if resolved_name in G._instances[scope] and G._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate VCCS name in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        G._instances[scope][resolved_name] = self

        self.nodes["n+"]   = self._format_node(node_p)
        self.nodes["n-"]   = self._format_node(node_n)
        self.nodes["nc+"]  = self._format_node(node_cp)
        self.nodes["nc-"]  = self._format_node(node_cn)

        self.value = value
        self.m = m
        self._doc = doc

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
        
    @property
    def m(self) -> Optional[Union[int, float, str]]:
        return self._m
    @m.setter
    def m(self, val: Optional[Union[int, float, str]]) -> None:
        self._m = val

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
        if self.m is not None:
            parts.append(f"m={self._format_value(self.m)}")
            
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

"""
4.2.2 Exxxx: Linear Voltage-Controlled Voltage Sources (VCVS)
General form:
    EXXXXXXX N+ N- NC+ NC- VALUE
Examples:
    E1 2 3 14 1 2.0
n+ is the positive node, and n- is the negative node. nc+ and nc- are the positive and negative controlling nodes, respectively. value is the voltage gain. Instance parameters are listed in chapt. 27.3.7.
"""

class E(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name:       Union[int, float, str],
        node_p:     Union[int, str],
        node_n:     Union[int, str],
        node_cp:    Union[int, str],
        node_cn:    Union[int, str],
        value:      Union[int, float, str],
        scope:      str = "global",
        doc:        Optional[str] = None,
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name if name.startswith("E") else f"E{name}"
        elif isinstance(name, int):
            resolved_name = f"E{name}"
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in E._instances:
            E._instances[scope] = {}
        if resolved_name in E._instances[scope] and E._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate VCCS name in scope '{scope}': '{resolved_name}'")

        self.name           = resolved_name
        self.scope          = scope
        E._instances[scope][resolved_name] = self

        self.nodes["n+"]    = self._format_node(node_p)
        self.nodes["n-"]    = self._format_node(node_n)
        self.nodes["nc+"]   = self._format_node(node_cp)
        self.nodes["nc-"]   = self._format_node(node_cn)

        self._value         = value
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
        
"""
4.2.3 Fxxxx: Linear Current-Controlled Current Sources (CCCS)
General form:
    FXXXXXXX N+ N- VNAM VALUE <m=val>
Examples:
    F1 13 5 VSENS 5 m=2
n+ and n- are the positive and negative nodes, respectively. Current ﬂow is from the positive
node, through the source, to the negative node. vnam is the name of a voltage source through
which the controlling current ﬂows. The direction of positive controlling current ﬂow is from
the positive node, through the source, to the negative node of vnam. value is the current gain.
m is an optional multiplier to the output current. Instance parameters are listed in chapt. 27.3.4.
"""

class F(SpiceElement, Nodes):
    """
    Current-Controlled Current Source (CCCS)

    FXXXXXXX N+ N- VNAM VALUE <m=val>

    n+ and n- are output terminals. VNAM is the name of a voltage source
    through which the controlling current flows. VALUE is the gain (unitless).
    """
    _instances = {}

    def __init__(
        self,
        name: Union[int, float, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        vnam: Union[str, V],
        value: Union[int, float, str],
        m: Optional[Union[int, float, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None,
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name if name.startswith("F") else f"F{name}"
        elif isinstance(name, int):
            resolved_name = f"F{name}"
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in F._instances:
            F._instances[scope] = {}
        if resolved_name in F._instances[scope] and F._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate CCCS name in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        F._instances[scope][resolved_name] = self

        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)
        self.vnam = vnam.name if isinstance(vnam, V) else str(vnam)

        self.value = value
        self.m = m
        self._doc = doc

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

    @property
    def m(self) -> Optional[Union[int, float, str]]:
        return self._m

    @m.setter
    def m(self, val: Optional[Union[int, float, str]]) -> None:
        self._m = val

    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}',
            f'{self.vnam:<8}',
            f'{self._format_value(self.value):<8}'
        ]
        if self.m is not None:
            parts.append(f"m={self._format_value(self.m)}")

        line = " ".join(parts)
        return f"{doc_line}\n{line}" if doc_line else line

    def to_line(self) -> str:
        parts = [
            self.name,
            self.nodes["n+"],
            self.nodes["n-"],
            self.vnam,
            str(self._format_value(self.value))
        ]
        if self.m is not None:
            parts.append(f"m={self._format_value(self.m)}")
        return " ".join(parts)

"""
Hxxxx: Linear Current-Controlled Voltage Sources (CCVS)
General form:
    HXXXXXXX N+ N- VNAM VALUE
Examples:
    HX 5 17 VZ 0.5K
n+ and n- are the positive and negative nodes, respectively. vnam is the name of a voltage source
through which the controlling current ﬂows. The direction of positive controlling current ﬂow
is from the positive node, through the source, to the negative node of vnam. value is the
transresistance (in ohms). Instance parameters are listed in chapt. 27.3.5.
"""

class H(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name: Union[int, float, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        vnam: Union[str, V],
        value: Union[int, float, str],
        scope: str = "global",
        doc: Optional[str] = None,
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name if name.startswith("H") else f"H{name}"
        elif isinstance(name, int):
            resolved_name = f"H{name}"
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in H._instances:
            H._instances[scope] = {}
        if resolved_name in H._instances[scope] and H._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate CCCS name in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        H._instances[scope][resolved_name] = self

        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)
        self.vnam = vnam.name if isinstance(vnam, V) else str(vnam)

        self.value = value
        self._doc = doc

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
            f'{self.vnam:<8}',
            f'{self._format_value(self.value):<8}'
        ]

        line = " ".join(parts)
        return f"{doc_line}\n{line}" if doc_line else line

    def to_line(self) -> str:
        parts = [
            self.name,
            self.nodes["n+"],
            self.nodes["n-"],
            self.vnam,
            str(self._format_value(self.value))
        ]
        return " ".join(parts)