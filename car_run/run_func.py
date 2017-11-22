import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
class CarControl(object):
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)# choose BCM or BOARD 
        # motor control
        GPIO.setup(35, GPIO.OUT)# set GPIO11 as an output  left+ 
        GPIO.setup(36, GPIO.OUT)# set GPIO11 as an output  left-  
        GPIO.setup(37, GPIO.OUT)# set GPIO11 as an output  right+ 
        GPIO.setup(38, GPIO.OUT)# set GPIO11 as an output  right- 
        self.left=0
        self.right=0
        self.l1=GPIO.PWM(35,50)
        self.l2=GPIO.PWM(36,50)
        self.r1=GPIO.PWM(37,50)
        self.r2=GPIO.PWM(38,50)
        self.l1.start(0)
        self.l2.start(0)
        self.r1.start(0)
        self.r2.start(0)

        # camera control
        GPIO.setup(12, GPIO.OUT)# set GPIO12 as an output  left and right
        GPIO.setup(16, GPIO.OUT)# set GPIO16 as an output  top and bottom  
        self.lr=0.0
        self.tb=0.0
        self.lr_center = 6.2
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
        self.cam_run(0, 0)


    def car_run(self,left,right):   #-100~100
        self.left=left
        self.right=right

        if self.left>0 and self.left<101:
            self.l1.ChangeDutyCycle(self.left)
            self.l2.ChangeDutyCycle(0)
        elif self.left<0 and self.left>-101:
            self.l1.ChangeDutyCycle(0)
            self.l2.ChangeDutyCycle(-self.left)
        elif self.left==0:
            self.l1.ChangeDutyCycle(0)
            self.l2.ChangeDutyCycle(0)
        else:
            self.l1.ChangeDutyCycle(0)
            self.l2.ChangeDutyCycle(0)
            print('out of range')

        if self.right>0 and self.right<101:
            self.r1.ChangeDutyCycle(self.right)
            self.r2.ChangeDutyCycle(0)
        elif self.right<0 and self.right>-101:
            self.r1.ChangeDutyCycle(0)
            self.r2.ChangeDutyCycle(-self.right)
        elif self.right==0:
            self.r1.ChangeDutyCycle(0)
            self.r2.ChangeDutyCycle(0)
        else:
            self.r1.ChangeDutyCycle(0)
            self.r2.ChangeDutyCycle(0)
            print('out of range')

    def cam_run(self,lr,tb):   #0~90
        self.lr=lr
        self.tb=tb
        self.lr = max(self.lr, self.lr_min)
        self.lr = min(self.lr, self.lr_max)
        self.tb = max(self.tb, self.tb_min)
        self.tb = min(self.tb, self.tb_max)
        self.lr_pwm.ChangeDutyCycle(self.lr_center + self.lr * self.lr_scale)
        self.tb_pwm.ChangeDutyCycle(self.tb_center + self.tb * self.tb_scale)

    def cleanup(self):
        # motor
        self.l1.stop()
        self.l2.stop()
        self.r1.stop()
        self.r2.stop()
        # camera
        self.lr_pwm.stop()
        self.tb_pwm.stop()
        GPIO.cleanup()
