from typing import Optional, Union
from Netlist.Classes.Base import *
from Netlist.Classes.switches_model import*# Adjust to your actual path

class S(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        ctrl_p: Union[int, str],
        ctrl_n: Union[int, str],
        mname: Optional[SW] = None,
        state: Optional[str] = None,  # "ON" or "OFF"
        scope: str = "global",
        doc: Optional[str] = None
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        # Name resolution
        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'S{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        # Instance registration
        if scope not in S._instances:
            S._instances[scope] = {}
        if resolved_name in S._instances[scope] and S._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate switch name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        S._instances[scope][resolved_name] = self

        # Nodes
        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)
        self.nodes["ctrl+"] = self._format_node(ctrl_p)
        self.nodes["ctrl-"] = self._format_node(ctrl_n)

        # Params
        self._mname = mname.name if mname else None
        self._state = state.upper() if state else None
        self._doc = doc if doc else None

    # --- Properties ---
    @property
    def mname(self): return self._mname
    @mname.setter
    def mname(self, model): self._mname = model.name if model else None

    @property
    def state(self): return self._state
    @state.setter
    def state(self, val):
        val = val.upper()
        if val not in ("ON", "OFF"):
            raise ValueError("Switch state must be 'ON' or 'OFF'")
        self._state = val

    # --- Output ---
    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}',
            f'{self.nodes["ctrl+"]:<8}',
            f'{self.nodes["ctrl-"]:<8}',
            f'{self._mname:<8}',
        ]
        if self._state:
            parts.append(f'{self._state:<8}')

        line = " ".join(parts).rstrip()
        return f"{doc_line}\n{line}" if doc_line else line

    def to_line(self) -> str:
        parts = [
            f'{self.name}',
            f'{self.nodes["n+"]}',
            f'{self.nodes["n-"]}',
            f'{self.nodes["ctrl+"]}',
            f'{self.nodes["ctrl-"]}',
            f'{self._mname}'
        ]
        if self._state:
            parts.append(self._state)
        return " ".join(parts)
    
class W(SpiceElement, Nodes):
    _instances = {}

    def __init__(
        self,
        name: Union[int, str],
        node_p: Union[int, str],
        node_n: Union[int, str],
        ctrl_vname: str,  # controlling voltage source name
        mname: Optional[CSW] = None,
        state: Optional[str] = None,
        scope: str = "global",
        doc: Optional[str] = None
    ) -> None:
        SpiceElement.__init__(self)
        Nodes.__init__(self)

        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'W{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")

        if scope not in W._instances:
            W._instances[scope] = {}
        if resolved_name in W._instances[scope] and W._instances[scope][resolved_name] is not self:
            raise ValueError(f"Duplicate switch name detected in scope '{scope}': '{resolved_name}'")

        self.name = resolved_name
        self.scope = scope
        W._instances[scope][resolved_name] = self

        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)

        self._vname = ctrl_vname
        self._mname = mname.name if mname else None
        self._state = state.upper() if state else None
        self._doc = doc if doc else None

    # --- Properties ---
    @property
    def mname(self): return self._mname
    @mname.setter
    def mname(self, model): self._mname = model.name if model else None

    @property
    def vname(self): return self._vname
    @vname.setter
    def vname(self, val): self._vname = str(val)

    @property
    def state(self): return self._state
    @state.setter
    def state(self, val):
        val = val.upper()
        if val not in ("ON", "OFF"):
            raise ValueError("Switch state must be 'ON' or 'OFF'")
        self._state = val

    # --- Output ---
    def to_string(self) -> str:
        doc_line = f"* {self._doc}" if self._doc else ""
        parts = [
            f'{self.name:<8}',
            f'{self.nodes["n+"]:<8}',
            f'{self.nodes["n-"]:<8}',
            f'{self._vname:<8}',
            f'{self._mname:<8}',
        ]
        if self._state:
            parts.append(f'{self._state:<8}')

        line = " ".join(parts).rstrip()
        return f"{doc_line}\n{line}" if doc_line else line

    def to_line(self) -> str:
        parts = [
            f'{self.name}',
            f'{self.nodes["n+"]}',
            f'{self.nodes["n-"]}',
            f'{self._vname}',
            f'{self._mname}'
        ]
        if self._state:
            parts.append(self._state)
        return " ".join(parts)