from Editor.Components import *

pulse = PULSE(2.5, 2.5, 0, 1e-9, 1e-9, 1e-9, 10e-9, 20e-9)
i2 = I('2', 1, 0, td_value=pulse)
print(i2)
print(i2.to_line())

i2.td_value = SIN(0, 0, '1k', 0, 0, 0)
print(i2)
print(i2.to_line())

i2.td_value = SFFM(0, 2, 20, 45, '1k', '1m', 0, 0)
print(i2)
print(i2.to_line())

i2.td_value = EXP(2, 5, '2n')
print(i2)
print(i2.to_line())

i2.td_value = PWL([(0, -7), (10, -7), (11, -3), (17, -3), (18, -7), (50, -7)], r=0, td='15n')
print(i2)
print(i2.to_line())

i2.td_value = AM(0.5, 2, 1.8, '20K', '5M', '1m')
print(i2)
print(i2.to_line())

i2.td_value = TRNOISE('20n', '0.5n', 0, 0)
print(i2)
print(i2.to_line())

i2.td_value = TRNOISE(0, '10p', 1.1, '12p')
print(i2)
print(i2.to_line())

i2.td_value = TRNOISE(20, '10p', 1.1, '12p')
print(i2)
print(i2.to_line())

i2.td_value = TRNOISE('1m', '1u', 1.0, '0.1m', '15m', '22u', '50u')
print(i2)
print(i2.to_line())

i2.td_value = TRRANDOM(2, '10m', 0, 1)
print(i2)
print(i2.to_line())

i2.td_value = TRRANDOM(1, '1u', '0.5u', 0.5, 0.5)
print(i2)
print(i2.to_line())

i2.td_value = EXTERNAL('')
print(i2)
print(i2.to_line())

i2.td_value = EXTERNAL('<m = xx>')
print(i2)
print(i2.to_line())

i2.td_value = PORNUM(1, 0, 100)