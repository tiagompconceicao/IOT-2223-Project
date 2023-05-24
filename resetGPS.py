import axp202
from machine import UART

axp=axp202.PMU(address=axp202.AXP192_SLAVE_ADDRESS)
axp.setLDO3Voltage(3300)   # T-Beam GPS  VDD    3v3
axp.enablePower(axp202.AXP192_LDO3)

dev = UART(1, 9600, pins=('G12','G34'))
msg = b'\xb5b\x06\x00\x14\x00\x01\x00\x00\x00\xd0\x08\x00\x00\x80%\x00\x00\x07\x00\x03\x00\x00\x00\x00\x00\xa2\xb5'
dev.write(msg)