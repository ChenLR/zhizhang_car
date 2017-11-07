import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
class SteCon(object):
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)# choose BCM or BOARD 
        GPIO.setup(12, GPIO.OUT)# set GPIO12 as an output  left and right
        GPIO.setup(16, GPIO.OUT)# set GPIO16 as an output  top and bottom  
        
        self.lr=0.0
        self.tb=0.0
        self.lr_center = 6.8
        self.tb_center = 7.5
        self.lr_scale = - 4.0/90.0
        self.tb_scale = - 4.0/90.0
        self.lr_min = -45.0
        self.lr_max = 45.0
        self.tb_min = -5.0
        self.tb_max = 90.0
        self.lr_pwm=GPIO.PWM(12,50)
        self.tb_pwm=GPIO.PWM(16,50)
        self.lr_pwm.start(self.lr_center)  #6 mid
        self.tb_pwm.start(self.tb_center)  #5.5 mid

    def run(self,lr,tb):   #0~90
        self.lr=lr
        self.tb=tb
        self.lr = max(self.lr, self.lr_min)
        self.lr = min(self.lr, self.lr_max)
        self.tb = max(self.tb, self.tb_min)
        self.tb = min(self.tb, self.tb_max)
        self.lr_pwm.ChangeDutyCycle(self.lr_center + self.lr * self.lr_scale)
        self.tb_pwm.ChangeDutyCycle(self.tb_center + self.tb * self.tb_scale)

    def cleanup(self):
        self.lr_pwm.stop()
        self.tb_pwm.stop()
        GPIO.cleanup()
