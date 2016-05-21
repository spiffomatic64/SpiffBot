#! python2

import win32api
import time
import random
import argparse
import logging
import sys

#constants
import ctypes

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))

class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)
    
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
    
def Input(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(INPUT_HARDWARE, _INPUTunion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')
    
def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))
    
WHEEL_DELTA = 120
XBUTTON1 = 0x0001
XBUTTON2 = 0x0002
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)
    
    
parser = argparse.ArgumentParser()
parser.add_argument('duration',type=int, nargs='?',default=random.randint(30, 60), help='Duration to move mouse around')

try:
    options = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

length = options.duration
logging.log(logging.INFO,"Drunk for %d seconds!" % length)

max = 7
    
sx = 0.2
sy = 0.1

state = 1
xm = 0

yl = 2
yr = 5
sizey = random.randint(yl, yr)
ym = sizey

stop = time.time()+length
while time.time() < stop:
    
    x, y = win32api.GetCursorPos()
    #0,10
    if xm > max:
        xm = max
    if xm < -max:
        xm = -max
    if state == 1:
        xm -= sx
        ym -= sy
        if ym <=0 :
            state = 2
            logging.log(logging.DEBUG,"STATE %d!" % state)
            sizey = random.randint(yl, yr)
    #-10,0
    elif state == 2:
        xm += sx
        ym -= sy
        if ym <=-sizey:
            state = 3
            logging.log(logging.DEBUG,"STATE %d!" % state)
            sizey = random.randint(yl, yr)
    #0,-10
    elif state == 3:
        #xm = xm + sx
        ym += sy
        if ym >= sizey:
            state = 4
            logging.log(logging.DEBUG,"STATE %d!" % state)
            sizey = random.randint(yl, yr)
    #0,10
    elif state == 4:
        xm += sx
        ym -= sy
        if ym <= 0:
            state = 5
            logging.log(logging.DEBUG,"STATE %d!" % state)
            sizey = random.randint(yl, yr)
    #10,0
    elif state == 5:
        xm -= sx
        ym -= sy
        if ym <= -sizey:
            state = 6
            logging.log(logging.DEBUG,"STATE %d!" % state)
            sizey = random.randint(yl, yr)
    #0,-10
    elif state == 6:
        #xm = xm - sx
        ym += sy
        if ym >= sizey:
            state = 1
            logging.log(logging.DEBUG,"STATE %d!" % state)
            sizey = random.randint(yl, yr)
    #0,-10

    
    #win32api.SetCursorPos((x+xm,y+ym))
    data = Mouse(MOUSEEVENTF_MOVE,int(xm),int(ym),0)
    SendInput(data)
    #print "x: %d y: %d xm: %d ym: %d" % (x,y,xm,ym)
    time.sleep(0.02)