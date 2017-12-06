import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
from run_func import CarControl
from rec_instru import *
car=CarControl()
f=get_instru('0.0.0.0',31423)
try:
    while 1:
        sps=msg_tosp(f.getin())
        print sps
        car.car_run(sps[0],sps[1])
        car.cam_run(sps[3], sps[2])#-45~45   0~90
except:
    car.cleanup()
