from basic_lib import helloWorld
from ssd1306 import SSD1306_I2C
import machine
import framebuf
from micropython import const
import hashlib
from micropyGPS import MicropyGPS
from time import sleep
from network import LoRa
import binascii
import socket
import time
import ubinascii
import axp202
from gps import GPS
import struct
from message import Message
import resetGPS
from lora import LoRaImpl


resetGPS.reset()

axp = axp202.PMU(address=axp202.AXP192_SLAVE_ADDRESS)
axp.setLDO2Voltage(3300)   # T-Beam LORA VDD   3v3
axp.setLDO3Voltage(3300)   # T-Beam GPS  VDD    3v3

show_hello()

isRunning = False
lora = LoRaImpl()
gps = GPS()

def show_hello():
    #oled size: 128 * 64
    oled = SSD1306_I2C(128, 64, i2c)

    oled.fill(0)
    oled.text('Hello', 0, 0, 0xffff)
    oled.text('World !', 0, 10, 0xffff)
    oled.show()


print('---------------------------')
print('     -> hello world <-     ')
print('---------------------------')

longe = 15.15698
latt = -48.15645
batt = 48
lora = LoRaImpl()


message = Message(longe,latt,batt)
lora.connect()
lora.send_message(message)
lora.save()

#When the accelometer receives an value it will trigger this function
#Enables LoRa and GPS module
#Get coords until receives the same value twice
def accel_trigger():
    isRunning = False
    lora = LoRaImpl()
    gps = GPS()
    if(not isRunning):
        axp.enablePower(axp202.AXP192_LDO3)
        axp.enablePower(axp202.AXP192_LDO2)
        isRunning = True
        previousCoords = None
        actualCoords = None

        #lora.connect()
        while True:
            previousCoords = actualCoords
            actualCoords = gps.getCoords()
            #if(previousCoords != None and previousCoords.latitude_string() == actualCoords.latitude_string() and previousCoords.longitude_string() == previousCoords.longitude_string()):
             #   break
            #parse longitude
            #parse latitude
            print('Lat='+actualCoords.latitude_string()+' Lon='+actualCoords.longitude_string())
            #battery = getBattery()
            #message = Message(longitude,latitude,battery)
            #lora.send_message(message)

            time.sleep(3) #Na prática o sleep seria de 8/10 segundos para respeitar o duty cycle
        #lora.save()
        axp.disablePower(axp202.AXP192_LDO3)
        axp.disablePower(axp202.AXP192_LDO2)



print("Battery:")
print("Percentage: " + str(axp.getBattPercentage()))
print("Voltage : " + str(axp.getBattVoltage()))
print("Current charge: " + str(axp.getBattChargeCurrent()))
print("In power: " + str(axp.getBattInpower()))
print("Temperature: " + str(axp.getTemp()))



#accel_trigger()

print('     -> Done! <-     ')

i2c = machine.I2C(0, pins=('G21', 'G22'))
#print('i2c devices ::: ' + str(i2c.scan()))


oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('Hello', 0, 0, 0xffff)
oled.text('World !', 0, 10, 0xffff)
oled.show()


#TODO
#Fazer parse coords string para float
#Problemas das variaveis globais
#Acabar logica aplicacional + dar refactor ao accel_trigger
#Implementar acelerometro