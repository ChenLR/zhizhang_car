import socket
import Image
import os,sys,pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((140,140))
pygame.display.set_caption("web cam")

pygame.display.flip()
svrsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
svrsocket.bind(("0.0.0.0",6789 ))
clock = pygame.time.Clock()
while 1:
    data, address = svrsocket.recvfrom(60000)
    camshot = pygame.image.frombuffer(data, (140,140), "RGB")
    for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    screen.blit(camshot, (0,0))
    pygame.display.update() 
    print clock.get_fps()
    clock.tick()
