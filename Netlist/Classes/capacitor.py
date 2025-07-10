from typing import Optional, Union
from Netlist.Classes.Base import*

"""
CXXXXXXX n+ n- <value> <mname> <m=val> <scale=val> <temp=val>
+ <dtemp=val> <tc1=val> <tc2=val> <ic=init_condition>

CXXXXXXX n+ n- <value> <mname> <l=length> <w=width> <m=val>
+ <scale=val> <temp=val> <dtemp=val> <ic=init_condition>
"""

class R(SpiceElement, Nodes):
    def __init__(
        self,
        name: str,
        node_p: Union[int, str],
        node_n: Union[int, str],
        value: Optional[Union[float, int, str]] = None,
        ac: Optional[Union[float, int, str]] = None,
        m: Optional[Union[float, int, str]] = None,
        scale: Optional[Union[float, int, str]] = None,
        temp: Optional[Union[float, int, str]] = None,
        dtemp: Optional[Union[float, int, str]] = None,
        tc1: Optional[Union[float, int, str]] = None,
        tc2: Optional[Union[float, int, str]] = None,
        noisy: Optional[float] = None,
        mname: Optional[MODEL] = None,
        l: Optional[Union[float, int, str]] = None,
        w: Optional[Union[float, int, str]] = None,
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        self.name = name
        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)
        self.value = value
        self.ac = ac
        self.m = m
        self.scale = scale
        self.temp = temp
        self.dtemp = dtemp
        self.tc1 = tc1
        self.tc2 = tc2
        if noisy is not None:
            if noisy not in (0, 1):
                raise ValueError(f"Resistor Error - Invalid NOISY value: {noisy}")
            self.noisy = noisy
        else:
            self.noisy = None
        self.mname = mname.name if mname else None
        self.l = l
        self.w = w
        
    def to_string(self) -> str:
        parts = [
            self.name,
            self.nodes["n+"],
            self.nodes["n-"],
            self.value if self.value is not None else "0"
        ]
        
        if self.mname is None:
            """
            RXXXXXXX n+ n- <resistance|r=>value <ac=val> <m=val>
            + <scale=val> <temp=val> <dtemp=val> <tc1=val> <tc2=val>
            + <noisy=0|1> <mname> <l=length> <w=width>
            """
            optional_fields = [
                ("ac", self.ac),
                ("m", self.m),
                ("scale", self.scale),
                ("temp", self.temp),
                ("dtemp", self.dtemp),
                ("tc1", self.tc1),
                ("tc2", self.tc2),
                ("noisy", self.noisy)
            ]
        else:
            """
            RXXXXXXX n+ n- <value> <mname> <l=length> <w=width>
            + <temp=val> <dtemp=val> <m=val> <ac=val> <scale=val>
            + <noisy = 0|1>
            """
            optional_fields = [
                ("mname", self.mname),
                ("l", self.l),
                ("w", self.w),
                ("temp", self.temp),
                ("dtemp", self.dtemp),
                ('m', self.m),
                ('ac', self.ac),
                ('scale', self.scale),
                ("noisy", self.noisy)
            ]

        for key, val in optional_fields:
            if val is not None:
                parts.append(f"{key}={val}")

        return " ".join(parts)