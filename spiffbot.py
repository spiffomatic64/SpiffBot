import socket
import re
import time
import serial
import pygame
import pygame.midi
import pygame.mixer
import threading
import random
import json
import requests
import logging
import win32api as win32
import win32con

#Prints to console, and a log file
def printer(string):
    print "%s: %s" % (time.strftime("%d-%m-%Y_%H-%M-%S"),string)
    logging.info("%s: %s" % (time.strftime("%d-%m-%Y_%H-%M-%S"),string)) 

#Not used at the moment, used to map a number from one range, to another
#similar to arduino's map function
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

#List and select midi device
def getMidiSport(midi):
    c = 0
    for x in range( 0, pygame.midi.get_count() ):
        printer(pygame.midi.get_device_info(x)[1])
        if pygame.midi.get_device_info(x)[1] == midi:
            return c
        c = c + 1

#Not used currently (and not finished) will be used to output a dimmed rgb value      
def midiVolume(vol, red, green, blue):
    red = round(red * (255/vol))
    green = round(red * (255/vol))
    blue = round(red * (255/vol))

#Midi thread, gets midi data, translates to html rgb values, 
#and lights leds based on that color for 50ms, then turns all leds off
#todo: go back to original color
def midiThread():
    global inp #midi input device
    global ser #serial device 
    
    drums = { 38 : "ffffff",    #snare
        40 : "ffffff",          #snare rim
        26 : "ffff00",         #highhat edge
        46 : "ffff00",   #highhat crown
        55 : "00ff00",           #crash edge
        49 : "00ff00",     #crash crown
        48 : "0000ff",        #left tom
        45 : "ff00ff",       #right tom
        59 : "00ffff",            #ride edge
        51 : "00ffff",      #ride crown
        41 : "ff8000",       #floor tom
        36 : "ff0000" }           #bass
    
    # run the event loop
    # Todo: ability to stop, or disable the thread
    while True:
        if inp.poll():
            # no way to find number of messages in queue
            # so we just specify a high max value
            events = inp.read(1000)
            #print events
            for e in events:
                if e[0][2] != 64:
                    printer("%s:%s" % (e[0][1],e[0][2])) #debug comment this out while playing, slows down the thread
                    intensity = abs(e[0][2]) * 2
                    if intensity > 255:
                        intensity = 255
                        
                    if e[0][1] in drums:
                        #print drums[e[0][1]]
                        value = drums[e[0][1]]

                    ser.write("0,%s,%s,%s\n" % (int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)))
                    pygame.time.wait(50)
                    ser.write("0,0,0,0\n")

        # wait 10ms - this is arbitrary, but wait(0) still resulted
        # in 100% cpu utilization
        pygame.time.wait(10)

#gets a "live" list of viewers in chat
def get_viewers():
    global optout
    
    url = 'https://tmi.twitch.tv/group/user/spiffomatic64/chatters'
    
    printer("Checking viewers...")
    data = requests.get(url=url)
    binary = data.content
    output = json.loads(binary)
    viewers = []
    for viewer in output['chatters']['viewers']:
        if viewer not in optout:
            viewers.append(viewer)
            printer(viewer)
    return viewers
    
#Thread responsible for switching control
def mastertimer():
    global counter
    global irc
    global master
    global warn_timer
    global optout
    global mode
    
    while True:
        if mode == 0:
            elapsed = time.time() - counter
            #every 2.5 minutes warn the user in control
            if elapsed>150 and warn_timer == 0:
                if master!="spiffbot":
                    irc.send ( "PRIVMSG #spiffomatic64 :2.5 Minutes left %s! \r\n" % master)  
                warn_timer = 1
            #every 5 minutes switch control, and opt out the user
            if elapsed>300 and warn_timer == 1:
                if master!="spiffbot":
                    irc.send ( 'PRIVMSG #spiffomatic64 :5 Minutes elapsed! Switching control, and opting %s out!\r\n' % master )  
                    printer("Passing control and opting out %s(due to timeout from mastertimer)" % master)
                    optout.append(master)
                switch()
            printer(elapsed)
        time.sleep(1)

