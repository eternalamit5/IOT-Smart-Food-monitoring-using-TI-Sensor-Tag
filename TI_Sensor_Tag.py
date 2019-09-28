

from __future__ import print_function
import pygatt
import time

def humConvert(rawTemp, rawHum):
    temp = (float(rawTemp) / 65536) * 165 - 40
    hum = (float(rawHum) / 65536) * 100
    return [temp, hum]

MAC = "98:07:2D:27:A7:81"
adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    print ("Connecting to {}".format(MAC))
    device = adapter.connect(MAC)
    print ("Connected. Enabling sensors")
    device.char_write('f000aa22-0451-4000-b000-000000000000', bytearray([0x01])) # enabling Humidity sensor
    print ("Sensors enabled. Starting measurements")
    time.sleep(2)
    print ("\n")
    while True:
        valueHum = device.char_read('f000aa21-0451-4000-b000-000000000000') # Reading Humidity value
        bytes = []
        for x in valueHum: bytes.append("{:02x}".format(x))
        rawTemp = int ('0x' + bytes[1] + bytes[0], 16)
        rawHum = int ('0x' + bytes[3] + bytes[2], 16)
        resultsHum = humConvert(rawTemp, rawHum)
        print ("Temperature: {:<5.1f} Humidity: {:<5.1f}".format(resultsHum[0], resultsHum[1]))
        time.sleep(1)
finally:
    adapter.stop()
