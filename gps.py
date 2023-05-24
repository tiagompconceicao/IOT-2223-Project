import axp202
import machine
import time
from micropyGPS import MicropyGPS


class GPS():
    def __init__(self):
        GPS_TX_PIN = 'G12'
        GPS_RX_PIN = 'G34'
        self.uart = machine.UART(1, baudrate=9600,pins=(GPS_TX_PIN,GPS_RX_PIN))
        self.my_gps = MicropyGPS(location_formatting='dd')

    def getCoords(self):
        attempt = 1
        while attempt < 10:
            print("Attempt: " + str(attempt))
            attempt += 1
            if(self.uart.any()):
                sentence=self.uart.readline()
                if sentence!=None:
                    for element in range(0, len(sentence)):
                        self.my_gps.update(chr(sentence[element]))
                    return self.my_gps
            time.sleep(1)
        return None