#switch control to a random person (or specific person if specified)
def switch(user=""):
    global counter
    global irc
    global master
    global warn_timer
    
    #if warn timer is not -1, set warn timer to -1, then back to 0 at the end of the function
    #This is used to lock the switch thread (to prevent double switching)
    if warn_timer != -1:
        warn_timer = -1
        viewers = get_viewers()
        #remove the current controller from viewers to prevent switching to the same person
        if master in viewers:
            viewers.remove(master)
        old = master
        #Switch to user if specified
        if user in viewers:
            master = user
        else:
            #if there are more than 0 viewers, pick a random viewer
            if len(viewers)>0:
                random.shuffle(viewers) #probably not needed, but what the hell :-P
                master = random.choice(viewers)
            else:
                printer("No valid viewers to switch to")
                master="spiffbot"
        #reset counter and notify chat that a new viewer is in control
        printer("%s is now in control!" % master)
        irc.send ( 'PRIVMSG #spiffomatic64 :%s is now in control!\r\n' % master) 
        printer("Switching from %s to %s" % (old,master))
        counter = time.time()
        warn_timer = 0

#commands that will only work for me (and moderators in the future)
#todo, look up moderators
def admin_commands(user,data):
    global master
    global irc
    global optout
    global mode
    
    if user.lower() == "spiffomatic64":
        #split irc messages into parts by white space 
        parts = data.lower().split()
        printer("admin")
        command = parts[0][1:] #get the first "word" and remove the first character which is ":"
        if command == "!switch":
            #if there is something after switch command, try to switch to that user
            if len(parts) == 2:
                switch(parts[1])
            if len(parts) == 1:
                switch()
        #if there are at least 2 words in the message
        if len(parts) == 2:
            printer(len(parts))
            for part in parts:
                printer(part)
            #add user to optout list
            if command == "!optout":
                if parts[1] not in optout:
                    optout.append(parts[1])
                    irc.send ( 'PRIVMSG #spiffomatic64 :%s has been opted out!\r\n' % parts[1])
                    #if the user is currently in control, switch
                    if parts[1].lower() == master:
                        switch()
            #optin a user
            if command == "!optin":
                #check that user is already opted out
                if parts[1] in optout:
                    optout.remove(parts[1])
                    irc.send ( 'PRIVMSG #spiffomatic64 :%s has been opted back in!\r\n' % parts[1])
            #change mode from scary to normal
            if command == "!mode":
                if parts[1] == "scary":
                    mode = 0
                    printer("Scary time!")
                    counter = time.time()
                    master="spiffomatic64"
                    irc.send ( 'PRIVMSG #spiffomatic64 :ITS SCARY TIME!!!\r\n')
                    modedefault()
                if parts[1] == "normal":
                    mode = 1
                    printer("Normal time!")
                    irc.send ( 'PRIVMSG #spiffomatic64 :Playing normal games\r\n')

#Not used, for debugging to list all monitors
def printAllScreen():
    i = 0
    while True:
        try:
            device = win32.EnumDisplayDevices(None,i);
            print("[%d] %s (%s)"%(i,device.DeviceString,device.DeviceName));
            i = i+1;
        except:
            break;
    return i
                    
#Flip the monitor using winapi's
def flip(duration=10):
    #manually selecting monitor 2 (Windows reports monitor 2, is actually 1)
    device = win32.EnumDisplayDevices(None,1);
    printer("Rotate device %s (%s)"%(device.DeviceString,device.DeviceName));

    dm = win32.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)
    dm.DisplayOrientation = win32con.DMDO_180 #flip 180 degrees
    dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
    dm.Fields = dm.Fields & win32con.DM_DISPLAYORIENTATION
    win32.ChangeDisplaySettingsEx(device.DeviceName,dm)
    time.sleep(duration)
    dm.DisplayOrientation = win32con.DMDO_DEFAULT #flip back to normal
    dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
    dm.Fields = dm.Fields & win32con.DM_DISPLAYORIENTATION
    win32.ChangeDisplaySettingsEx(device.DeviceName,dm)
    return
      
