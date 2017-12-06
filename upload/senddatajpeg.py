import socket
import numpy
from PIL  import Image
import cv2


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


capture = cv2.VideoCapture(0)
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
while 1:
    ret, frame = capture.read()
    frame=cv2.resize(frame,(224,224))
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    if len(stringData)<65500:
        sock.sendto(stringData,("101.5.210.160",6789) )
sock.close()

