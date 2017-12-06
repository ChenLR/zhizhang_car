import socket
import Image
import os,sys,pygame
from pygame.locals import *
import cv2
import numpy
import dlib
import cv2
import argparse as ap
import get_points
import numpy as np
def mytanh(x,scale=20,gama=5):
    gama=gama/scale
    x=x/scale
    if x<-gama:
        #return (np.exp(x+gama)-np.exp(-x-gama))/(np.exp(x+gama)+np.exp(-x-gama))
        return 
    elif  -gama<=x<=gama:
        return 0
    else:
        return (np.exp(x-gama)-np.exp(-x+gama))/(np.exp(x-gama)+np.exp(-x+gama))

def myfun(x,gama=30,scale=2):
    x=x*scale
    if x<-gama:
        return max(x+gama,-100)
    elif  -gama<=x<=gama:
        return 0
    else:
        return min(100,x-gama)

class reciever(object):
    def __init__(self,size=512,port=6789):
        self.size=size
        self.port=port
        self.svrsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.svrsocket.bind(("0.0.0.0",self.port))
    def getimage(self):
        data, address = self.svrsocket.recvfrom(60000)
        data = numpy.fromstring(data, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        #print decimg.shape
        return decimg
    def close(self):
        self.svrsocket.close()
        
class send_instru(object):
    def __init__(self,ip,port):
        self.address=(ip,port)
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def send(self,sp1,sp2):
        msg = self.sp_tomsg(sp1,sp2)
        self.sock.sendto(msg,self.address)
    def close(self):
        self.sock.close()
    def sp_tomsg(self,sp1,sp2):
        print sp1,sp2
        return str(sp1)+' '+str(sp2)+' '+'0 '+'0'

class contral_by_point(object):
    def __init__(self,ip):
        self.sender=send_instru(ip, 31423)
    def set_initpoint(self,point1,point2):
        self.pt1=point1
        self.pt2=point2
        self.ct=(point1[0]+point2[0])/2
        print self.ct
        self.ct1=(point2[0]-point1[0])
    def sendcon(self,point1,point2):
        speed1=-myfun((point2[0]-point1[0])-self.ct1,gama=1,scale=3)
  
        #print speed1,(point2[0]-point1[0]),self.ct1
        speed2=speed1+myfun(self.ct-(point1[0]+point2[0])/2,gama=10,scale=1)
        #print speed1,speed2
        offset1=max(speed1,speed2,100)-100
        offset2=min(speed1,speed2,-100)+100
        speed1=int(speed1-offset1-offset2)
        speed2=int(speed2-offset1-offset2)
        self.sender.send(speed1,speed2)
class runtracker(object):
    def __init__(self,ip,size=224,port=6789):
        self.reimg=reciever(size=size,port=port)
        self.contraler=contral_by_point(ip=ip)
        self.sender1=send_instru(ip, 31423)
        self.on=0
        cv2.namedWindow("Image", 0)
        print "Press key `p` to pause the video to start tracking"
        while True:
            # Retrieve an image and Display it.
            self.img=self.reimg.getimage()
            if(cv2.waitKey(10)==ord('p')):
                break
            
            cv2.imshow("Image", self.img)
        # Co-ordinates of objects to be tracked 
        # will be stored in a list named `points`
        points = get_points.run(self.img) 
        self.contraler.set_initpoint((points[0][0],points[0][1]),(points[0][2],points[0][3]))
        if not points:
            print "ERROR: No object to be tracked."
            exit()
 
        cv2.imshow("Image", self.img)
        # Initial co-ordinates of the object to be tracked 
        # Create the tracker object
        self.tracker = dlib.correlation_tracker()
        # Provide the tracker the initial position of the object
        self.tracker.start_track(self.img, dlib.rectangle(*points[0]))
        print "all inited"
    def run(self):
        cv2.namedWindow("Image",0)
        print "Press key `p` to pause the video to reinit"
        print "Press key `esc`  to quit"
        while True:
             
            # Read frame from device or file
            self.img=self.reimg.getimage()
            # Update the tracker  
            self.tracker.update(self.img)
            # Get the position of the object, draw a 
            # bounding box around it and display it.
            rect = self.tracker.get_position()
            self.pt1 = (int(rect.left()), int(rect.top()))
            self.pt2 = (int(rect.right()), int(rect.bottom()))
            if self.on:
                self.contraler.sendcon(self.pt1,self.pt2)
            cv2.rectangle(self.img, self.pt1, self.pt2, (255, 255, 255), 3)
            #print "Object tracked at [{}, {}] \r".format(self.pt1, self.pt2),
            
            cv2.imshow("Image", self.img)
            key=cv2.waitKey(1)
            if(key==ord('p')):
                self.reinit()
            # Continue until the user presses ESC key
            if key == 27:
                break

    def reinit(self):
        self.sender1.send(0,0)
        print "Press key `p` to pause the video to start tracking"
        while True:
            # Retrieve an image and Display it.
            self.img=self.reimg.getimage()
            if(cv2.waitKey(10)==ord('p')):
                break
            cv2.namedWindow("Image", 0)
            cv2.imshow("Image", self.img)
        # Co-ordinates of objects to be tracked 
        # will be stored in a list named `points`
        points = get_points.run(self.img) 
        self.contraler.set_initpoint((points[0][0],points[0][1]),(points[0][2],points[0][3]))
        if not points:
            print "ERROR: No object to be tracked."
            exit()
    
        cv2.imshow("Image", self.img)
        # Initial co-ordinates of the object to be tracked 
        # Create the tracker object
        self.tracker = dlib.correlation_tracker()
        # Provide the tracker the initial position of the object
        self.tracker.start_track(self.img, dlib.rectangle(*points[0]))
        print "reinited"

    def close(self):
        self.reimg.close()
        cv2.destroyAllWindows()
#aa=runtracker()
#aa.run()
