import machine
import time
import ubinascii
import socket
from message import Message
from network import LoRa

class LoRaImpl():
    #Constructor, creates the LoRa and socket objects, as well declares the communication keys

    def __init__(self):
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

        self.app_eui = ubinascii.unhexlify('0000000000000000')
        self.app_key = ubinascii.unhexlify('95D1C04E0C407C2AAC755CCCB273E99E')
        self.dev_eui = ubinascii.unhexlify('70B3D57ED005D8DE')
        
        # create a LoRa socket
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        # set the LoRaWAN data rate
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

    #Creates an connect between the LoRa gateway and the device
    #If the device already had a connection, it will be restored
    def connect(self):
        self.lora.nvram_restore()
        if(not self.lora.has_joined()):
            self.lora.join(activation=LoRa.OTAA, auth=(self.dev_eui, self.app_eui, self.app_key), timeout=0)
            print("Made a new connection")
        else:
            print("Connection reloaded")

        while not self.lora.has_joined():
            time.sleep(2.5)
            print('Not yet joined...')

    #Saves the current LoRa connection
    def save(self):
        self.lora.nvram_save()

    #Sends an message to a LoRa gateway
    def send_message(self,message: Message):
        if(not self.lora.has_joined()):
            self.connect()

        data_long = bytearray(struct.pack(">f", message.longitude))
        data_lat = bytearray(struct.pack(">f", message.latitude))
        data_batt = message.battery.to_bytes(2, 'little')

        print("Long: " + str(data_long))
        print("latt: " + str(data_lat))
        print("batt: " + str(data_batt))

        message_bytes = data_long + data_lat + data_batt

        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        self.s.setblocking(True)

        # send some data
        self.s.send(message_bytes)
        print("Message sent")
        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        self.s.setblocking(False)

    
    

   