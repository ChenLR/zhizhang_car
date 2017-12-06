from upload import uploadimg
from car_run import run_func
from car_run import rec_instru
import socket
class car666(object):
    def __init__(self):
        print 'initing ....'
        sock1= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock1.bind(('0.0.0.0',31424))
        ipdata,_=sock1.recvfrom(1024)
        self.serverip=ipdata.split()[1]
        print 'serverip:',self.serverip
        sock1.close()
        address=(self.serverip,31424)
        sock2=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock2.sendto('laosiji666',address)
        sock2.close()
        print 'init network'
        self.upimg=uploadimg.uploadimg(self.serverip)
        self.car=run_func.CarControl()
        self.getins=rec_instru.get_instru('0.0.0.0',31423)
    def run(self):
        self.upimg.run()
        try:
            while 1:
                sps=rec_instru.msg_topsp(self.getins())
                print sps
                self.car.car_run(sps[0],sps[1])
                self.car.cam_run(sps[3],sps[2])
        except:
            self.car.cleanup()
    
car_to_you_er_yuan=car666()
car_to_you_er_yuan.run()

