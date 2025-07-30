"""
IYYYYYYY N+ N- <<DC> DC/TRAN VALUE> <AC <ACMAG <ACPHASE>>>
+ <DISTOF1 <F1MAG <F1PHASE>>> <DISTOF2 <F2MAG <F2PHASE>>>
"""

"""
VXXXXXXX N+ N- <<DC> DC/TRAN VALUE> <AC <ACMAG <ACPHASE>>>
+ <DISTOF1 <F1MAG <F1PHASE>>> <DISTOF2 <F2MAG <F2PHASE>>>
"""

from ..Base import *
from .source import *
from typing import Optional, Union

class I(SpiceElement, Nodes):
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
        td_value: Optional[IndependentSource] = None,
        doc: Optional[str] = None,
        scope: str = 'global',
    ) -> None:
        SpiceElement.__init__(
            self,
            comp_prefix='I',
            name=name,
            doc=doc,
            scope=scope,
        )
        Nodes.__init__(self, node_p=node_p, node_n=node_n)

        self._dc_tran = dc_tran
        self._ac_mag = ac_mag
        self._ac_phase = ac_phase
        self._f1_mag = f1_mag
        self._f1_phase = f1_phase
        self._f2_mag = f2_mag
        self._f2_phase = f2_phase
        self._td_value = str(td_value) if td_value else None
        
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
    def td_value(self, value: Optional[IndependentSource]) -> None:
        if value is None:
            self._td_value = None
        else:
            self._td_value = str(value)
        
    @header
    @property
    def output(self) -> str:
        output = []
        if self._dc_tran:
            if self._ac_mag or self._ac_phase or self._f1_mag or self._f1_phase or self._f2_mag or self._f2_phase:
                output.append(f'{self.dc_tran}')
            else:
                output.append(f'"DC {self.dc_tran}"')
                
        if self._ac_mag:
            output.append(f'AC {self._ac_mag}')
            if self._ac_phase:
                output.append(f'{self._ac_phase}')
                
        if self._td_value:
            output.append(f'{self._td_value}')
                
        if self._f1_mag and self._td_value is None:
            app = [f'DISTOF1 {self._f2_mag}']
            if self._f2_phase:
                app.append(f'{self._f2_phase}')
            out = ' '.join(app)
            output.append(f'{out:<20}')

        if self._f2_mag and self._td_value is None:
            app = [f'DISTOF2 {self._f2_mag}']
            if self._f2_phase:
                app.append(f'{self._f2_phase}')
            out = ' '.join(app)
            output.append(f'{out:<20}')
        
        return ' '.join(output)