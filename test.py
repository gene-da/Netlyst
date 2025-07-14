from Netlist.Components import*
from Netlist.Classes.Base import*

title = TITLE(
    "Band-Pass Filter Design",
    doc="""
    This netlist describes a band-pass filter circuit.
    It uses standard RLC components with a center frequency around 1kHz.
    Ideal for audio pre-processing simulations.
    """
)
print(title.to_string())
comment = COMMENT("This is a comment", doc="Comment for the circuit")
print(comment.to_string())

r1 = R(1, 1, 2, 1_000_000)
print(r1)

r1.value = 2_000_000
r1.scale = 1_000
print(r1)
r2 = R(2, 1, 2, 1_000_000, ac='5', m=5, scale=1e-6, temp=27, dtemp=0.1, tc1=0.01, tc2=0.0)
print(r2)

rmod = RMOD(1, 1, 2, 1_000_000)
r3 = R(3, 1, 2, 1_000_000, mname=rmod)
print(r3)
print(rmod)

c1 = C(1, 1, 2, 1e-6)
c2 = C(2, 1, 2, 1e-6,m=5, scale=1e-6, temp=27, dtemp=0.1, tc1=0.01, tc2=0.02, ic=0.0)
print(c1)
print(c2)

cmod = CMOD(1, 1e-6, 1e-12, 1e-12, 1e-6, 0.01, 0.02, 27, 1e-6, 1e-6)
c3 = C(3, 1, 2, 1e-6, mname=cmod)
print(c3)
print(cmod)

l1 = L(1, 1, 2, 1e-6)
l2 = L(2, 1, 2, 1e-6, m=5, scale=1e-6, temp=27, dtemp=0.1, tc1=0.01, tc2=0.02, ic=0.0)
print(l1)
print(l2)

lmod = LMOD(1, 1e-6, 1e-12, 1e-12, 1e-6, 0.01, 0.02, 27, 1e-6, 1e-6)
l3 = L(3, 1, 2, 1e-6, mname=lmod)
print(l3)
print(lmod)

s1 = S(1, 1, 2, 3, 4, mname=SW('SW1', vt=0.5, vh=1.0, ron=10, roff=100), state='ON')
print(s1)
s1.state = 'OFF'
print(s1)

s2 = W(2, 1, 2, 'V1', mname=CSW('CSW1', it=0.5, ih=1.0, ron=10, roff=100), state='ON')
print(s2)
s2.state = 'OFF'
print(s2)

end = END(doc="End of the circuit")
print(end.to_string())
