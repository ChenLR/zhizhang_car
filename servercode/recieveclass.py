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

class runtracker(object):
    def __init__(self,size=512,port=6789):
        self.reimg=reciever(size=size,port=port)
        cv2.namedWindow("Image", 1)
        print "Press key `p` to pause the video to start tracking"
        while True:
            # Retrieve an image and Display it.
            self.img=self.reimg.getimage()
            if(cv2.waitKey(10)==ord('p')):
                break
            
            cv2.imshow("Image", self.img)
        cv2.destroyWindow("Image")
        # Co-ordinates of objects to be tracked 
        # will be stored in a list named `points`
        points = get_points.run(self.img) 

        if not points:
            print "ERROR: No object to be tracked."
            exit()
    
        cv2.namedWindow("Image", 1)
        cv2.imshow("Image", self.img)
        # Initial co-ordinates of the object to be tracked 
        # Create the tracker object
        self.tracker = dlib.correlation_tracker()
        # Provide the tracker the initial position of the object
        self.tracker.start_track(self.img, dlib.rectangle(*points[0]))
        print "all inited"
    def run(self):
        cv2.namedWindow("Image", 1)
        print "Press key `p` to pause the video to reinit"
        print "Press key `q`  to quit"
        while True:
            key=cv2.waitKey(20)
            if(key==ord('p')):
                self.reinit()
            if(key==ord('q')):
                break
             
            # Read frame from device or file
            self.img=self.reimg.getimage()
            # Update the tracker  
            self.tracker.update(self.img)
            # Get the position of the object, draw a 
            # bounding box around it and display it.
            rect = self.tracker.get_position()
            self.pt1 = (int(rect.left()), int(rect.top()))
            self.pt2 = (int(rect.right()), int(rect.bottom()))
            cv2.rectangle(self.img, self.pt1, self.pt2, (255, 255, 255), 3)
            print "Object tracked at [{}, {}] \r".format(self.pt1, self.pt2),
            
            cv2.imshow("Image", self.img)
            # Continue until the user presses ESC key
            if cv2.waitKey(1) == 27:
                break
    def reinit(self):
        print "Press key `p` to pause the video to start tracking"
        while True:
            # Retrieve an image and Display it.
            self.img=self.reimg.getimage()
            if(cv2.waitKey(10)==ord('p')):
                break
            cv2.namedWindow("Image", 1)
            cv2.imshow("Image", self.img)
        cv2.destroyWindow("Image")
        # Co-ordinates of objects to be tracked 
        # will be stored in a list named `points`
        points = get_points.run(self.img) 

        if not points:
            print "ERROR: No object to be tracked."
            exit()
    
        cv2.namedWindow("Image", 1)
        cv2.imshow("Image", self.img)
        # Initial co-ordinates of the object to be tracked 
        # Create the tracker object
        self.tracker = dlib.correlation_tracker()
        # Provide the tracker the initial position of the object
        self.tracker.start_track(self.img, dlib.rectangle(*points[0]))
        print "all inited"
    def close(self):
        self.reimg.close()
        cv2.destroyAllWindows()
aa=runtracker()
aa.run()
