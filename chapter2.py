from Netlist.Components import *
# Title block
doc = [
    "2.1 .TITLE Statement",
    "Defines the title of the simulation. Appears as the first non-comment line.",
    "Used to describe the purpose or identifier of the circuit simulation file.",
    "While it doesn’t affect simulation behavior, it makes your files not look like total chaos."
]
title = "Netlist Generation Examples - Chapter 2"
print(TITLE(title, "\n".join(doc)))

print()

doc = [
    "2.4 Comment Lines",
    "Comment lines begin with an asterisk (*) in the first column.",
    "Use them to explain circuit functionality, assumptions, or to leave snarky notes to your future self.",
    "These are ignored by the simulator but critical for documentation and sanity."
]
print(COMMENT("\n".join(doc)))


doc = [
    "2.5 .MODEL Statement",
    "Used to define device-level parameters like transistors, diodes, etc.",
    "Format: .MODEL name type (parameter=value ...)",
    "Supports long parameter lines with continuation character for clarity.",
    "This one defines an NPN BJT with moderate gain and base-emitter voltage swing.",
]
print(MODEL('MOD1', 'npn', '(bf=50 is=1e-13 vbf=50)', doc="\n".join(doc)))

print()

doc = [
    "2.6 .SUBCKT Statement",
    "Defines a reusable block of components. Good for hierarchy, better for your blood pressure.",
    "Specify external nodes followed by the component definitions inside.",
    "Supports parameters and nested subcircuits.",
]
print(COMMENT("\n".join(doc)))

circuit = [
    R(1, 1, 2, '10k'),
    R(2, 2, 3, '5k')
]

sub = SUBCKT(name='vdivide', nodes=[1, 2, 3], circuit=circuit, doc='The following are the subcircuit definition cards:\n ')

doc = [
    "2.6.1 Subcircuit Instance (.X)",
    "Instantiates a previously defined subcircuit with named nodes.",
    "Optional parameters can override those inside the .SUBCKT block.",
    "This is where modular design in SPICE actually pays off.",
]

vdiv = X(name='vdiv1', nodes=[10, 7, 0], subckt=sub, doc='\n'.join(doc))

print(vdiv)
print(sub)

print()

doc = [
    "2.7 .GLOBAL Statement",
    "Declares nodes that are global across all subcircuits.",
    "Useful for power rails or common signal references.",
    "Don’t abuse it — it can cause confusion if overused.",
]
print(COMMENT("\n".join(doc)))
print(GLOBAL([0, 'vcc']))

print()

doc = [
    "2.8 .INCLUDE Statement",
    "Includes an external SPICE model or netlist file.",
    "Use this to import vendor-supplied models (e.g., opamps, MOSFETs).",
    "Path must be accessible from simulation environment — don’t hardcode garbage paths.",
]
print(COMMENT("\n".join(doc)))
print(INCLUDE('/users/spice/common/bsim3-param.mod'))

print()

doc = [
    "2.9 .INCPSLT Statement",
    "Similar to .INCLUDE but may be used for platform-specific tools or versioned libraries.",
    "Some tools treat this differently depending on simulation settings.",
    "If .INCLUDE doesn’t work, .INCPSLT is your plan B.",
]
print(COMMENT("\n".join(doc)))
print(INCPSLT('/users/spice/models/OPA1641.lib'))

print()


doc = [
    "2.10 .LIB Statement",
    "Loads a specific section from a SPICE model library file.",
    "Syntax: .LIB path section_name",
    "Perfect for pulling only the exact models you need from bloated vendor files.",
]
print(COMMENT("\n".join(doc)))
print(LIB('/users/spice/common/mosfets.lib mos1'))

print()

doc = [
    "2.11 .PARAM Statement",
    "Defines named constants or expressions for use in netlist values.",
    "Supports math, functions, and helps reduce repetitive code.",
    "Also makes your netlists look like they were written by someone who passed algebra.",
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

doc = [
    "2.12 .FUNC Statement",
    "Defines a named function for reuse in parameter expressions.",
    "Syntax: .FUNC name(args) {expression}",
    "Use this for repeated expressions or to pretend you’re writing actual code.",
]
print(COMMENT('\n'.join(doc)))
print(FUNC('icos(x)', '{cos(x) - 1}'))
print(FUNC('f(x,y)', '{x*y}'))
print(FUNC('foo(a,b)', '{a + b}'))

print()

doc = [
    "2.13 .CSPARAM Statement",
    "Used for conditional or computed parameters in subcircuits.",
    "Typically appears after basic parameters to define chained expressions.",
    "Think of it like a dependency resolver for parameter math.",
]
print(COMMENT("\n".join(doc)))
print(PARAM([Parameter('pippo', '5')]))
print(PARAM([Parameter('pp', '6')]))
print(CSPARAM(Parameter('pippp', '{pippo + pp}')))
print(PARAM([Parameter('p', '{pp}')]))

print()
doc = [
    "2.14 .TEMP Statement",
    "Sets the simulation temperature in degrees Celsius.",
    "This affects models with temperature-dependent behavior (e.g., BJTs, diodes).",
    "Pro tip: simulate at 125°C if you want to see what 'thermal runaway' really means.",
]
print(COMMENT("\n".join(doc)))
print(TEMP('27'))