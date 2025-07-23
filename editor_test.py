from Editor import*
from Editor.Components import *

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
    COMMENT('This is another test comment block. The following components are part of the circuit.'),
    R(name='R1', node_p=2, node_n=3, value=1000),
    R(name='R1', node_p=2, node_n=3, value=1000, scope='local'),
    CSPARAM(ident='pippo', expr=5, doc='This is a test CSPARAM directive.'),
    AC(variation=Points.dec, pts=100, fstart=1e3, fstop=1e6, doc='AC analysis from 1kHz to 1MHz'),
    CONTROL(controls=control, doc='Control commands for the simulation'),
    END(),
]

print('=====================================Testing __str__() method:======================================\n')
for element in circuit:
    print(element)

print('=====================================Testing to_line() method:======================================\n')

for element in circuit:
    if element.to_line():
        print(element.to_line())

print('===================================Testing Observing UID Options:===================================\n')

dot_commands = ('TITLE', 'MODEL', 'AC', 'CONTROL', 'END', 'CSPARAM')

commands = []

elementry = []

comments = []

print('\nFiltered .Commasnds:')
for element in circuit:
    if element.__class__.__name__ in dot_commands:
        commands.append(element)
        
for element in commands:
    print(element)

print('\nFiltered Non-Dot Commands:')      
for element in circuit:
    if element.__class__.__name__ not in dot_commands and element.__class__.__name__ != 'COMMENT':
        elementry.append(element)
        
for element in elementry:
    print(element)
        
print('\nComment Elements:')
for element in circuit:
    if element.__class__.__name__ == 'COMMENT':
        comments.append(element)
        
for element in comments:
    print(element)

