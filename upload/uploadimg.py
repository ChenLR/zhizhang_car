import socket
import numpy
from PIL  import Image
import cv2

class uploadimg(object):
    def __init__(self,ip,size=224):
        self.size=size
        self.ip=ip
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.capture = cv2.VideoCapture(0)
        self.encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        self.on=1
    def run(self):
        
        while self.on:
            ret, frame = self.capture.read()
            frame=cv2.resize(frame,(self.size,self.size))
            result, imgencode = cv2.imencode('.jpg', frame, self.encode_param)
            data = numpy.array(imgencode)
            stringData = data.tostring()
            if len(stringData)<65500:
                self.sock.sendto(stringData,(self.ip,6789))
    def close(self):
        self.on=0
        sock.close()

