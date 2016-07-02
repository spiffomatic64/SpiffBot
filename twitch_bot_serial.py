#! python2

import serial
import serial.tools.list_ports
import time
import logging


class twitch_serial:

    def __init__(self,speed):
        self.Enabled = False
        ports = serial.tools.list_ports.comports()
        for p in ports:
            logging.log(logging.INFO,"Checking %s..." % p.device)
            try:
                ser = serial.Serial(p.device, speed,timeout=1)
                time.sleep(1)
                ser.flushInput()
                line = ser.readline()
                if len(line)>0:
                    if line == "Arduino Starting...\r\n":
                        logging.log(logging.DEBUG, "Got it! %s" % p.device)
                        ser.flushInput()
                        ready = ser.readline()
                        logging.log(logging.INFO, "Readline1: %s" % ready)
                        ready = ser.readline()
                        logging.log(logging.INFO, "Readline2: %s" % ready)
                        ready = ser.readline()
                        logging.log(logging.INFO, "Readline3: %s" % ready)
                        ready = ser.readline()
                        logging.log(logging.INFO, "Readline4: %s" % ready)
                        port = p.device
                        self.Enabled = True
            except serial.SerialException: 
                logging.log(logging.ERROR, "nope")
                self.Enabled = False
        if self.Enabled:
            self.ser = ser
        self.writing = False
        if port:
            logging.log(logging.INFO,"Opened Serial Port: %s Speed: %s" % (port,speed))
        else:
            logging.log(logging.INFO, "Could not find arduino using speed: %d", speed)

    def wait(self):
        while self.writing==1:
            time.sleep(0.001)

    def write(self,input):
        self.wait()
        self.writing = True
        if self.Enabled:
            try:
                self.ser.write(input)
            except:
                logging.log(logging.ERROR,"FAILED TO WRITE!")
                return False
        self.writing = False
        return True
    def flushInput(self):
        self.wait()
        self.writing = True
        if self.Enabled:
            self.ser.reset_input_buffer()
        self.writing = False
        
    #get current pixel colors and return into a list of lists
    def get_pixels(self):
        pixels = {}
        self.flushInput()
        self.write("#000%c0" % chr(252))
        logging.log(logging.INFO, "WriteLine: #000%c" % 252)
        self.wait()
        self.writing = True
        line = self.ser.readline()
        logging.log(logging.INFO, "Readline: %s" % line)

        if self.Enabled:
            for x in range( 0, 30 ):
                line = self.ser.readline()
                logging.log(logging.INFO, "Readline: %d %s" % (x,line))
                line = line.split(",")
                pixels.update( {line[0] : [ int(line[1]),int(line[2]),int(line[3]) ] } )
        self.writing = False
        return pixels