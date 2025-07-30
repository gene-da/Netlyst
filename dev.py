from Editor.Components import *

pulse = PULSE(2.5, 2.5, 0, 1e-9, 1e-9, 1e-9, 10e-9, 20e-9)
i2 = I('2', 1, 0, td_value=pulse)
print(i2)
i2.td_value = SIN(0, 0, '1k', 0, 0, 0)
print(i2)

i2.td_value = SFFM(0, 0, '1k', 0, '1k', 0, 0, 0)
print(i2)

i2.td_value = EXP(2, 5, '2n')
print(i2)

i2.td_value = PWL(VT(0, 0), [VT(1, 1), VT(2, 2), VT(3, 3), VT(4, 4), VT(5, 5), VT(6, 6)])
print(i2)

i2.td_value = PWL(VT(0, 0), r=0.1, td=0.2)
print(i2)