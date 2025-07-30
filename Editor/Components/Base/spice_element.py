from typing import Optional, Union, List, Tuple, Dict
from textwrap import wrap
from dataclasses import dataclass
from enum import Enum
from .node import Nodes

from Utilities.Converter import Conversion

class SpiceElementType(Enum):
    STRUCTURE = 'structure'
    COMMAND = 'command'
    PARAMETER = 'parameter'
    ANALYSIS = 'analysis'
    CONTROL = 'control'
    MODEL = 'model'
    DEVICE = 'device'
    OTHER = 'other'
    SOURCE = 'source'
    NOT_IMPLEMENTED = 'not_implemented'
    
def body(thing):
    """Decorator to mark a method or property getter as part of the body."""
    if isinstance(thing, property):
        # If it's a property, decorate the fget instead
        if thing.fget:
            thing.fget.is_body = True
        return thing
    else:
        # If it's a function, just tag it
        thing.is_body = True
        return thing


def header(thing):
    """Decorator to mark a method or property getter as a header."""
    if isinstance(thing, property):
        if thing.fget:
            thing.fget.is_header = True
        return thing
    else:
        thing.is_header = True
        return thing

@dataclass
class ID:
    cname: str
    iname: str
    etype: SpiceElementType
    scope: str
    
    @property
    def string(self) -> str:
        return f"{self.etype.name}.{self.cname.upper()}.{self.iname.upper()}.{self.scope.upper()}"

class SpiceElement:
    _instances = {}

    def __init__(
        self,
        comp_prefix: Optional[str] = None,
        name: Optional[Union[str, int]] = None,
        doc: Optional[str] = None,
        scope: str = 'global',
        width: int = 100
    ) -> None:
        self._doc = doc
        self._width = width
        
        id_name = self._resolve_self(
            prefix=comp_prefix,
            name=name,
            scope=scope
        )
        
        self.id = ID(
            cname=self.__class__.__name__.lower(),
            iname=self._resolve_self(comp_prefix, name, scope),
            etype=SpiceElementType.NOT_IMPLEMENTED,
            scope=scope
        )

    def _resolve_self(self, prefix: Optional[str], name: Optional[Union[str, int]], scope: str) -> None:
        return_name = name if name is not None else self.__class__.__name__.lower()
        
        if prefix and name is not None:
            if isinstance(name, str):
                if name.startswith(prefix):
                    return_name = name
                else:
                    return_name = f'{prefix}{name}'
            elif isinstance(name, int):
                return_name = f'{prefix}{name}'
            else:
                raise TypeError(f"Invalid type for name in class {self.__class__.__name__}: {type(name)}")
            
            if scope not in SpiceElement._instances:
                SpiceElement._instances[scope] = {}
            
            if return_name in SpiceElement._instances[scope] and SpiceElement._instances[scope][return_name] is not self:
                raise ValueError(f"Duplicate {self.__class__.__name__.upper()} name in scope '{scope}': '{return_name}'")
            
            SpiceElement._instances[scope][return_name] = self

        return return_name

    def _wrap_lines(self, text: str) -> list[str]:
        wrapped = []
        for line in text.splitlines():
            if not line.strip():
                wrapped.append("*")
                continue
            expanded = line.replace('\t', '    ')
            indent = ' ' * (len(expanded) - len(expanded.lstrip()))
            content = expanded.lstrip()
            for l in wrap(content, width=self._width - 2):
                wrapped.append(f"* {indent}{l}")
        return wrapped
    
    def _format_value(self, val: Optional[Union[int, float, str]]) -> Optional[str]:
        if val is None:
            return None
        if isinstance(val, str):
            return Conversion.spice(val)
        return Conversion.spice(float(val))

    def _wrap_continuation_line(self, text: str, prefix: str = '+') -> str:
        lines = []
        current_line = prefix
        for token in text.split():
            if len(current_line) + len(token) + 1 > self._width:
                lines.append(current_line.rstrip())
                current_line = prefix
            current_line += f" {token}"
        if current_line.strip() != prefix:
            lines.append(current_line.rstrip())
        return '\n'.join(lines)
    
    def _validate_noisy(self, val) -> Optional[int]:
        if val is None:
            return None
        if val not in (0, 1):
            raise ValueError(f"Resistor Error - Invalid NOISY value: {val}")
        return val

    def get_properties(self, prop: str):
        result = {}
        for cls in self.__class__.__mro__:  # Walks R, Base, object
            for name, attr in cls.__dict__.items():
                if isinstance(attr, property):
                    if prop == 'body' and getattr(attr.fget, 'is_body', False):
                        result[name] = getattr(self, name)
                    elif prop == 'header' and getattr(attr.fget, 'is_header', False):
                        result[name] = getattr(self, name)
        return result
    


    def to_line(self) -> str:
        line: List[str] = []
        headers = self.get_properties('header')
        bodies = self.get_properties('body')

        line.append(f'{self.id.iname}')

        if isinstance(self, Nodes):
            for key, value in self._nodes.items():
                line.append(str(value))

        if headers:
            for key, value in headers.items():
                if value is not None:
                    line.append(str(value))

        if bodies:
            for key, value in bodies.items():
                if value is not None:
                    line.append(f'{key}={value}')

        return ' '.join(line)


    def to_string(self) -> str:
        lines: List[str] = []
        headers = self.get_properties('header')
        bodies = self.get_properties('body')

        if self._doc:
            lines.extend(self._wrap_lines(self._doc))

        header: List[str] = []
        if headers:
            header.append(f'{self.id.iname:<8}')
            if isinstance(self, Nodes):
                for key, value in self._nodes.items():
                    header.append(f'{value:<8}')
            for key, value in headers.items():
                if value is not None:
                    header.append(f'{value:<8}')
            lines.append(' '.join(header))

        if bodies:
            body_lines = [f"{key}={value}" for key, value in bodies.items() if value is not None]
            if body_lines:
                lines.append(self._wrap_continuation_line('\n'.join(body_lines)).rstrip())

        return '\n'.join(lines)


    def __str__(self) -> str:
        """String representation of the SpiceElement.

        Returns:
            str: The string representation of the SpiceElement defualted to the output of `to_string()` method.
        """
        return self.to_string()
    
    def __repr__(self) -> str:
        return self.id.string
