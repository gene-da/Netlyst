from typing import Optional, Union,Tuple
from Netlist.Components import SpiceElement, Nodes
from Netlist.Components.Sources.Independent.source_analysis import DCT, ACA, DISTOF
from Netlist.Components.Sources.Independent.signals import*

"""
VXXXXXXX N+ N- ((DC) DC/TRAN VALUE>) (AC (ACMAG ((ACPHASE)))
+ (DISTOF1 (F1MAG (F1PHASE))) (DISTOF2 (F2MAG (F2PHASE)))
""" 

class V(SpiceElement, Nodes):
    def __init__(
        self,
        name: Union[int, str],
        node_p: Union[str, int],
        node_n: Union[str, int],
        dc: Optional[DCT] = None,
        ac: Optional[ACA] = None,
        distof1: Optional[DISTOF] = None,
        distof2: Optional[DISTOF] = None,
    ) -> None:
        """Voltage Source Class

        Args:
            name (str): Name of the voltage source.
            node_p (str): Positive node of the voltage source.
            node_n (str): Negative node of the voltage source.
            dc (Optional[DCT], optional): DC analysis parameters. Defaults to None.
            ac (Optional[ACA], optional): AC analysis parameters. Defaults to None.
            distof1 (Optional[DISTOF], optional): First distortion analysis parameters. Defaults to None.
            distof2 (Optional[DISTOF], optional): Second distortion analysis parameters. Defaults to None.
        """
        SpiceElement.__init__(self)
        Nodes.__init__(self)
        if isinstance(name, str):
            resolved_name = name
        elif isinstance(name, int):
            resolved_name = f'V{name}'
        else:
            raise TypeError(f"Invalid type for name: {type(name)}")
        self.name = resolved_name
        
        self.nodes["n+"] = self._format_node(node_p)
        self.nodes["n-"] = self._format_node(node_n)
        
        self.dc = dc if dc is None else dc
        self.ac = ac if ac is None else ac
        self.distof1 = distof1 if distof1 is None else distof1
        self.distof2 = distof2 if distof2 is None else distof2
        
    def to_string(self) -> str:
        """Convert the voltage source to a SPICE string representation.

        Returns:
            str: SPICE string representation of the voltage source.
        """
        result = f"{self.name:<8} {self.nodes['n+']:<8} {self.nodes['n-']:<8}"
        if self.dc:
            result += f" {self.dc.__str__():<8}"
        if self.ac:
            result += f" {self.ac.__str__():<8}"
        if self.distof1:
            result += f" {self.distof1.__str__():<16}"
        if self.distof2:
            result += f" {self.distof2.__str__():<16}"
        return result
    
    def to_line(self) -> str:
        """Convert the voltage source to a SPICE line representation.

        Returns:
            str: SPICE line representation of the voltage source.
        """
        result = f"{self.name} {self.nodes['n+']} {self.nodes['n-']}"
        
        # If AC or distortion parameters are present, only include DC
        if self.ac or self.distof1 or self.distof2:
            if self.dc:
                result += f" {self.dc}"
        else:
            # If no AC or distortion, include DC if present
            if self.dc:
                result += f" {self.dc}"
        
        return result

if __name__ == "__main__":
    from Netlist.Components import R
    
    print(R(1, 1, 2, '1k'))
    # Example usage
    print(V(
        name=1,
        node_p=1,
        node_n=0,
        dc=DCT(dc_tran=5.0),
        ac=ACA(ac_mag=1.0, ac_phase=0.0),
        distof1=DISTOF(iter=1, mag=0.1, phase=30),
        distof2=DISTOF(iter=2, mag=0.05, phase=45)
    ))
    print(V(
        name='VCC',
        node_p=13,
        node_n=2,
        dc=DCT(dc_tran=0.001),
        ac=ACA(ac_mag=1, ac_phase=0),
    ))