#commands only accessible by the user in control      
def master_commands(user,data):
    global master
    global irc
    global sounds
    global ser
    
    if user.lower() == master.lower(): #check that the user is the master
        parts = data.lower().split()
        command = parts[0][1:]
        
        printer("%s == %s" % (user.lower(), master.lower()))
        #allow a user to pass to someone else, or to someone random
        if command == "!pass":
            if len(parts) == 2:
                if user.lower() != parts[1].lower():
                    switch(parts[1])
                else:
                    irc.send ( 'PRIVMSG #spiffomatic64 :You cant pass to yourself!\r\n')
                    printer("%s tried to pass to them-self" % user.lower())
            if len(parts) == 1:
                switch()
            
        #Song commands
        song = ''
        #slect a random sound
        if command == "!randomsound":
            printer("Random sound")
            song = random.choice(sounds.values())
        #check message for all sound commands
        for sound, file in sounds.iteritems():
            if data.find(sound) != -1:
                printer("Found %s in %s" % (sound,data))
                song = file
                break #stop after the first sound command is found
        if song != '': #if a sound was selected
            warn_timer = 2 #dont switch until the sound is done playing
           
            #setup disco animation in a thread
            printer("Disco animation")
            t3 = threading.Thread(target=disco)
            t3.daemon = True
            
            #setup audio
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
            #printer("Mixer settings" % pygame.mixer.get_init())
            #printer("Mixer channels" % pygame.mixer.get_num_channels())
            pygame.mixer.music.set_volume(1) #set volume to full
            
            #play the sound
            printer("Playing sound %s" % song)
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            clock = pygame.time.Clock()
            t3.start() #start disco animation thread
            while pygame.mixer.music.get_busy():
               # check if playback has finished
               clock.tick(30)
            pygame.mixer.quit() 
            switch()
            return
            
        actions = ['quiet', "rattle", "heart"]
        
        if command == "!randomscare":
            data = random.choice(actions)
            
        #Drop the box on me by moving the arm down for 1 second, then waiting 20 seconds and switching
        if data.find ( 'quiet' ) != -1 or data.find ( 'door' ) != -1 or data.find ( 'drop' ) != -1 or data.find ( 'gun' ) != -1:
            warn_timer = 2
            ser.write("-5,1\n")
            time.sleep(1)
            ser.write("-5,0\n")
            time.sleep(20)
            switch()
            return
        
        #rattle the vibration motor for 2 seconds, then wait 20 seconds and switch
        if data.find ( 'rattle' ) != -1 or data.find ( 'fall' ) != -1 or data.find ( 'rumble' ) != -1 or data.find ( 'vibe' ) != -1:
            warn_timer = 2
            ser.write("-6,1\n")
            time.sleep(2)
            ser.write("-6,0\n")
            time.sleep(20)
            switch()
            return
            
        #rattle the smaller vibration motor for 2 seconds, then wait 20 seconds and switch
        if data.find ( 'heart' ) != -1 or data.find ( 'chest' ) != -1 or data.find ( 'buzz' ) != -1 or data.find ( 'neck' ) != -1:
            warn_timer = 2
            ser.write("-7,1\n")
            time.sleep(2)
            ser.write("-7,0\n")
            time.sleep(20)
            switch()
            return
        #flip the main monitor and switch control
        if data.find ( 'flip' ) != -1:
            flip()
            switch()
            return
        
#set the leds to black if in scary mode, fade up from black to white if normal mode
def modedefault():
    if mode == 0:
        ser.write("0,0,0,0\n")
    if mode == 1:
        for y in range(0, 255):
            ser.write("0,%s,%s,%s\n" % (y,y,y))
            pygame.time.wait(5)
    return
            
def disco():
    global ser
    global mode
    
    irc.send ( 'PRIVMSG #spiffomatic64 :DISCO PARTY!!!!!!!!\r\n' )
    for x in range(0, 5): #loop 5 mins
        for y in range(0, 255): #loop through all 255 colors
            ser.write("-1,%s\n" % y)
            pygame.time.wait(1)
    modedefault()
    return
    
def strobe():
    irc.send ( 'PRIVMSG #spiffomatic64 :SEIZURE PARTY!!!!!!!!\r\n' )
    for x in range(0, 200): #flicker 200 times, for 30 ms on, then 30ms off
        ser.write("0,255,255,255\n")
        pygame.time.wait(30)
        ser.write("0,0,0,0\n")
        pygame.time.wait(30)
    ser.flushInput()
    modedefault()
    return

def discostrobe():
    irc.send ( 'PRIVMSG #spiffomatic64 :DISCO SEIZURES!!!!!!!!\r\n' )
    for x in range(0, 255): #flicker 255 colors on and off for 30 ms each
        ser.write("-1,%s\n" % x)
        pygame.time.wait(30)
        ser.write("0,0,0,0\n")
        pygame.time.wait(30)
    ser.flushInput()
    modedefault()
    return    

