from typing import Optional, Union, List, Tuple
from textwrap import wrap

from Utilities.Converter import Conversion

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
        
        # self.comp_title = comp_title or self.__class__.__name__.upper()
        self.name = name if name is not None else self.__class__.__name__.lower()
        
        self._scope = scope
        
        if comp_prefix and name is not None:
            if isinstance(name, str):
                self.name = name if name.startswith(comp_prefix) else f"{comp_prefix}{name}"
            elif isinstance(name, int):
                self.name = f"{comp_prefix}{name}"
            else:
                raise TypeError(f"Invalid type for name: {type(name)}")

            if scope not in SpiceElement._instances:
                SpiceElement._instances[scope] = {}
            if self.name in SpiceElement._instances[scope] and SpiceElement._instances[scope][self.name] is not self:
                raise ValueError(f"Duplicate {self.__class__.__name__.upper()} name in scope '{scope}': '{self.name}'")

            SpiceElement._instances[scope][self.name] = self
            
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
    
    def _format_doc_block(self) -> list[str]:
        block = []
        if self._doc:
            block.extend(self._wrap_lines(self._doc))
        return block
    
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
    
    def _build_header(self, include: Tuple[str, ...]) -> List[str]:
        header: List[str] = []
        for key, value in vars(self).items():
            param = key.lstrip('_')
            if param in include and value is not None:
                if param == 'nodes':
                    for node_key, node_value in value.items():
                        header.append(f"{node_value}")
                else:
                    header.append(f'{value}')
                    
        return header
        
    def _build_body(self, include: Tuple[str, ...]) -> List[str]:
        items: List[str] = []
        for key, value in vars(self).items():
            param = key.lstrip('_')
            if param in include and value is not None:
                items.append(f'{param}={value}')
        return items
    
    def _validate_noisy(self, val) -> Optional[int]:
        if val is None:
            return None
        if val not in (0, 1):
            raise ValueError(f"Resistor Error - Invalid NOISY value: {val}")
        return val
    
    @property
    def key(self) -> str:
        """Returns a key that can be used in circuit dictionaries."""
        if self._scope == 'global':
            return self.name
        return f"{self.name}.{self._scope}"

    @classmethod
    def parse_key(cls, key: str) -> tuple[str, str]:
        """
        Parses a dictionary-style key like 'R1' or 'R1.sub' into (name, scope).
        Defaults to 'global' scope if not specified.
        """
        if '.' in key:
            name, scope = key.split('.', 1)
        else:
            name, scope = key, 'global'
        return name, scope

    def _include(self) -> Tuple[str, ...]:
        """Defines which attributes to include in the body."""
        raise NotImplementedError(f'[{self.__class__.__name__.upper()}] Subclasses must implement `_include()` method.')
    
    def to_line(self):
        line: List[str] = []
        header_vals = ('name', 'value', 'mname', 'nodes')
        line.extend(self._build_header(include=header_vals))
        line.extend(self._build_body(include=self._include()))
        
        return ' '.join(line)

    def to_string(self) -> str:
        doc = '\n'.join(self._format_doc_block())
        header_vals = ('name', 'value', 'mname', 'nodes')
        header = ' '.join(f'{line:<8}' for line in self._build_header(include=header_vals))
        
        body = self._build_body(include=self._include())
        body = self._wrap_continuation_line(' '.join(body))
        
        output = []
        if doc:
            output.append(doc)
        
        output.append(header)
        
        if body:
            output.append(body)

        return '\n'.join(output)
    
    def __str__(self) -> str:
        """String representation of the SpiceElement.

        Returns:
            str: The string representation of the SpiceElement defualted to the output of `to_string()` method.
        """
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}-{self._scope}-{self.name}]"
