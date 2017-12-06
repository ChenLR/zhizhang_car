# -*- coding: utf-8 -*
import serial
import time
# 打开串口
ser = serial.Serial("/dev/ttyAMA0", 9600,timeout=0.5)
print ser.name 
time.sleep(5)
ser.write('6.8,7.4') 
time.sleep(5)
ser.write('7.2,6.4') 
time.sleep(5)
ser.close()