def fire():
    irc.send ( 'PRIVMSG #spiffomatic64 :FIRE!!!\r\n' )
    for x in range(0, 100):
        ser.write("-2\n")
        pygame.time.wait(60)
    modedefault()
    return

def chase(r, g, b,num=6):
    printer("%s,%s,%s" %(r,g,b))
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            ser.write("-3,%s,%s,%s,%s\n" %(r,g,b,y))
            #printer("-3,%s,%s,%s,%s\n" %(r,g,b,y))
            pygame.time.wait(30)
        pygame.time.wait(500)
    return
    
def alternate(r1,g1,b1,r2,g2,b2):
    printer("%s,%s,%s,%s,%s,%s" %(r1,g1,b1,r2,g2,b2))
    for x in range(0,10):
        ser.write("-4,%s,%s,%s,%s,%s,%s\n" %(r1,g1,b1,r2,g2,b2))
        pygame.time.wait(500)
    modedefault()
    return

#fire animation using 2 colors
def fire(r1,g1,b1,r2,g2,b2):
    printer("%s,%s,%s,%s,%s,%s" %(r1,g1,b1,r2,g2,b2))
    for x in range(0,100):
        ser.write("-2,%s,%s,%s,%s,%s,%s\n" %(r1,g1,b1,r2,g2,b2))
        pygame.time.wait(60)
    modedefault()
    return

#not used right now, will convert input(r,g,b) or html color, or #rrggbb into rgb values to be used by all functions
def convertcolor(input):
    input = input.lower()
    value = []
    for key, value in colors.iteritems():
        if input.find ( key.lower() ) != -1:
            value[0] = int("0x"+value[0:2],0)
            value[1] = int("0x"+value[2:4],0)
            value[2] = int("0x"+value[4:6],0)
        return

