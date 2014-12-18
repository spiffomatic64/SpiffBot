import pygame.time
import serial
import twitch_bot_utils


class twitch_serial:

    def __init__(self,port,speed):
        #todo: add arduino detection here
        self.ser = serial.Serial(port, speed)
        self.writing = False
        twitch_bot_utils.printer("Opened Serial Port: %s Speed: %s" % (port,speed))

    def wait(self):
        while self.writing==1:
            pygame.time.wait(10)

    def write(self,input):
        self.wait()
        self.writing = True
        try:
            self.ser.write(input)
        except:
            return False
        self.writing = False
        return True
    def flushInput(self):
        self.wait()
        self.writing = True
        self.ser.flushInput()
        self.writing = False
        
    #get current pixel colors and return into a list of lists
    def get_pixels(self):
        pixels = {}
        self.flushInput()
        self.write("#000%c0" % chr(252))
        self.wait()
        self.writing = True
        for x in range( 0, 30 ):
            line = self.ser.readline().split(",")
            pixels.update( {line[0] : [ int(line[1]),int(line[2]),int(line[3]) ] } )
        self.writing = False
        return pixels