"""
VXXXXXXX N+ N- <<DC> DC/TRAN VALUE> <AC <ACMAG <ACPHASE>>>
+ <DISTOF1 <F1MAG <F1PHASE>>> <DISTOF2 <F2MAG <F2PHASE>>>
"""

from ..Base import *
from .source import *
from typing import Optional, Union

class V(SpiceElement, Nodes, Source):
    def __init__(
        self,
        name: Union[str, int],
        node_p: Union[int, str],
        node_n: Union[int, str],
        dc_tran: Optional[Union[float, int, str]] = None,
        ac_mag: Optional[Union[float, int, str]] = None,
        ac_phase: Optional[Union[float, int, str]] = None,
        f1_mag: Optional[Union[float, int, str]] = None,
        f1_phase: Optional[Union[float, int, str]] = None,
        f2_mag: Optional[Union[float, int, str]] = None,
        f2_phase: Optional[Union[float, int, str]] = None,
        td_value: Optional[TimeDependentSource] = None,
        doc: Optional[str] = None,
        scope: str = 'global',
    ) -> None:
        SpiceElement.__init__(
            self,
            comp_prefix='V',
            name=name,
            doc=doc,
            scope=scope,
        )
        Nodes.__init__(self, node_n=node_n, node_p=node_p)
        
        self._dc_tran = dc_tran
        self._ac_mag = ac_mag
        self._ac_phase = ac_phase
        self._f1_mag = f1_mag
        self._f1_phase = f1_phase
        self._f2_mag = f2_mag
        self._f2_phase = f2_phase
        self._td_value = td_value.string if td_value else None
        
        self.id.etype = SpiceElementType.SOURCE
        
    @property
    def dc_tran(self) -> Optional[Union[float, int, str]]:
        return self._dc_tran    
    @dc_tran.setter
    def dc_tran(self, value: Union[float, int, str]) -> None:
        self._dc_tran = value
        
    @property
    def ac_mag(self) -> Optional[Union[float, int, str]]:
        return self._ac_mag
    @ac_mag.setter
    def ac_mag(self, value: Union[float, int, str]) -> None:
        self._ac_mag = value
        
    @property
    def ac_phase(self) -> Optional[Union[float, int, str]]:
        return self._ac_phase
    @ac_phase.setter
    def ac_phase(self, value: Union[float, int, str]) -> None:
        self._ac_phase = value
        
    @property
    def f1_mag(self) -> Optional[Union[float, int, str]]:
        return self._f1_mag
    @f1_mag.setter
    def f1_mag(self, value: Union[float, int, str]) -> None:
        self._f1_mag = value
        
    @property
    def f1_phase(self) -> Optional[Union[float, int, str]]:
        return self._f1_phase
    @f1_phase.setter
    def f1_phase(self, value: Union[float, int, str]) -> None:
        self._f1_phase = value
    
    @property
    def f2_mag(self) -> Optional[Union[float, int, str]]:
        return self._f2_mag
    @f2_mag.setter
    def f2_mag(self, value: Union[float, int, str]) -> None:
        self._f2_mag = value
        
    @property
    def f2_phase(self) -> Optional[Union[float, int, str]]:
        return self._f2_phase
    @f2_phase.setter
    def f2_phase(self, value: Union[float, int, str]) -> None:
        self._f2_phase = value
    
    @property
    def td_value(self) -> Optional[str]:
        return self._td_value
    @td_value.setter
    def td_value(self, value: TimeDependentSource) -> None:
        self._td_value = value.string if value else None
        
    def _get_headers(self):
        return ['id_name', 'nodes', 'dc_tran', 'ac_mag', 'ac_phase', 'f1_mag', 'f1_phase', 'f2_mag', 'f2_phase', 'td_value']
        