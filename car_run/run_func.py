import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
class CarControl(object):
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)# choose BCM or BOARD 
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
    def push(self):
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
    def run(self,left,right):   #-100~100
        self.left=left
        self.right=right
        self.push()
    def cleanup(self):
        self.l1.stop()
        self.l2.stop()
        self.r1.stop()
        self.r2.stop()
        GPIO.cleanup()
