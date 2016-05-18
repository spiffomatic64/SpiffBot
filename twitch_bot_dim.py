import pygame
import twitch_bot_utils
import win32api
import win32gui
import win32con
import time
import random

times = random.randint(30, 60)
width = 1920
height = 1080

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
    
def user_wait(duration):
    stop = time.time()+duration
    while time.time() < stop:
        pygame.event.pump()
        time.sleep(0.5)
        pygame.display.update()
    return

pygame.init()
logging.log(logging.INFO,"Dim scare! %s seconds" % times)
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

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 220, win32con.LWA_ALPHA)
user_wait(times)
logging.log(logging.INFO,"Done!")

