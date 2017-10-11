
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 1000)
p.start(50)

try:
    while 1:
        pass
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()


