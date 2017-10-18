import socket
import numpy
from PIL  import Image
import cv2


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


capture = cv2.VideoCapture(0)
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
while 1:
    ret, frame = capture.read()
    frame=cv2.resize(frame,(140,140))
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    sock.sendto(stringData,("101.5.210.125",6789) )
sock.close()

