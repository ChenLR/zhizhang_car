import socket  
class get_instru(object):
    def __init__(self,ip,port):
        self.address=(ip,port)
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)
    def getin(self):
        data,addr=self.sock.recvfrom(1024)
        return data
    def close(self):
        self.sock.close()
'''
k=get_instru('0.0.0.0',31423)
'''
def msg_tosp(msg):
    print msg
    sps = [int(item) for item in msg.split()]
    return sps
'''
while 1:
    print msg_tosp(k.getin())
    print 'heihei'
'''
