from typing import Optional, Union
from Netlist.Components import SpiceElement, Nodes, MODEL

"""
Standard Inductor
LYYYYYYY n+ n- <value> <mname> <nt=val> <m=val>
+ <scale=val> <temp=val> <dtemp=val> <tc1=val>
+ <tc2=val> <ic=init_condition>
"""

from typing import Optional, Union
from Netlist.Classes.Base import *

class L(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        value: Optional[Union[float, int, str]] = None,
        mname: Optional[MODEL] = None,
        nt: Optional[Union[float, int, str]] = None,
        m: Optional[Union[float, int, str]] = None,
        scale: Optional[Union[float, int, str]] = None,
        temp: Optional[Union[float, int, str]] = None,
        dtemp: Optional[Union[float, int, str]] = None,
        tc1: Optional[Union[float, int, str]] = None,
        tc2: Optional[Union[float, int, str]] = None,
        ic: Optional[Union[float, int, str]] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'L{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in L._instances:
            L._instances[scope] = {}
        if resolved_name in L._instances[scope] and L._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate inductor name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        L._instances[scope][resolved_name] = self

        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)

        self._value = self._format_value(value)
        self._mname = mname.name if mname else None
        self._nt = self._format_value(nt)
        self._m = self._format_value(m)
        self._scale = self._format_value(scale)
        self._temp = self._format_value(temp)
        self._dtemp = self._format_value(dtemp)
        self._tc1 = self._format_value(tc1)
        self._tc2 = self._format_value(tc2)
        self._ic = self._format_value(ic)

        self._doc = doc if doc else None

    # --- Properties ---
    @property
    def value(self): return self._value
    @value.setter
    def value(self, val): self._value = self._format_value(val)

    @property
    def mname(self): return self._mname
    @mname.setter
    def mname(self, model): self._mname = model.name if model else None

    @property
    def nt(self): return self._nt
    @nt.setter
    def nt(self, val): self._nt = self._format_value(val)

    @property
    def m(self): return self._m
    @m.setter
    def m(self, val): self._m = self._format_value(val)

    @property
    def scale(self): return self._scale
    @scale.setter
    def scale(self, val): self._scale = self._format_value(val)

    @property
    def temp(self): return self._temp
    @temp.setter
    def temp(self, val): self._temp = self._format_value(val)

    @property
    def dtemp(self): return self._dtemp
    @dtemp.setter
    def dtemp(self, val): self._dtemp = self._format_value(val)

    @property
    def tc1(self): return self._tc1
    @tc1.setter
    def tc1(self, val): self._tc1 = self._format_value(val)

    @property
    def tc2(self): return self._tc2
    @tc2.setter
    def tc2(self, val): self._tc2 = self._format_value(val)

    @property
    def ic(self): return self._ic
    @ic.setter
    def ic(self, val): self._ic = self._format_value(val)

    # --- Output ---
    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}',
            f'{self.value:<8}',
        ]

        if self.mname:
            parts.append(f'{self.mname:<8}')

        optional_fields = []
        if self.mname is None:
            optional_fields = [
                ("nt", self.nt), ("m", self.m), ("scale", self.scale),
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("tc1", self.tc1), ("tc2", self.tc2),
                ("ic", self.ic)
            ]
        else:
            optional_fields = [
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("m", self.m), ("scale", self.scale),
                ("ic", self.ic)
            ]

        extras = [f"{key}={val}" for key, val in optional_fields if val is not None]
        base_line = " ".join(parts)

        if not extras:
            return f"{doc_line}\n{base_line}" if doc_line else base_line

        lines = []
        current_line = "+ "
        for field in extras:
            if len(current_line) + len(field) + 1 > 40:
                lines.append(current_line.rstrip())
                current_line = "+ "
            current_line += field + " "
        if current_line.strip() != "+":
            lines.append(current_line.rstrip())

        netlist_block = f"{base_line}\n" + "\n".join(lines)
        return f"{doc_line}\n{netlist_block}" if doc_line else netlist_block

    def to_line(self) -> str:
        parts = [
            f'{self.name}',
            f'{self.nodes["n+"]}',
            f'{self.nodes["n-"]}',
            f'{self.value}',
        ]

        if self.mname:
            parts.append(f'{self.mname}')

        if self.mname is None:
            optional_fields = [
                ("nt", self.nt), ("m", self.m), ("scale", self.scale),
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("tc1", self.tc1), ("tc2", self.tc2),
                ("ic", self.ic)
            ]
        else:
            optional_fields = [
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("m", self.m), ("scale", self.scale),
                ("ic", self.ic)
            ]

        extras = [f"{key}={val}" for key, val in optional_fields if val is not None]

        return " ".join(parts + extras)