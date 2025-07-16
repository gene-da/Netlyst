from typing import Optional, Union, Tuple
from dataclasses import dataclass
from Netlist.Components import SpiceElement, Nodes
from Utilities.Converter import Conversion

"""
VXXXXXXX N+ N- ((DC) DC/TRAN VALUE>) (AC (ACMAG ((ACPHASE)))
+ (DISTOF1 (F1MAG (F1PHASE))) (DISTOF2 (F2MAG (F2PHASE)))

IYYYYYYY N+ N- <<DC> DC/TRAN VALUE> <AC <ACMAG <ACPHASE>>>
+ <DISTOF1 <F1MAG <F1PHASE>>> <DISTOF2 <F2MAG <F2PHASE>>>
""" 
    
@dataclass
class DCT():
    """DC Analysis Class for Independent Sources.
    This class is used to represent the DC analysis parameters of independent sources.
    """
    def __init__(
        self,
        dc_tran: Union[float, int, str],
    ) -> None:
        """DC Analysis Parameters

        Args:
            dc_tran (Union[float, int, str]): DC voltage/current value.
        """
        super().__init__()
        self.dc_tran = Conversion.spice(dc_tran)
        
    def __str__(self) -> str:
        return f"DC {self.dc_tran}"
        

@dataclass
class ACA():
    """AC Analysis Class for Independent Sources.
    This class is used to represent the AC analysis parameters of independent sources.
    """
    def __init__(
        self,
        ac_mag: Union[float, int, str],
        ac_phase: Optional[Union[float, int, str]],
    ) -> None:
        """AC Analysis Parameters

        Args:
            ac_mag (Union[float, int, str]): AC magnitude value.
            ac_phase (Union[float, int, str]): AC phase value.
        """
        super().__init__()
        self.ac_mag = Conversion.spice(ac_mag)
        if ac_phase is not None:
            self.ac_phase = Conversion.spice(ac_phase)
        else:
            self.ac_phase = None
        
    def __str__(self) -> str:
        return f"AC {self.ac_mag} {self.ac_phase}"

@dataclass
class DISTOF():
    def __init__(
        self,
        iter: int,
        mag: Union[float, int, str],
        phase: Union[float, int, str],
    ) -> None:
        """Distortion Analysis Parameters

        Args:
            iter (int): Distortion iteration number.
            mag (Union[float, int, str]): Distortion magnitude.
            phase (Union[float, int, str]): Distortion phase.
        """
        super().__init__()
        if iter not in [1, 2]:
            raise ValueError("DISTOF must be either 1 or 2")
        
        self.iter = iter
        self.mag = Conversion.spice(mag)
        self.phase = Conversion.spice(phase)
        
    def __str__(self) -> str:
        return f"DISTOF{self.iter} {self.mag} {self.phase}"

if __name__ == "__main__":
    # Example usage
    dc = DCT(dc_tran=5.0)
    ac = ACA(ac_mag=10.0, ac_phase=30.0)
    dist1 = DISTOF(iter=1, mag=2.0, phase=45.0)
    dist2 = DISTOF(iter=2, mag=3.0, phase=60.0)

    print(dc)
    print(ac)
    print(dist1)
    print(dist2)