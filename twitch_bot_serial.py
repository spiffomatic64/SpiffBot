import pygame.time
import serial
import serial.tools.list_ports
import twitch_bot_utils
import time


class twitch_serial:

    def __init__(self,port,speed):
        self.Enabled = False
        ports = serial.tools.list_ports.comports()
        for p in ports:
            print "Checking %s..." % p.device
            try:
                ser = serial.Serial(p.device, 115200,timeout=1)
                time.sleep(1)
                ser.flushInput()
                line = ser.readline()
                if len(line)>0:
                    if line == "Arduino Starting...\r\n":
                        print "Got it! %s" % p.device
                        port = p.device
                        self.Enabled = True
            except serial.SerialException: 
                print "nope"
                self.Enabled = False
        if self.Enabled:
            self.ser = ser
        self.writing = False
        twitch_bot_utils.printer("Opened Serial Port: %s Speed: %s" % (port,speed))

    def wait(self):
        while self.writing==1:
            pygame.time.wait(10)

    def write(self,input):
        self.wait()
        self.writing = True
        if self.Enabled:
            try:
                self.ser.write(input)
            except:
                return False
        self.writing = False
        return True
    def flushInput(self):
        self.wait()
        self.writing = True
        if self.Enabled:
            self.ser.flushInput()
        self.writing = False
        
    #get current pixel colors and return into a list of lists
    def get_pixels(self):
        pixels = {}
        self.flushInput()
        self.write("#000%c0" % chr(252))
        self.wait()
        self.writing = True
        
        if self.Enabled:
            for x in range( 0, 30 ):
                line = self.ser.readline().split(",")
                pixels.update( {line[0] : [ int(line[1]),int(line[2]),int(line[3]) ] } )
        self.writing = False
        return pixels