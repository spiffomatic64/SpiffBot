import logging
import datetime
import time
import html_colors

#return scary-0 or normal-1 dependant on the current day (>=4 is between thurs and sunday)
def scaryDay():
    if datetime.date.today().isoweekday()>=4:
        return 0
    else:
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

log = time.strftime("%m-%d-%Y_%H-%M-%S.log")
logging.basicConfig(filename=log,level=logging.INFO)    
logging.info('Setting up serial connection...')   