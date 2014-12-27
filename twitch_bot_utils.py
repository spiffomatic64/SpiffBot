import logging
import datetime
import time
import html_colors
import random
import pygame
import threading
import socket
import string

class irc_connection:
    
    def __init__(self,network,port,bot,oauth,streamer,msg_parsers=[],irc_parsers=[]):
        #IRC connect
        network = 'irc.twitch.tv'
        port = 6667
        self.conn = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.conn.connect ( ( network, port ) )
        printer("connected")
        #IRC auth
        self.conn.send("PASS oauth:%s\r\n" % oauth)
        self.bot = bot
        self.conn.send("NICK %s\r\n" % self.bot)
        self.conn.send("USER %s %s %s :Python IRC\r\n" % (self.bot,self.bot,self.bot))
        #wait before reading data (needed for twitch)
        time.sleep(0.5)
        printer(self.conn.recv ( 4096 ))
        printer("Got stuff")
        #wait before joining (needed for twitch)
        time.sleep(0.5)
        self.streamer = streamer
        self.conn.send("JOIN #%s\r\n" % self.streamer)
        self.msg_parsers = msg_parsers
        self.irc_parsers = irc_parsers
        t = threading.Thread(target=self.irc_thread)
        t.daemon = True
        t.start()
    
    def send(self,msg):   
        self.conn.send ( msg )  
        
    def recv(self,buf_size):   
        return self.conn.recv ( buf_size )  
    
    def msg(self,msg):   
        printer('PRIVMSG #%s :%s\r\n' % (self.streamer,msg))
        self.conn.send ( 'PRIVMSG #%s :%s\r\n' % (self.streamer,msg.encode('utf-8')) )  
        
    def add_msgParser(msg_parser):
        self.msg_parsers.append(msg_parser)
        
    def add_ircPasers(irc_parser):
        self.irc_parsers.append(irc_parser)
        
    def irc_thread(self):
        printer("Started irc_thread")
        while True:
            orig = self.conn.recv ( 4096 ) #receive irc data
        
            if orig.find ( 'PING' ) != -1: #Needed to keep connected to IRC, without this, twitch will disconnect
                self.conn.send ( 'PONG ' + orig.split() [ 1 ] + '\r\n' )
                
            lines = orig.splitlines()
            for line in lines:
                printer("Line: %s" % line)
                parts = line.split() #Split irc data by white space
                if len(parts)>=3 and parts[2][1:].lower()==self.streamer:
                    for parser in self.irc_parsers:
                        parser(parts)
                    if len(parts)>3: #all user input data has at least 3 parts user, PRIVMSG, #channel
                        if parts[1].lower()=="privmsg" and parts[2][1:].lower()==self.streamer: #check this is a message, and its to our channel
                            user = parts.pop(0) 
                            user = user[1:user.find("!")] #get the username from the first "part"
                            parts.pop(0) #throw away the next two parts
                            parts.pop(0)
                            #Put all parts of the message back together into data variable, and lowercase it
                            data = ""
                            for part in parts:
                                data = data + part + " "
                            data = data.lower()
                            printer("User: %s Message: %s" % (user,data))
                            for parser in self.msg_parsers:
                                if parser(user,data):
                                    break

class notification:

    def __init__(self,sound,throttle):
        self.notified = time.time()-throttle
        self.throttle = throttle
        self.sound = sound
    
    def notify(self):
        elapsed = time.time() - self.notified
        if elapsed >= self.throttle:
            printer("Playing notification sound to grab attention %s" % elapsed)
            sound_scare = pygame.mixer.Sound(self.sound)
            channel = sound_scare.play()
            channel.set_volume(1,1) #set volume to full

            clock = pygame.time.Clock()
            # check if playback has finished
            while channel.get_busy():
               clock.tick(30)
            self.notified = time.time()
            return False
        else:
            return round(elapsed)
            
        
    def update_throttle(throttle):
        self.throttle = throttle

#return scary-0 or normal-1 dependant on the current day (>=4 is between thurs and sunday)
def scaryDay():
    if datetime.date.today().isoweekday()>=4:
        printer("Scary Day!")
        return 0
    else:
        printer("Normal Day!")
        return 1

#Prints to console, and a log file
def printer(string):
    print "%s: %s" % (time.strftime("%d-%m-%Y_%H-%M-%S"),string)
    logging.info("%s: %s" % (time.strftime("%d-%m-%Y_%H-%M-%S"),string)) 

#converts a 6 character long (3 bytes) hex string into 3 integers
def hex2chr(input):
    rgb = []
    rgb.append(int(input[0:2], 16))
    rgb.append(int(input[2:4], 16))
    rgb.append(int(input[4:6], 16))
    #print ':'.join(x.encode('hex') for x in rgb)
    return rgb
    
def is_hex(s):
     hex_digits = set(string.hexdigits)
     # if s is long, then it is faster to check against a set
     return all(c in hex_digits for c in s)
     
def bounds(input):
    if input<0:
        input = 0
    if input>255:
        input = 255
    return input
    
#return a color from a 255 rainbow palette
def Wheel(input):
    WheelPos = 255 - int(round(input));
    if WheelPos < 85:
        return [255 - WheelPos * 3, 0, WheelPos * 3];
    elif WheelPos < 170:
        WheelPos -= 85;
        return [0, WheelPos * 3, 255 - WheelPos * 3];
    else:
        WheelPos -= 170;
        return [WheelPos * 3, 255 - WheelPos * 3, 0];

#parse a string for a single color (returned as a list)
def convertcolor(input,random_color):
    input = input.lower()
    stuff = []
    
    if input == "random":
        random_color = ((random.randint(1, 32)+random_color)*7)%255
        printer("Random color: %s" % random_color)
        value = Wheel(random_color)
        stuff.append(value[0])
        stuff.append(value[1])
        stuff.append(value[2])
        return stuff
    
    #look for html color
    for key, value in sorted(html_colors.colors.iteritems()):
        if input.find ( key.lower() ) != -1:
            stuff.append(bounds(int("0x"+value[0:2],0)))
            stuff.append(bounds(int("0x"+value[2:4],0)))
            stuff.append(bounds(int("0x"+value[4:6],0)))
            return stuff
    
    #look for 3 x,x,x
    parts = input.split(",")
    if len(parts)==3:
        #255,255,255
        for part in parts:
            if part.isdigit():
                stuff.append(bounds(int(part)))
        if len(stuff)==3:
            return stuff
        stuff = []
        
        #ff,ff,ff
        for part in parts:
            if len(part)==2 and is_hex(part):
                stuff.append(bounds(int(part, 16)))
        if len(stuff)==3:
            return stuff
            
    else:
        # #ffffff
        stuff = []
        if input[0]=="#":
            input = input[1:]
        # 0xffffff
        if input[0:2]=="0x":
            input = input[2:]
        if len(input)==6 and is_hex(input):
            stuff.append(bounds(int(input[0:2], 16)))
            stuff.append(bounds(int(input[2:4], 16)))
            stuff.append(bounds(int(input[4:6], 16)))
            return stuff

#used to print and write to serial (for debug purposes)
def debugserial(input):
    global ser
	
    printer(input)
    ser.write(input)
    
#Not used at the moment, used to map a number from one range, to another
#similar to arduino's map function
def translate(value, leftMin, leftMax, rightMin, rightMax):
    valueScaled = float(value - leftMin) / float(leftMax - leftMin)
    return rightMin + (valueScaled * (rightMax - rightMin))

log = time.strftime("./logs/%m-%d-%Y_%H-%M-%S.log")
logging.basicConfig(filename=log,level=logging.INFO)    
logging.info('Setting up serial connection...')   