#commands accessible by all users
def user_commands(user,data):
    global master
    global irc
    global colors
    global ser
    global optout
    global mode
    
    parts = data.lower().split()
    command = parts[0][1:]
    
    #start commands
    if data.find ( 'test' ) != -1:
        irc.send ( 'PRIVMSG #spiffomatic64 :test to you too!\r\n' )
    
    #Scary mode only commands
    if mode == 0:
        if command == "!whosgotit":
            irc.send ( 'PRIVMSG #spiffomatic64 :%s is in control!\r\n' % master)
            return
        #opt a user out, and switch if they were in control
        if command == "!optout":
            if user not in optout and user != "spiffomatic64":
                optout.append(user)
                irc.send ( 'PRIVMSG #spiffomatic64 :%s has opted out!\r\n' % user)
                if user == master:
                    switch()
            return
        #allow a user to opt back in
        if command == "!optin":
            if user in optout:
                optout.remove(user)
                irc.send ( 'PRIVMSG #spiffomatic64 :%s has opted back in!\r\n' % user)
            return
        #let viewers know how much time is left    
        if command == "!timeleft":
            timeleft = 300 - (time.time() - counter)
            irc.send ( 'PRIVMSG #spiffomatic64 :%s has %s seconds left!\r\n' % (master,round(timeleft)))
            return
        
    #disco rainbow colors
    if data.find ( 'disco' ) != -1:
        if data.find ( 'strobe' ) != -1:
            discostrobe()
        else :
            disco()
        return

    #flickr strobe
    if data.find ( 'strobe' ) != -1:
        strobe()
        return
            
    #fire animation
    #if data.find ( 'fire' ) != -1:
        #fire()
        #return
    
    #rgb all pixels one color
    m = re.search('rgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\)',data,re.IGNORECASE)
    if m:
        if m.group(3):
            printer("%s,%s,%s" %(m.group(1),m.group(2),m.group(3)))
            ser.write("0,%s,%s,%s\n" %(m.group(1),m.group(2),m.group(3)))
            time.sleep(5)
            modedefault()
            return

    #Chase animation (rgb)
    m = re.search('chase\((\d{1,3}),(\d{1,3}),(\d{1,3})\)',data,re.IGNORECASE)
    if m:
        if m.group(3):
            chase(m.group(1),m.group(2),m.group(3))
            modedefault()
            return
            
    #Chase 3 colors (html codes)
    m = re.search('chase\((\w+),(\w+),(\w+)\)',data,re.IGNORECASE)
    if m:
        if m.group(1) and m.group(1) in colors:
            value = colors[m.group(1)]
            chase(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0),2)
        if m.group(2) and m.group(2) in colors:
            value = colors[m.group(2)]
            chase(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0),2)
        if m.group(3) and m.group(3) in colors:
            value = colors[m.group(3)]
            chase(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0),2)
        modedefault()
        return
    #Chase 2 colors (html codes)
    m = re.search('chase\((\w+),(\w+)\)',data,re.IGNORECASE)
    if m:
        if m.group(1) and m.group(1) in colors:
            value = colors[m.group(1)]
            chase(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0),3)
        if m.group(2) and m.group(2) in colors:
            value = colors[m.group(2)]
            chase(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0),3)
        modedefault()
        return
    #Chase 1 color (html codes)
    m = re.search('chase\((\w+)\)',data,re.IGNORECASE)
    if m:
        if m.group(1) and m.group(1) in colors:
            value = colors[m.group(1)]
            chase(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0))
            modedefault()
            return

    #Alternate animation (rgb)
    m = re.search('alternate\((\d{1,3}),(\d{1,3}),(\d{1,3}),(\d{1,3}),(\d{1,3}),(\d{1,3})\)',data,re.IGNORECASE)
    if m:
        if m.group(6):
            alternate(m.group(1),m.group(2),m.group(3),m.group(4),m.group(5),m.group(6))
            return
    #Alternate animation (html)
    m = re.search('alternate\((\w+),(\w+)\)',data,re.IGNORECASE)
    if m:
        if m.group(2) and  m.group(1) in colors and  m.group(2) in colors:
            value = colors[m.group(1)]
            value2 = colors[m.group(2)]
            alternate(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0),int("0x"+value2[0:2],0),int("0x"+value2[2:4],0),int("0x"+value2[4:6],0))
            return
    #fire animation (rgb)
    m = re.search('fire\((\d{1,3}),(\d{1,3}),(\d{1,3}),(\d{1,3}),(\d{1,3}),(\d{1,3})\)',data,re.IGNORECASE)
    if m:
        if m.group(6):
            fire(m.group(1),m.group(2),m.group(3),m.group(4),m.group(5),m.group(6))
            return
    #fire animation (html)
    m = re.search('fire\((\w+),(\w+)\)',data,re.IGNORECASE)
    if m:
        if m.group(2) and  m.group(1) in colors and  m.group(2) in colors:
            value = colors[m.group(1)]
            value2 = colors[m.group(2)]
            fire(int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0),int("0x"+value2[0:2],0),int("0x"+value2[2:4],0),int("0x"+value2[4:6],0))
            return
            
    #html color keys (single color, no animation)
    for key, value in colors.iteritems():
        if data.find ( key.lower() ) != -1:
            printer("key: %s value: %s : %s,%s,%s" % (key,value,int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)))
            irc.send ( 'PRIVMSG #spiffomatic64 :%s!!!\r\n' % key.upper())
            ser.write("0,%s,%s,%s\n" % (int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)) )
            time.sleep(5)
            modedefault()
            return

