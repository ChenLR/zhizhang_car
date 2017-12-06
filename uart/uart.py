# -*- coding: utf-8 -*
import serial
import time
# 打开串口
ser = serial.Serial("/dev/ttyAMA0", 9600)
print ser.name 
try:
    while True:
        ser.write('s8.8,8.4e') 
        time.sleep(0.1)
except KeyboardInterrupt:
    if ser != None:
        ser.close()

