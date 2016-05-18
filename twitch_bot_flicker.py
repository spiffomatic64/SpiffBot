import pygame
import twitch_bot_utils
import win32api
import win32gui
import win32con
import time
import random


if len(sys.argv)==2 and sys.argv[1].isdigit():
    start = int(sys.argv[1])
    end = int(sys.argv[1])
elif len(sys.argv)==3 and sys.argv[1].isdigit() and sys.argv[2].isdigit():
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    
logging.log(logging.INFO,"Time randomly: %d-%d" % (start, end))

times = random.randint(start, end)

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
logging.log(logging.INFO,"Monitor %d x %d" %(width,height))

#WS_EX_LAYERED 0x00080000
#WS_EX_TOPMOST 0x00000008L
#WS_EX_TRANSPARENT 0x00000020L
#0x00080028

frames = random.randint(10, 30)
visible = (1.0 / 60.0) * frames
frames = 30
black = (1.0 / 60.0) * frames


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

pygame.init()
logging.log(logging.INFO,"Flicker scare! %s times" % times)
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
for i in range(0,times):
    logging.log(logging.DEBUG,"Flicker off")
    pygame.display.set_mode((width, height), pygame.NOFRAME  , 32)
    set_top(hwnd)
    time.sleep(black)
    
    logging.log(logging.DEBUG,"Flicker on")
    pygame.display.set_mode((1, 1), pygame.NOFRAME  , 32)
    logging.log(logging.DEBUG,"Showing %f frames" % visible)
    
    time.sleep(visible)

