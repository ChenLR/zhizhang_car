import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BOARD)             # choose BCM or BOARD  
GPIO.setup(11, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(12, GPIO.OUT)  
   
 
GPIO.output(11, 1) 
GPIO.output(12, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
sleep(5)                 # wait half a second  
GPIO.output(11, 0)  
GPIO.output(12, 1)        # set GPIO24 to 0/GPIO.LOW/False  
sleep(5)                 # wait half a second  
GPIO.output(11, 1)  
GPIO.output(12, 1) 
sleep(5)    
GPIO.cleanup()  