#map of html color commands to hex codes
colorsup = { "AliceBlue":"F0F8FF" ,
"AntiqueWhite":"FAEBD7" ,
"Aqua":"00FFFF" ,
"Aquamarine":"7FFFD4" ,
"Azure":"F0FFFF" ,
"Beige":"F5F5DC" ,
"Bisque":"FFE4C4" ,
"Black":"000000" ,
"BlanchedAlmond":"FFEBCD" ,
"Blue":"0000FF" ,
"BlueViolet":"8A2BE2" ,
"Brown":"A52A2A" ,
"BurlyWood":"DEB887" ,
"CadetBlue":"5F9EA0" ,
"Chartreuse":"7FFF00" ,
"Chocolate":"D2691E" ,
"Coral":"FF7F50" ,
"CornflowerBlue":"6495ED" ,
"Cornsilk":"FFF8DC" ,
"Crimson":"DC143C" ,
"Cyan":"00FFFF" ,
"DarkBlue":"00008B" ,
"DarkCyan":"008B8B" ,
"DarkGoldenRod":"B8860B" ,
"DarkGray":"A9A9A9" ,
"DarkGreen":"006400" ,
"DarkKhaki":"BDB76B" ,
"DarkMagenta":"8B008B" ,
"DarkOliveGreen":"556B2F" ,
"DarkOrange":"FF8C00" ,
"DarkOrchid":"9932CC" ,
"DarkRed":"8B0000" ,
"DarkSalmon":"E9967A" ,
"DarkSeaGreen":"8FBC8F" ,
"DarkSlateBlue":"483D8B" ,
"DarkSlateGray":"2F4F4F" ,
"DarkTurquoise":"00CED1" ,
"DarkViolet":"9400D3" ,
"DeepPink":"FF1493" ,
"DeepSkyBlue":"00BFFF" ,
"DimGray":"696969" ,
"DodgerBlue":"1E90FF" ,
"FireBrick":"B22222" ,
"FloralWhite":"FFFAF0" ,
"ForestGreen":"228B22" ,
"Fuchsia":"FF00FF" ,
"Gainsboro":"DCDCDC" ,
"GhostWhite":"F8F8FF" ,
"Gold":"FFD700" ,
"GoldenRod":"DAA520" ,
"Gray":"808080" ,
"Green":"008000" ,
"GreenYellow":"ADFF2F" ,
"HoneyDew":"F0FFF0" ,
"HotPink":"FF69B4" ,
"IndianRed":"CD5C5C" ,
"Indigo":"4B0082" ,
"Ivory":"FFFFF0" ,
"Khaki":"F0E68C" ,
"Lavender":"E6E6FA" ,
"LavenderBlush":"FFF0F5" ,
"LawnGreen":"7CFC00" ,
"LemonChiffon":"FFFACD" ,
"LightBlue":"ADD8E6" ,
"LightCoral":"F08080" ,
"LightCyan":"E0FFFF" ,
"LightGoldenRodYellow":"FAFAD2" ,
"LightGray":"D3D3D3" ,
"LightGreen":"90EE90" ,
"LightPink":"FFB6C1" ,
"LightSalmon":"FFA07A" ,
"LightSeaGreen":"20B2AA" ,
"LightSkyBlue":"87CEFA" ,
"LightSlateGray":"778899" ,
"LightSteelBlue":"B0C4DE" ,
"LightYellow":"FFFFE0" ,
"Lime":"00FF00" ,
"LimeGreen":"32CD32" ,
"Linen":"FAF0E6" ,
"Magenta":"FF00FF" ,
"Maroon":"800000" ,
"MediumAquaMarine":"66CDAA" ,
"MediumBlue":"0000CD" ,
"MediumOrchid":"BA55D3" ,
"MediumPurple":"9370DB" ,
"MediumSeaGreen":"3CB371" ,
"MediumSlateBlue":"7B68EE" ,
"MediumSpringGreen":"00FA9A" ,
"MediumTurquoise":"48D1CC" ,
"MediumVioletRed":"C71585" ,
"MidnightBlue":"191970" ,
"MintCream":"F5FFFA" ,
"MistyRose":"FFE4E1" ,
"Moccasin":"FFE4B5" ,
"NavajoWhite":"FFDEAD" ,
"Navy":"000080" ,
"OldLace":"FDF5E6" ,
"Olive":"808000" ,
"OliveDrab":"6B8E23" ,
"Orange":"FFA500" ,
"OrangeRed":"FF4500" ,
"Orchid":"DA70D6" ,
"PaleGoldenRod":"EEE8AA" ,
"PaleGreen":"98FB98" ,
"PaleTurquoise":"AFEEEE" ,
"PaleVioletRed":"DB7093" ,
"PapayaWhip":"FFEFD5" ,
"PeachPuff":"FFDAB9" ,
"Peru":"CD853F" ,
"Pink":"FFC0CB" ,
"Plum":"DDA0DD" ,
"PowderBlue":"B0E0E6" ,
"Purple":"800080" ,
"Red":"FF0000" ,
"RosyBrown":"BC8F8F" ,
"RoyalBlue":"4169E1" ,
"SaddleBrown":"8B4513" ,
"Salmon":"FA8072" ,
"SandyBrown":"F4A460" ,
"SeaGreen":"2E8B57" ,
"SeaShell":"FFF5EE" ,
"Sienna":"A0522D" ,
"Silver":"C0C0C0" ,
"SkyBlue":"87CEEB" ,
"SlateBlue":"6A5ACD" ,
"SlateGray":"708090" ,
"Snow":"FFFAFA" ,
"SpringGreen":"00FF7F" ,
"SteelBlue":"4682B4" ,
"Tan":"D2B48C" ,
"Teal":"008080" ,
"Thistle":"D8BFD8" ,
"Tomato":"FF6347" ,
"Turquoise":"40E0D0" ,
"Violet":"EE82EE" ,
"Wheat":"F5DEB3" ,
"White":"FFFFFF" ,
"WhiteSmoke":"F5F5F5" ,
"Yellow":"FFFF00" ,
"YellowGreen":"9ACD32" }

