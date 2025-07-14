# from Netlist.Components import *
from Netlist.Components import*

# Title block
title = TITLE(
    "Band-Pass Filter Design",
    doc="""
    This netlist describes a band-pass filter circuit.
    It uses standard RLC components with a center frequency around 1kHz.
    Ideal for audio pre-processing simulations.
    """
)
print(title.to_string() + "\n")

# Comment block
comment = COMMENT("Instantiates BP_FILTER and supporting components", doc="Top-level circuit configuration")
print(comment.to_string() + "\n")

# Subcircuit internal components
r1 = R("R1", "IN", "N1", "1k", doc="Stage 1 resistor", scope='subcircuit')
r2 = R("R2", "N1", "OUT", "2k", ac="1", temp="25", tc1="0.002", tc2="0.0005", doc="Biasing resistor", scope='subcircuit')
c1 = C("C1", "IN", "N2", "100n", doc="Input coupling capacitor", scope='subcircuit')
l1 = L("L1", "N2", 0, "10m", doc="Choke inductor", scope='subcircuit')

# Subcircuit definition
bp_filter = SUBCKT(
    name="BP_FILTER",
    nodes=["IN", "OUT", 0],
    circuit=[r1, r2, c1, l1],
    doc="Band-pass filter subcircuit with RLC elements."
)
print(bp_filter.to_string() + "\n")

op_amp = SUBCKT(
    name='Ideal Op-Amp',
    nodes=['IN+', 'IN-', 'OUT', 0],
    circuit=[
        R("R1", "IN+", "OUT", "10k", doc="Feedback resistor", scope='subcircuit'),
        R("R2", "IN-", "OUT", "10k", doc="Input resistor", scope='subcircuit'),
        C("C1", "OUT", 0, "1u", doc="Output capacitor", scope='subcircuit')
    ],
    doc="Ideal operational amplifier subcircuit with feedback and input resistors."
)
# Top-level instantiation of subcircuit (as if used in a schematic)
r3 = R("R1", "VIN", "IN", "100", doc="Input resistor to subcircuit")
print(r3.to_string() + "\n")

# Flat subcircuit instance line
print(bp_filter.to_line() + "\n")

# End marker
end = END(doc="End of the circuit")
print(end.to_string())
