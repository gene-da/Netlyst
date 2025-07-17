from Netlist.Components import *
# Title block
title = 'Chapter 2 Circuit Description - Test Examples'
description0 = "\tThis chapter provides test examples for circuit descriptions in SPICE simulations."
description1 = '\tThis is an example of a circuit description using SPICE syntax of a title block, comments, and subcircuit definitions.'

title_block = [title, description0, description1]
print(TITLE(title, "\n".join(title_block)))

print()

comment = [
    ' ',
    '2.4.4 End-of-line comments',
    'RF=1K Gain should be 100',
    'Check open-loop gain and phase margin',
    'The asterisk in the ﬁrst column indicates that this line is a comment line. Comment lines may be placed anywhere in the circuit description.',
    '2.4.4 End-of-line comments are not supported in this implementation.',
    ' '
]
print(COMMENT("\n".join(comment)))


doc = [
    ' ',
    '2.5 .MODEL Device Models',
    'The .MODEL statement defines a device model with specific parameters.',
    'Example: .MODEL npn (bf=50 is=1e-13 vbf=50)',
    'Automatically generates continuation lines needed for model parameters to help keep readability. The "doc" parameter calls the COMMENT class to generate a comment line. Wrapping it automatically to fit within 100 characters wide.',
    ' '
]
print(MODEL('MOD1', 'npn', '(bf=50 is=1e-13 vbf=50)', doc="\n".join(doc)))

print()

doc = [
    '2.6 .SUBCKT Subcircuits',
    'The .SUBCKT statement defines a subcircuit with specific nodes and components.'
]

print(COMMENT("\n".join(doc)))

circuit = [
    R(1, 1, 2, '10k'),
    R(2, 2, 3, '5k')
]

sub = SUBCKT(name='vdivide', nodes=[1, 2, 3], circuit=circuit, doc='The following are the subcircuit definition cards:\n ')

vdiv = X(name='vdiv1', nodes=[10, 7, 0], subckt=sub, doc='The following is the instance card:\n ')

print(vdiv)
print(sub)

print()

print(COMMENT('2.7 .GLOBAL'))
print(GLOBAL([0, 'vcc']))

print()

print(COMMENT('2.8 .INCLUDE'))
print(INCLUDE('/users/spice/common/bsim3-param.mod'))

print()

print(COMMENT('2.9 .INCPSLT'))
print(INCPSLT('/users/spice/models/OPA1641.lib'))

print()

print(COMMENT('2.10 .LIB'))
print(LIB('/users/spice/common/mosfets.lib mos1'))

print()

doc = [
    '2.11 .PARAM Parametric netlists',
    'Ngspice allows for the deﬁnition of parametric attributes in the netlists. This is an enhancement of the ngspice front-end that adds arithmetic functionality to the circuit description language.'
    'PARAM also allows for the use of comments, which are automatically wrapped to fit within 100 characters wide.',
]
print(PARAM([Parameter('pippo', '5')], doc='\n'.join(doc)))
print(PARAM(
    [
        Parameter('po', '6'),
        Parameter('pp', '7.8'),
        Parameter('pap', '{AGAUSS(pippo, 1, 1.67)}')
    ]
))
print(PARAM([Parameter('pippp', 'pippo + pp')]))
print(PARAM([Parameter('p', '{pp}')]))
print(PARAM([Parameter('pop', 'pp+p')]))

print()

doc = [
    '2.11.3 Subcircuit parameters',
    'Subcircuit parameters allow for the customization of subcircuit behavior and characteristics.',
    'They can be defined using the using a combination of the the Prameter, SUBCKT, X classes.',

]

example = [
    'Param-example'
]
amplitude = Parameter('amplitude', '1V')
print(PARAM([amplitude], doc='\n'.join(example)))

rval =  Parameter('rval', '100k')
cval = Parameter('cval', '100n')

circuit = [
    R('Ra', 'in', 'p1', f'{{2*{rval.ident}}}', scope='subcircuit1'),
    R('Rb', 'p1', 'out', f'{{2*{rval.ident}}}', scope='subcircuit1'),
    C('C1', 'p1', '0', f'{{2*{cval.ident}}}', scope='subcircuit1'),
    C('Ca', 'in', 'p2', f'{{{cval.ident}}}', scope='subcircuit1'),
    C('Cb', 'p2', 'out', f'{{{cval.ident}}}', scope='subcircuit1'),
    R('R1', 'p2', '0', f'{{{rval.ident}}}', scope='subcircuit1'),
]

sub = SUBCKT(
    name='myfilter',
    nodes=['in', 'out'],
    params=[rval, cval],
    circuit=circuit,
    doc='\n'.join(doc)
)

print(sub)
print(X('1', ['input', 'output'], sub, params=[rval, cval]))

print(V(1, 'input', '0', ac=ACA(f'{{2*{amplitude.ident}}}')))
print(END())

print()

print(COMMENT('2.12 .FUNC'))
print(FUNC('icos(x)', '{cos(x) - 1}'))
print(FUNC('f(x,y)', '{x*y}'))
print(FUNC('foo(a,b)', '{a + b}'))

print()

print(COMMENT('2.13 .CSPARAM'))
print(PARAM([Parameter('pippo', '5')]))
print(PARAM([Parameter('pp', '6')]))
print(CSPARAM(Parameter('pippp', '{pippo + pp}')))
print(PARAM([Parameter('p', '{pp}')]))

print()
print(COMMENT('2.14 .TEMP'))
print(TEMP('27'))