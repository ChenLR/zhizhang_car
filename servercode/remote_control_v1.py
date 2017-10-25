# coding=utf-8
#!/usr/bin/env python
from __future__ import division
import os
import argparse
import warnings
import socket

import cv2
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches
import matplotlib.cbook
warnings.filterwarnings('ignore', category=matplotlib.cbook.mplDeprecation)

def enum(**enums):
    return type('Enum', (), enums)

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
        return str(sp1)+' '+str(sp2)


class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.refresh()

    def on_mouse_move(self, event):
        if not event.inaxes:
            return
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()

    def refresh(self):
        self.lx = self.ax.axhline(color='y')  # the horiz line
        self.ly = self.ax.axvline(color='y')  # the vert line

        # text location in axes coords
        self.txt = self.ax.text(0.7, 0.9, '', color='r', transform=self.ax.transAxes)

class InteractiveViewer(object):
    def __init__(self):
        self.sender = send_instru('101.5.213.220', 31423)
        self.key_pressed = False
        self.key_event = None

        self.fig = None
        self.im_ax = None

        self.is_skipped = False
        self.is_finished = False

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def on_click(self, event):
        print "clicked"
        return


    def on_release(self, event):
        print "released"
        return

    def on_key_press(self, event):
        self.key_event = event
        self.key_pressed = True
        key = self.key_event.key
        if key == 'up':
            self.up = True
        elif key == 'down':
            self.down = True
        elif key == 'left':
            self.left = True
        elif key == 'right':
            self.right = True
        # print "key pressed", self.key_event.key

    def on_key_release(self, event):
        self.key_event = event
        self.key_pressed = False
        key = self.key_event.key
        if key == 'up':
            self.up = False
        elif key == 'down':
            self.down = False
        elif key == 'left':
            self.left = False
        elif key == 'right':
            self.right = False
        # print "key release", self.key_event.key

    def connect(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)

    def button_event(self, event):
        self.key_pressed = False
        print "button clicked"
        return

    def maximize_window(self):
        backend = matplotlib.get_backend()
        if backend == 'TkAgg':
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
        elif backend == 'QT4Agg':
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()


    def init_subplots(self):
        self.fig = plt.figure("annotate")
        self.fig.clear()
        print matplotlib.get_backend()
        # self.maximize_window()

        self.im_ax = self.fig.add_subplot(1, 1, 1)
        self.im_ax.xaxis.set_visible(False)
        self.im_ax.yaxis.set_visible(False)
        self.im_ax.set_title('Input')

    def send_command(self):
        # forward = 1, 0, -1
        # direct = 1, 0, -1
        forward = 0
        direct = 0
        if self.up and not self.down:
            forward = 1
        elif self.down and not self.up:
            forward = -1
        else:
            forward = 0

        if self.left and not self.right:
            direct = 1
        elif self.right and not self.left:
            direct = -1
        else:
            direct = 0

        arr = [[[50, 100], [100, 100], [100, 50]],
                [[-50, 50], [0, 0], [50, -50]],
                [[-50, -100], [-100, -100], [-100, -50]]]

        cmd = arr[1-forward][1-direct]
        left = cmd[0]
        right = cmd[1]

        self.sender.send(left, right)

        

    def run(self):
        self.init_subplots()
        self.connect()

        while True:
            # Wait for output, and 'update' figure
            plt.pause(0.02)
            self.send_command()

            # Exit
            if (self.is_finished or self.is_skipped
                    or (self.key_pressed and self.key_event.key == 'q')
                    ):
                break

        plt.close()

        if self.is_finished:
            return 0 # finished normally
        elif self.is_skipped:
            return 1 # not to save
        else:
            return 2 # aborted (pressed 'q')

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Annotate face images. Output to file.')
    args = parser.parse_args()
    return args


def main(args):
    # img_list = open(args.img_list, "r").read().splitlines()
    viewer = InteractiveViewer()
    status =  viewer.run()
    return


if __name__ == '__main__':
    main(parse_arguments())
