from Netlist.Components import *

# Chapter 4 - Voltage and Current Sources

print(TITLE('Independent Sources Example'))

# 4.1 Independent Sources for Voltage or Current
print('\n4.1 Independent Sources for Voltage or Current')

print(V('VCC', 10, 0, dc=DCT(6)))

print(V('VIN', 13, 2, dc=DCT(0.001), ac=ACA(1), signal=SIN(0, 1, '1Meg', 0, 0, 0)))

print(I('ISRC', 23, 21, ac=ACA(0.333, 45.0), signal=SFFM(0, 1, '10k', 5, '1k', 0, 0, 0)))

print(V('VMEAS', 12, 9))

print(V('VCAR', 1, 0, distof1=DISTOF(1, 0.1, -90.0)))

print(V('VMOD', 2, 0, distof2=DISTOF(2, 0.01)))

print(I('IIN1', 1, 5, ac=ACA(1), distof1=DISTOF(1), distof2=DISTOF(2, 0.001)))

# 4.1.1 Pulse
print('\n4.1.1 Pulse')
print(V('VIN', 3, 0, signal=PULSE(-1, 1, '2n', '2n', '2n', '50n', '500n', 5), scope='pulse_example'))
