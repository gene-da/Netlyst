from Netlist.Components import *

title = "Netlist Generation Examples - Chapter 3"
doc = 'Data ﬁelds that are enclosed in less-than and greater-than signs (‘< >’) are optional. All indicated punctuation (parentheses, equal signs, etc.) is optional but indicate the presence of any delimiter. Further, future implementations may require the punctuation as stated. A consistent style adhering to the punctuation shown here makes the input easier to understand. With respect to branch voltages and currents, ngspice uniformly uses the associated reference convention (current ﬂows in the direction of voltage drop).'

print(TITLE(title, doc))

print()

doc = [
    'All Spice components can be placed in a list or dictionary. Where dictionary keys are the component names and can be directly called by their name for edits.',
    'All components have an instance tracking checks for duplicate components. To over ride this, use the scope variable, by default everything is in the global scope.'
]

print(COMMENT('\n'.join(doc)))

print()

print(COMMENT('3.3 Elementary Devices'))

print()

doc = [
    '3.3.1 Resistors',
    'General form:',
    '\tRXXXXXXX n+ n- <resistance|r=>value <ac=val> <m=val>',
    '\t+ <scale=val> <temp=val> <dtemp=val> <tc1=val> <tc2=val>',
    '\t+ <noisy=0|1>'
]

print(COMMENT('\n'.join(doc)))

print()

doc = [
    'Basic resistors setup being usesd in a list.'
]
print(COMMENT('\n'.join(doc)))

circuit_list = [
    R(1, 1, 2, 100),
    R('RC1', 12, 17, '1k'),
    R(2, 5, 7, '1k', ac='2k'),
    R('RL', 1, 4, '2k', m=2),
]

for comp in circuit_list:
    print(comp)

print()

doc = [
    'Setup and calling of a circuit dictionary.',
    '\t',
    'TODO: In netlist class the circuit definitions might be stored as a dirctionary but passed in as a list. This in theory should allow easier declaration and for easy access for iteration and edits.',
    'This is not implemented yet, but will be in the future.',
    '\t'
]

print(COMMENT('\n'.join(doc)))
circuit_dict = {}

for comp in circuit_list:
    circuit_dict[comp.name] = comp
    
print(circuit_dict['R2'])

for comp in circuit_dict:
    print(circuit_dict[comp])