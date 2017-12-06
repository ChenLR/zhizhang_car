import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
from run_func import SteCon
k=SteCon()
sleep(50)
k.run(45,45)
sleep(5)
k.cleanup()
