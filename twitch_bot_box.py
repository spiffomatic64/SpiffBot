import pygame
import twitch_bot_utils
import win32api
import win32gui
import win32con
import time
import random
import sys
import logging
import argparse

    
parser = argparse.ArgumentParser()
parser.add_argument('times',type=int, nargs='?',default=random.randint(30, 60), help='Times to flicker the screen')

try:
    options = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

times = options.times

logging.log(logging.INFO,"Drawing box for %d seconds" % times)
    
    
width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
logging.log(logging.INFO,"Monitor %d x %d" %(width,height))
low = 20
high = 40

w = random.randint(int(width * (low / 100.0)), int(width * (high / 100.0)))
h = random.randint(int(height * (low / 100.0)), int(height * (high / 100.0)))
logging.log(logging.INFO,"Box size %d x %d" %(w,h))

x = random.randint(0, width - w)
y = random.randint(0, height - h)
logging.log(logging.INFO,"Box position %d x %d" %(x,y))


#TODO turn into function
def set_top(hwnd):
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,x,y,w,h,win32con.SWP_NOACTIVATE)
    logging.log(logging.DEBUG,"SetWindowPos to HWND_TOPMOST and SWP_NOACTIVATE")
    
    style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    logging.log(logging.DEBUG,"Got style %X before" % style)
    
    style = style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST
    win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
    logging.log(logging.DEBUG,"Setting style %X" % style)
    
    style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    logging.log(logging.DEBUG,"Got style %X after" % style)

#TODO turn into function    


pygame.init()
logging.log(logging.INFO,"BOX scare! %s seconds" % times)
pygame.display.set_mode((w, h), pygame.NOFRAME  , 32)
logging.log(logging.DEBUG,"Looking for window!")

#TODO turn into function
while True:
    time.sleep(0.001)
    try:
        hwnd = win32gui.FindWindow(None,"pygame window")
        if hwnd:
            logging.log(logging.DEBUG,"Found window! hwnd: %s" % hwnd)
            set_top(hwnd)
            break
    except win32gui.error:
        logging.log(logging.ERROR,"Error: window not found")

twitch_bot_utils.pygame_user_wait(times)
logging.log(logging.INFO,"Done!")

