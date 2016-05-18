import pygame
import twitch_bot_utils
import win32api
import win32gui
import win32con
import time
import random
import argparse
import logging

def check_range(arg):
    try:
        value = int(arg)
    except ValueError as err:
       raise argparse.ArgumentTypeError(str(err))

    if value < 0 or value > 255:
        message = "Expected 0 <= value <= 255, got value = {}".format(value)
        raise argparse.ArgumentTypeError(message)

    return value
    
parser = argparse.ArgumentParser()
parser.add_argument('duration',type=int,nargs='?', help='Duration in seconds to dim the screen')
parser.add_argument('-dim', type=check_range, help='Dim value (0-255) Where 0 is transparant and 255 is opaque')

try:
    options = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

if options.duration is None:
    options.duration = random.randint(30, 60)
if options.dim is None:
    options.dim = 220
    
logging.log(logging.INFO,"Dimming screen: %d for %d seconds" % (options.dim,options.duration))

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
logging.log(logging.INFO,"Monitor %d x %d" %(width,height))

def set_top(hwnd):
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,width,height,win32con.SWP_NOACTIVATE)
    logging.log(logging.DEBUG,"SetWindowPos to HWND_TOPMOST and SWP_NOACTIVATE")
    style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    logging.log(logging.DEBUG,"Got style %X before" % style)
    style = style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST
    logging.log(logging.DEBUG,"Setting style %X" % style)
    win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
    logging.log(logging.DEBUG,"Set style %X" % style)
    style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    logging.log(logging.DEBUG,"Got style %X after" % style)
    
def user_wait(duration):
    stop = time.time()+duration
    while time.time() < stop:
        pygame.event.pump()
        time.sleep(0.5)
        pygame.display.update()
    return

pygame.init()
logging.log(logging.INFO,"Dim scare! %s seconds" % options.duration)
pygame.display.set_mode((width, height), pygame.NOFRAME  , 32)
logging.log(logging.DEBUG,"Looking for window!")

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

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), options.dim, win32con.LWA_ALPHA)
user_wait(options.duration)
logging.log(logging.INFO,"Done!")

