from typing import List
from Editor.Components.Base.spice_element import SpiceElement

class Netlist:
    def __init__(
        self,
        elements: List[SpiceElement] = None,
    ) -> None:
        self.elements = {}
        
        for element in elements or []:
            self.elements[f'{element.name}.{element._scope}'] = element
            
    def add_element(self, elements: List[SpiceElement]) -> None:
        for element in elements:
            self.elements[element.name] = element
            
    def print_list(self) -> None:
        """TODO: Still might be a bug in regards to multiple components with the same name.
        """
        for element in self.elements:
            print(self.elements[element].to_string())
            
    def to_string(self) -> str:
        """Run the netlist simulation."""
        lines = []
        for element in self.elements:
            line = self.elements[element].to_line()
            if line and line.strip():
                lines.append(line)
        return "\n".join(lines)
                
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        elements = []
        for element in self.elements:
            elements.append(f"{element}: {self.elements[element].to_line()}")
        return '\n'.join(elements)