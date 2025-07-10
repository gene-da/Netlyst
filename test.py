from Netlist.Components import*
from Netlist.Classes.Base import*

print(Conversion.spice('1Meg'))
mod = MODEL('2N2222', 'npn', '(bf=50 is=1e-13 vbf=50)')

r1 = R('R1', 1, 2, '1M')

print(r1)

print(mod)