import pygame
import twitch_bot_utils
import win32api
import win32gui
import win32con
import time
import random

times = random.randint(30, 60)
width = 1280
height = 1024
low = 20
high = 40
w = random.randint(int(width * (low / 100.0)), int(width * (high / 100.0)))
h = random.randint(int(height * (low / 100.0)), int(height * (high / 100.0)))
x = random.randint(0, width - w)
y = random.randint(0, height - h)

frames = random.randint(10, 30)
visible = (1.0 / 60.0) * frames
frames = 30
black = (1.0 / 60.0) * frames


def set_top(hwnd):
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,x,y,w,h,win32con.SWP_NOACTIVATE)
    twitch_bot_utils.printer("SetWindowPos to HWND_TOPMOST and SWP_NOACTIVATE")
    style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    twitch_bot_utils.printer("Got style %X before" % style)
    style = style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST
    twitch_bot_utils.printer("Setting style %X" % style)
    win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
    twitch_bot_utils.printer("Set style %X" % style)
    style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    twitch_bot_utils.printer("Got style %X after" % style)
    
def user_wait(duration):
    stop = time.time()+duration
    while time.time() < stop:
        time.sleep(0.5)
        pygame.display.set_mode((w, h), pygame.NOFRAME  , 32)
    return

pygame.init()
twitch_bot_utils.printer("Dim scare! %s seconds" % times)
pygame.display.set_mode((w, h), pygame.NOFRAME  , 32)
twitch_bot_utils.printer("Looking for window!")

while True:
    time.sleep(0.001)
    try:
        hwnd = win32gui.FindWindow(None,"pygame window")
        if hwnd:
            twitch_bot_utils.printer("Found window! hwnd: %s" % hwnd)
            set_top(hwnd)
            break
    except win32gui.error:
        twitch_bot_utils.printer("Error: window not found")

user_wait(times)
twitch_bot_utils.printer("Done!")