#turns all html colors to lowercase
colors = dict((k.lower(), v) for k,v in colorsup.iteritems())
    
#Map of sound commands to sound files
sounds = { "slam" : "SOUND_1277.ogg",
"screach" : "SOUND_1288.ogg",
"heatbeat" : "SOUND_1323.ogg",
"crash" : "SOUND_1399.ogg",
"bam" : "SOUND_1463.ogg",
"deep" : "SOUND_1465.ogg",
"eery" : "SOUND_1467.ogg",
"creak" : "SOUND_1507.ogg",
"low" : "SOUND_1511.ogg",
"bang" : "SOUND_1528.ogg",
"clang" : "SOUND_1598.ogg",
"boom" : "SOUND_1603.ogg",
"scrape" : "SOUND_1604.ogg",
"creepy" : "SOUND_1608.ogg",
"techo" : "SOUND_1630.ogg",
"animal" : "SOUND_0004.ogg",
"creeky" : "SOUND_0012.ogg",
"robot" : "SOUND_0029.ogg",
"rythm" : "SOUND_0030.ogg",
"open" : "SOUND_0042.ogg",
"locked" : "SOUND_0072.ogg",
"hiss" : "SOUND_0195.ogg",
"moan" : "SOUND_0296.ogg",
"static" : "sh2static2.ogg",
"kids" : "kids.ogg",
"cut" : "3dcut.ogg", 
"saw" : "3dbread.ogg" }

#Create log file
log = time.strftime("%m-%d-%Y_%H-%M-%S.log")
logging.basicConfig(filename=log,level=logging.INFO)    
logging.info('Setting up serial connection...')   

#Midi initialization 
#pygame.init()
#pygame.midi.init()
#inp = pygame.midi.Input(getMidiSport("MIDISPORT 1x1 In"))

#serial stuff
#todo: add code to find arduino dynamically
ser = serial.Serial("Com4", 9600)


	
#start IRC
network = 'irc.twitch.tv'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
printer("connected")
#IRC auth
#todo: move this to a seperate file
irc.send ( 'PASS oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\r\n' )
irc.send ( 'NICK spiffbot\r\n' )
irc.send ( 'USER spiffbot spiffbot spiffbot :Python IRC\r\n' )
#wait before reading data (needed for twitch)
time.sleep(0.5)
printer(irc.recv ( 4096 ))
printer("Got stuff")
#wait before joining (needed for twitch)
time.sleep(0.5)
irc.send ( 'JOIN #spiffomatic64\r\n' )

#Midi Thread start
#t = threading.Thread(target=midiThread)
#t.daemon = True
#t.start()

#Switch Timer Thread start
t2 = threading.Thread(target=mastertimer)
t2.daemon = True
counter = time.time()
master = "spiffomatic64"
warn_timer = 0
mode = 1
t2.start()

#instead of calling functions directly, add them to a global queue with a processing thread
#the thread will 

optout = []
#not used yet, will be using these global variables to keep track of the "current color"
r = 0
g = 0
b = 0

#Main loop
while True:
    ser.flushInput() #ignore serial input, TODO log serial input without locking loop
    orig = irc.recv ( 4096 ) #recieve irc data
    parts = orig.split() #Split irc data by white space
    if orig.find ( 'PING' ) != -1: #Needed to keep connected to IRC, without this, twitch will disconnect
        irc.send ( 'PONG ' + orig.split() [ 1 ] + '\r\n' )
    if len(parts)>3: #all user input data has at least 3 parts user, PRIVMSG, #channel
        printer("Len parts %s" % len(parts))
        user = parts.pop(0) 
        user = user[1:user.find("!")] #get the username from the first "part"
        parts.pop(0) #throw away the next two parts
        parts.pop(0)
        #Put all parts back together into data variable, and lowercase it
        data = ""
        for part in parts:
            data = data + part + " "
        data = data.lower()
        printer("User Message: %s" % data)
        
        #check for admin commands
        admin_commands(user,data)
        #if scary mode, check for in control commands
        if mode == 0:
            master_commands(user,data)  
        #check for normal user commands
        user_commands(user,data)
    printer(orig)