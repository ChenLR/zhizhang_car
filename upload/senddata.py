import socket
import numpy
import Image
import cv2

address = ('101.5.210.125', 8002)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(address)

capture = cv2.VideoCapture(1)
while 1:
    ret, img = capture.read()
    im = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    im=im.resize((640,640))
    stringData = im.tobytes()
    sock.send( str(len(stringData)).ljust(16))
    sock.send( stringData )
sock.close()

