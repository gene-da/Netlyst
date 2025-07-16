from typing import Optional, Union
from Netlist.Components import SpiceElement, Nodes, MODEL

class R(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
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
        scope: str = "global",
        doc: Optional[str] = None
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
        if scope not in R._instances:
            R._instances[scope] = {}
        if resolved_name in R._instances[scope] and R._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate resistor name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        R._instances[scope][resolved_name] = self

        # Nodes
        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)

        # Params
        self._value = self._format_value(value)
        self._ac = self._format_value(ac)
        self._m = self._format_value(m)
        self._scale = self._format_value(scale)
        self._temp = self._format_value(temp)
        self._dtemp = self._format_value(dtemp)
        self._tc1 = self._format_value(tc1)
        self._tc2 = self._format_value(tc2)
        self._noisy = self._validate_noisy(noisy)
        self._mname = mname.name if mname else None
        self._l = self._format_value(l)
        self._w = self._format_value(w)

        self._doc = doc if doc else None
        self.scope = scope

    # --- Properties ---
    @property
    def value(self) -> Optional[str]: 
        return self._value
    @value.setter
    def value(self, val) -> None: 
        self._value = self._format_value(val)

    @property
    def ac(self) -> Optional[str]: 
        return self._ac
    @ac.setter
    def ac(self, val) -> None: 
        self._ac = self._format_value(val)

    @property
    def m(self) -> Optional[str]: 
        return self._m
    @m.setter
    def m(self, val) -> None: 
        self._m = self._format_value(val)

    @property
    def scale(self) -> Optional[str]: 
        return self._scale
    @scale.setter
    def scale(self, val) -> None: 
        self._scale = self._format_value(val)

    @property
    def temp(self) -> Optional[str]: 
        return self._temp
    @temp.setter
    def temp(self, val) -> None: 
        self._temp = self._format_value(val)

    @property
    def dtemp(self) -> Optional[str]: 
        return self._dtemp
    @dtemp.setter
    def dtemp(self, val) -> None: 
        self._dtemp = self._format_value(val)

    @property
    def tc1(self) -> Optional[str]: 
        return self._tc1
    @tc1.setter
    def tc1(self, val) -> None: 
        self._tc1 = self._format_value(val)

    @property
    def tc2(self) -> Optional[str]: 
        return self._tc2
    @tc2.setter
    def tc2(self, val) -> None: 
        self._tc2 = self._format_value(val)

    @property
    def noisy(self) -> Optional[int]: 
        return self._noisy
    @noisy.setter
    def noisy(self, val) -> None: 
        self._noisy = self._validate_noisy(val)

    @property
    def mname(self) -> Optional[str]: 
        return self._mname
    @mname.setter
    def mname(self, model) -> None: 
        self._mname = model.name if model else None

    @property
    def l(self) -> Optional[str]: 
        return self._l
    @l.setter
    def l(self, val) -> None: 
        self._l = self._format_value(val)

    @property
    def w(self) -> Optional[str]: 
        return self._w
    @w.setter
    def w(self, val) -> None: 
        self._w = self._format_value(val)

    # --- Internals ---
    def _validate_noisy(self, val) -> Optional[int]:
        if val is None:
            return None
        if val not in (0, 1):
            raise ValueError(f"Resistor Error - Invalid NOISY value: {val}")
        return val

    # --- Output ---
    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}',
            f'{self.value:<8}',
        ]

        # Add mname inline if it exists
        if self.mname:
            parts.append(f'{self.mname:<8}')

        optional_fields = []
        if self.mname is None:
            optional_fields = [
                ("ac", self.ac), ("m", self.m), ("scale", self.scale),
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("tc1", self.tc1), ("tc2", self.tc2),
                ("noisy", self.noisy)
            ]
        else:
            optional_fields = [
                ("l", self.l), ("w", self.w),
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("m", self.m), ("ac", self.ac), ("scale", self.scale),
                ("noisy", self.noisy)
            ]

        extras = [f"{key}={val}" for key, val in optional_fields if val is not None]

        base_line = " ".join(parts)

        if not extras:
            return f"{doc_line}\n{base_line}" if doc_line else base_line

        # Build continuation lines <= 40 chars
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
                ("ac", self.ac), ("m", self.m), ("scale", self.scale),
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("tc1", self.tc1), ("tc2", self.tc2),
                ("noisy", self.noisy)
            ]
        else:
            optional_fields = [
                ("l", self.l), ("w", self.w),
                ("temp", self.temp), ("dtemp", self.dtemp),
                ("m", self.m), ("ac", self.ac), ("scale", self.scale),
                ("noisy", self.noisy)
            ]

        extras = [f"{key}={val}" for key, val in optional_fields if val is not None]

        return " ".join(parts + extras)