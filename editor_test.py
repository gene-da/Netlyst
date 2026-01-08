from Editor import*
from Editor.Components import *
from dataclasses import dataclass
from typing import List, Tuple, Type, Dict, Union, Optional
from collections import defaultdict

control = [
    'save vcc#branch',
    'run',
    'plot vcc#branch',
    'rusage all'
]

doc = 'Blorfanex quindle rathmop ziggulant drebskorn flanterly opmivix trellagorn snubwicket framoodle gortanzil wexomph.'

vsens = V(name='VSENS', node_p=13, node_n=5, doc=doc)
vz = V(name='VZ', node_p=5, node_n=17, doc=doc)
        
circuit = [
    TITLE(title='Test Circuit', doc=doc),
    COMMENT('This is a test comment block.'),
    MODEL(name='BC451', mtype='bjt', model='IS=1e-14 BF=100', doc=doc),
    MODEL(name='BC451', mtype='bjt', model='IS=1e-14 BF=100', scope='local'),
    R(name='R1', node_p=2, node_n=3, value=1000, doc=doc),
    COMMENT('This is another test comment block. The following components are part of the circuit.'),
    R(name='R1', node_p=2, node_n=3, value=1000, scope='local'),
    CSPARAM(ident='pippo', expr=5, doc=doc),
    AC(variation=Points.dec, pts=100, fstart=1e3, fstop=1e6, doc=doc),
    CONTROL(controls=control, doc=doc),
    V(name='V1', node_p=1, node_n=0, dc_tran=5, ac_mag=1, ac_phase=0, doc=doc),
    V(name='VCC', node_p=10, node_n=0, dc_tran=6, doc=doc),
    V('VIN', 13, 2, 0.001, 1),
    G(1, 2, 0, 5, 0, 0.1, 0.01),
    E(1, 2, 3, 14, 1, 2.0),
    F(1, 13, 5, vsens, 5, 2),
    H('X', 5, 17, vz, '0.5K'),
    B('B1', 0, 1, i='cos(v(1))+sin(v(2))'),
    B('B2', 0, 1, v='ln(cos(log(v(1,2)^2)))-v(3)^4+v(2)^v(1)'),
    B('B3', 3, 4, i='17'),
    B('B4', 3, 4, v='exp(pi^i(vdd))'),
    B('B5', 2, 0, v='V(1) < {Vlow} ? {Vlow} : V(1) > {Vhigh} ? {Vhigh} : V(1)'),
    END(),
]

def printt(title: str, width: int = 100, fill: str = '\u2550') -> str:
    title = title.strip()
    total_fill = width - len(title) - 2
    left = total_fill // 2
    right = total_fill - left
    print(f'\n{fill * left} {title} {fill * right}\n')


printt('Testing to_string() method')

for element in circuit:
    if element.to_string():
        print(element.to_string())


printt('Testing to_line() method')

for element in circuit:
    if element.to_line():
        print(element.to_line())

printt('Testing and Observing ID property')

print(f'{'':4}{'Component':<10}\t{'ID String':<50}')
print(f'{'':4}{'\u2500'*10}\t{'\u2500'*50}')
for element in circuit:
    print(f'{'':4}{element.id.iname:<10}\t{element.id.string:<50}')

printt('Testing Grouping by ID Type')

grouped: Dict[SpiceElementType, List[SpiceElement]] = defaultdict(list)

for element in circuit:
    group = element.id.etype
    
    if group == SpiceElementType.STRUCTURE:
        grouped[SpiceElementType.STRUCTURE].append(element)
        
    if group == SpiceElementType.COMMAND:
        grouped[SpiceElementType.COMMAND].append(element)
        
    if group == SpiceElementType.PARAMETER:
        grouped[SpiceElementType.PARAMETER].append(element)
    
    if group == SpiceElementType.ANALYSIS:
        grouped[SpiceElementType.ANALYSIS].append(element)
    
    if group == SpiceElementType.CONTROL:
        grouped[SpiceElementType.CONTROL].append(element)
        
    if group == SpiceElementType.MODEL:
        grouped[SpiceElementType.MODEL].append(element)
    
    if group == SpiceElementType.DEVICE:
        grouped[SpiceElementType.DEVICE].append(element)
    
    if group == SpiceElementType.OTHER:
        grouped[SpiceElementType.DEVICE].append(element)
        
    if group == SpiceElementType.SOURCE:
        grouped[SpiceElementType.DEVICE].append(element)

for name, elements in grouped.items():
    print(f'Group: {name.value.capitalize()}')
    for element in elements:
        print(f'{'':2}{element.id.string:<50}')
    print()