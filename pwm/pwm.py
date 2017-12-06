import RPi.GPIO as GPIO
from time import sleep 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10,GPIO.OUT)
p=GPIO.PWM(10,50)
p.start(40)
sleep(5) 
p.start(50)
sleep(50) 
GPIO.cleanup()

