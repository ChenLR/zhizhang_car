import RPi.GPIO as GPIO
from time import sleep 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
p=GPIO.PWM(11,50)
p.start(40)
sleep(5) 
p.start(50)
sleep(5) 
GPIO.cleanup()

