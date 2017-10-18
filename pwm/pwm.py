import wiringpi
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(21,1)
wiringpi.digitalWrite(21,1)
#i=wiringpi.softPwmCreate(21,1,100)
#wiringpi.softPwmWrite(21,50)
try:
    while 1:
        pass
except KeyboardInterrupt:
    pass

