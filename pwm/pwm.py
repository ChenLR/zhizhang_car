import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARO)
GPIO.setup(11,GPIO.OUT)
p=GPIO.PWM(11,50)
p.start(50)
p.stop()
GPIO.cleanup()

