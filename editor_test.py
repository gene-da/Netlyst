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
        
circuit = [
    TITLE(title='Test Circuit', doc='This is a test circuit title.'),
    COMMENT('This is a test comment block.'),
    MODEL(name='BC451', mtype='bjt', model='IS=1e-14 BF=100'),
    MODEL(name='BC451', mtype='bjt', model='IS=1e-14 BF=100', scope='local'),
    R(name='R1', node_p=2, node_n=3, value=1000),
    COMMENT('This is another test comment block. The following components are part of the circuit.'),
    R(name='R1', node_p=2, node_n=3, value=1000, scope='local'),
    CSPARAM(ident='pippo', expr=5, doc='This is a test CSPARAM directive.'),
    AC(variation=Points.dec, pts=100, fstart=1e3, fstop=1e6, doc='AC analysis from 1kHz to 1MHz'),
    CONTROL(controls=control, doc='Control commands for the simulation'),
    V(name='V1', node_p=1, node_n=0, dc_tran=5, ac_mag=1, ac_phase=0, doc='Voltage source with DC and AC values'),
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
    print(f'{'':4}{element.id.cname:<10}\t{element.id.string:<50}')

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

for name, elements in grouped.items():
    print(f'Group: {name.value.capitalize()}')
    for element in elements:
        print(f'{'':2}{element.id.string:<50}')
    print()