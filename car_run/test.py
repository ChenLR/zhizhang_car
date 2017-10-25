import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
from run_func import CarControl
from rec_instru import *
k=CarControl()
f=get_instru('0.0.0.0',31423)
try:
    while 1:
        sp1,sp2=msg_tosp(f.getin())
        print sp1,sp2
        k.run(sp1,sp2)
except:
    k.cleanup()
