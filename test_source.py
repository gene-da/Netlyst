from Netlist.Components import *

# Chapter 4 - Voltage and Current Sources

print(TITLE('Independent Sources Example'))

# 4.1 Independent Sources for Voltage or Current
print('\n* 4.1 Independent Sources for Voltage or Current')

print(V('VCC', 10, 0, dc=DCT(6)))
print(V('VIN', 13, 2, dc=DCT(0.001), ac=ACA(1), signal=SIN(0, 1, '1Meg', 0, 0, 0)))
print(I('ISRC', 23, 21, ac=ACA(0.333, 45.0), signal=SFFM(0, 1, '10k', 5, '1k', 0, 0, 0)))
print(V('VMEAS', 12, 9))
print(V('VCAR', 1, 0, distof1=DISTOF(1, 0.1, -90.0)))
print(V('VMOD', 2, 0, distof2=DISTOF(2, 0.01)))
print(I('IIN1', 1, 5, ac=ACA(1), distof1=DISTOF(1), distof2=DISTOF(2, 0.001)))

# 4.1.1 Pulse
print('\n* 4.1.1 Pulse')
print(V('VIN', 3, 0, signal=PULSE(-1, 1, '2n', '2n', '2n', '50n', '500n', 5), scope='pulse_example'))

# 4.1.2 Sinusoidal
print('\n* 4.1.2 Sinusoidal')
print(V('VIN', 3, 0, signal=SIN(0, 1, '1Meg', 0, 0, 0), scope='sinusoidal_example'))

# 4.1.3 Exponential
print('\n* 4.1.3 Exponential')
print(V('VIN', 3, 0, signal=EXP(-4, -1, '2n', '30n', '60n', '40n'), scope='exponential_example'))

# 4.1.4 Piecewise Linear
print('\n* 4.1.4 Piecewise Linear')
print(V('VCLOCK', 7, 5, signal=PWL(0, -7, [(0, -7), ('10n', -7), ('11n', -3), ('17n', -3), ('18n', -7), ('50n', -7)], r=0, td='15n'), scope='pwl_example'))

# 4.1.5 Single-Frequency FM
print('\n* 4.1.5 Single-Frequency FM')
print(V(1, 12, 0, signal=SFFM(0, 2, 20, 45, '1k', '1m', 0, 0), scope='sffm_example'))

# 4.1.6 Amplitude modulation source (AM)
print('\n* 4.1.6 Amplitude Modulation Source (AM)')
print(V(1, 12, 0, signal=AM(0.5, 2, 1.8, '20k', '5Meg', '1m'), scope='am_example'))

# 4.1.7 Transient noise source
print('\n* 4.1.7 Transient Noise Source')
print(V('VNoiw', 1, 0, dc=DCT(0), signal=TRNOISE('20n', '0.5n', 0, 0)))
print(V('VNoilof', 1, 0, dc=DCT(0), signal=TRNOISE('0', '10p', 1.0, '12p')))
print(V('VNoiwlof', 1, 0, dc=DCT(0), signal=TRNOISE(20, '10p', 1.0, '12p')))
print(I('IALL', 10, 0, dc=DCT(0), signal=TRNOISE('1m', '1u', 1.0, '0.1m', '15m', '22u', '50u')))

# 4.1.8 Random voltage source
print('\n* 4.1.8 Random Voltage Source')
print(V('VR1', 1, 0, dc=DCT(0), signal=TRRANDOM(2, '10m', (0, 1))))
print(V('V1', 1, 0, dc=DCT(0), signal=TRRANDOM(1, '1u', ('0.5u', 0.5, 0.5))))

print(END())