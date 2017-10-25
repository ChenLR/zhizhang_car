import socket 
class send_instru(object):
    def __init__(self,ip,port):
        self.address=(ip,port)
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def send(self,msg):
        self.sock.sendto(msg,self.address)
    def close(self):
        self.sock.close()
def sp_tomsg(sp1,sp2):
    return str(sp1)+' '+str(sp2)
    
send = send_instru('101.5.213.220', 31423)  
send.send(sp_tomsg(-20,30))
