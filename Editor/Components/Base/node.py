from typing import Union, Optional

class Nodes:
    def __init__(self, **kwargs) -> None:
        self.nodes = {}
        for key, value in kwargs.items():
            self.nodes[key] = self._format_node(value)

    def _format_node(self, index: Union[int, str]) -> str:
        """
        Formats node identifiers for SPICE compatibility.
        - Converts 0 or '0' to 'GND'
        - Accepts alphanumeric labels like 'IN', 'VDD', 'N001'
        - Normalizes all to clean string
        """
        if isinstance(index, (int, float)) and index == 0:
            return "GND"
        if isinstance(index, str):
            if index.strip() == "0":
                return "GND"
            return index.strip()

        return f"N{index:03d}"
