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
import win32api as win32
import win32gui
import win32con
import twitch_auth
import string
import html_colors
import os 
import twitch_bot_utils
import time
import traceback
from subprocess import call
import twitch_db

#Map of sound commands to sound files
sounds = { "slam" : "SOUND_1277.ogg",
"screech" : "SOUND_1288.ogg",
"heartbeat" : "SOUND_1323.ogg",
"crash" : "SOUND_1399.ogg",
"highbang" : "SOUND_1463.ogg",
"deep" : "SOUND_1465.ogg",
"eery" : "SOUND_1467.ogg",
"creak" : "SOUND_1507.ogg",
"lownoise" : "SOUND_1511.ogg",
"deepbang" : "SOUND_1528.ogg",
"clang" : "SOUND_1598.ogg",
"boom" : "SOUND_1603.ogg",
"scrape" : "SOUND_1604.ogg",
"creepy" : "SOUND_1608.ogg",
"techno" : "SOUND_1630.ogg",
"animal" : "SOUND_0004.ogg",
"creeky" : "SOUND_0012.ogg",
"robot" : "SOUND_0029.ogg",
"rhythm" : "SOUND_0030.ogg",
"open" : "SOUND_0042.ogg",
"locked" : "SOUND_0072.ogg",
"hiss" : "SOUND_0195.ogg",
"moan" : "SOUND_0296.ogg",
"static" : "sh2static2.ogg",
"kids" : "kids.ogg",
"cutting" : "3dcut.ogg", 
"sawing" : "3dbread.ogg", 
"zombie" : "zombie_scare.ogg",
"tentacle" : "stinger_tentacle.ogg",
"sting" : "sting.ogg",
"bigzombie" : "large_zombie.ogg",
"hunter" : "hunter.ogg",
"brute" : "brute.ogg",
"zombieattack" : "zombie_attack_walk.ogg",
"spawn" : "aslt_spwn_01.ogg",
"birds" : "birdflock_calls_medium_loop_v1.ogg",
"teleport" : "taken_flanker_tele_01.ogg",
"wings" : "birdflock_wings_medium_loop_v1.ogg",
"subtlebirds" : "subtle_birds.ogg"
}

def inBetween(stuff,first,last):
    return stuff[stuff.find(first)+len(first):stuff.find(last)]

def get_next_game():
    url = "http://api.twitch.tv/api/channels/%s/panels" % twitch_auth.get_streamer()
    twitch_bot_utils.printer("Checking games...")
    data = requests.get(url)
    binary = data.content
    output = json.loads(binary)
    for panel in output:
        if panel['data']['title'] == "Schedule":
            scary = panel['html_description'].split("<strong>Normal Games</strong>")[1]
            games = scary.splitlines()
            for game in games:
                if game.find("<strong>next</strong>") != -1:
                    return inBetween(game,"<h1>",":")

def twitch_profile(data):
    f = open('profile.txt', 'a')
    if data==-1:
        f.truncate()
    else:
        f.write("%s\n" % data)
    f.close()

twitch_profile(-1)
twitch_profile("Here are the commands you can use to play along, and interact with my \"spiffbot\"")
twitch_profile("")
twitch_profile("Spiffbot has 2 main modes: Scary (Thurs-Sunday), Normal (Mon-Weds)")
twitch_profile("")

def opt(user,inout):
    user=user.lower()
    if inout:
        if not db.getUserOpted(user):
            db.updateUserOpted(user,1)
            if master==twitch_auth.get_bot():
                switch(user)
    else:
        if user == twitch_auth.get_streamer():
            switch()
        elif db.getUserOpted(user):
            db.updateUserOpted(user,0)
            if user == master:
                switch()
                
def autoOptIn(user,data):
    if user not in db.getUsers():
        opt(user,True)

def scare_lock(status):
    global scaring
    twitch_bot_utils.printer("Setting scaring: %s" % status)
    scaring = status

def wait_serial():
    while writing==1:
        pygame.time.wait(10)
        
def wait_animating():
    while animating==1:
        pygame.time.wait(10)

def writing_serial(input):
    global writing
    
    wait_serial()
    writing = 1
    try:
        ser.write(input)
    except:
        twitch_bot_utils.printer("Serial write crashed crashed writing: %s" % join(hex(ord(n)) for n in my_hex))
        twitch_bot_utils.printer(traceback.format_exc())
    writing = 0

def user_wait(duration):
    stop = time.time()+duration
    while time.time() < stop and scaring==0:
        time.sleep(0.5)
    return

#List and select midi device
def getMidi(midi_device):
    c = 0
    for x in range( 0, pygame.midi.get_count() ):
        twitch_bot_utils.printer(pygame.midi.get_device_info(x)[1])
        if pygame.midi.get_device_info(x)[1] == midi_device:
            twitch_bot_utils.printer("Found midi: %s" % c)
            return c
        c = c + 1

#Midi thread, gets midi data, translates to html rgb values, 
#and lights leds based on that color for 50ms, then turns all leds off
def midiThread():
    global midi #midi input device
     #serial device 
    
    drums = { 38 : "ffffff",    #snare
        40 : "ffffff",          #snare rim
        26 : "ffff00",          #highhat edge
        46 : "ffff00",          #highhat crown
        55 : "00ff00",          #crash edge
        49 : "00ff00",          #crash crown
        48 : "0000ff",          #left tom
        45 : "ff00ff",          #right tom
        59 : "00ffff",          #ride edge
        51 : "00ffff",          #ride crown
        41 : "ff8000",          #floor tom
        36 : "ff0000" }         #bass
    
    # run the event loop
    # Todo: ability to start/stop, or enable/disable the thread
    while True:
        if midi.poll():
            #read 1000 bytes from midi device
            events = midi.read(1000)
            for e in events:
                if e[0][2] != 64: #ignore note off packets
                    #twitch_bot_utils.printer("%s:%s" % (e[0][1],e[0][2])) #debug, comment this out while playing, slows down the thread
                    intensity = abs(e[0][2]) * 2
                    if intensity > 255:
                        intensity = 255
                        
                    if e[0][1] in drums:
                        #twitch_bot_utils.printer(drums[e[0][1]]) #debug, comment this out while playing, slows down the thread
                        value = drums[e[0][1]]
                    rgb = twitch_bot_utils.hex2chr(value)
                    #before = get_pixels()
                    
                    writing_serial("#%c%c%c\xff!" % (rgb[0],rgb[1],rgb[2]))
                    pygame.time.wait(50)
                    '''for x in range(0,30):
                        writing_serial("#%c%c%c%c" % (before["%s"%x][0],before["%s"%x][1],before["%s"%x][2],x))
                    writing_serial("!")'''
                    writing_serial("#\x00\x00\x00\xff!")

        # wait 10ms - this is arbitrary, but wait(0) still resulted
        # in 100% cpu utilization
        pygame.time.wait(10)

#gets a "live" list of viewers in chat
def get_viewers(opted=True):
    url = "https://tmi.twitch.tv/group/user/%s/chatters" % twitch_auth.get_streamer()
    twitch_bot_utils.printer("Checking viewers...")
    data = requests.get(url=url)
    binary = data.content
    output = json.loads(binary)
    viewers = []
    for viewer in output['chatters']['viewers']:
        if db.getUserOpted(viewer):
            viewers.append(viewer)
            twitch_bot_utils.printer(viewer)
    for viewer in output['chatters']['moderators']:
        if db.getUserOpted(viewer) and viewer!=twitch_auth.get_bot() and viewer!=twitch_auth.get_streamer():
            viewers.append(viewer)
            twitch_bot_utils.printer(viewer)
    return viewers
    
def get_game():
    url = "https://api.twitch.tv/kraken/streams/%s" % twitch_auth.get_streamer()
    twitch_bot_utils.printer("Checking game...")
    data = requests.get(url=url)
    binary = data.content
    output = json.loads(binary)
    game = output['stream']['game']
    return game
    
#Thread responsible for switching control
def mastertimer():
    global counter
    global master
    global switching
    global mode

    warn_timer = 0
    counter = time.time()
    
    while True:
        if mode == 0:
            if scaring == 0 and switching == 0:
                elapsed = time.time() - counter
                #every 5 minutes switch control, and remove master from optedin list 300
                if elapsed>300 and warn_timer < 2:
                    if master!=twitch_auth.get_bot():
                        irc.msg("5 Minutes elapsed! Switching control, and opting %s out!" % master)  
                        twitch_bot_utils.printer("Passing control and opting out %s(due to timeout from mastertimer)" % master)
                        opt(master,False)
                    twitch_bot_utils.printer("Master switch")
                    counter = time.time()
                    warn_timer = 0
                #every 2.5 minutes warn the user in control 150 (make sure to only warn once)
                elif elapsed>150 and warn_timer == 0:
                    if master!=twitch_auth.get_bot():
                        irc.msg( "2.5 Minutes left %s!" % master)  
                        twitch_bot_utils.printer("Sending 2.5 minute warning")
                    warn_timer = 1
                
                twitch_bot_utils.printer(elapsed)
        time.sleep(1)
        
#switch control to a random person (or specific person if specified)
def switch(user="",pass_control=0):
    global counter
    global master
    global switching
    global next
    global pass_counter
    
    twitch_bot_utils.printer("Switching with user: %s" % user)
    #if warn timer is not -1, set warn timer to -1, then back to 0 at the end of the function
    #This is used to lock the switch thread (to prevent double switching)
    if switching == 0 and scaring == 0:
        switching = 1
        
        #pass limiting logic
        twitch_bot_utils.printer("Pass Counter: %s" % pass_counter)
        if pass_control==0: #reset pass counter
            pass_counter = 0
        elif pass_control==1: #increment pass_counter
            pass_counter = pass_counter +1
        if pass_counter>2 and pass_control!=-1:
            irc.msg("Too many passes to specific users, use a scare command, or !pass without a username") 
            switching = 0
            return
            
        twitch_bot_utils.printer("getting viewers")
        viewers = get_viewers()
        
        #remove the current controller from available viewers to prevent switching to the same person
        if master in viewers:
            viewers.remove(master)
        #add logic for fairness
        
        old = master
        #if a "next" user is specified, switch to that user
        if next:
            twitch_bot_utils.printer("next was set to: %s" % next)
            if user=="":
                twitch_bot_utils.printer("user is not set")
                user = next
                next = None
        #Switch to user if specified
        if user in viewers:
            twitch_bot_utils.printer("User is set: %s" % user)
            master = user
        else:
            #if there are more than 0 viewers, pick a random viewer
            if len(viewers)>0:
                
                if user == -1:
                    master = db.getLastControl(viewers)
                else:
                    random.shuffle(viewers) #probably not needed, but what the hell :-P
                    master = random.choice(viewers)
            else:
                twitch_bot_utils.printer("No valid viewers to switch to")
                master=twitch_auth.get_bot()
        #reset counter and notify chat that a new viewer is in control
        twitch_bot_utils.printer("%s is now in control!" % master)
        irc.msg("%s is now in control!" % master) 
        twitch_bot_utils.printer("Switching from %s to %s" % (old,master))
        db.updateLastControl(master)
        counter = time.time()
        switching = 0
    else:
        twitch_bot_utils.printer("Another switch is in progress")

#commands that will only work for me (and moderators in the future)
def admin_commands(user,data):
    global master
    global counter
    global mode
    global next
    
    #if user.lower() == twitch_auth.get_streamer():
    if user.lower() == "spiffomatic64":
        #split irc messages into parts by white space 
        parts = data.lower().split()
        twitch_bot_utils.printer("User is admin, checking for commands")
        command = parts[0][1:] #get the first "word" and remove the first character which is ":"
        if command == "!switch":
            #if there is something after switch command, try to switch to that user
            if len(parts) == 2:
                switch(parts[1],-1)
                return True
            if len(parts) == 1:
                switch()
                return True
        if command == "!whosoptedin":
            optedin = ""
            viewers = get_viewers()
            for optins in db.getOptedUsers():
                if optins in viewers:
                    optedin = "%s %s " % (optedin,optins)
            irc.msg("%s" % optedin)
            return True
        #if there are at least 2 words in the message
        if len(parts) == 2:
            for part in parts:
                twitch_bot_utils.printer(part)
            #add user to opted in list
            if command == "!optin":
                opt(parts[1],True)
                irc.msg("Opting %s in" % parts[1])
                return True
            #optout a user
            if command == "!optout":
                #check that user is already opted in
                opt(parts[1],False)
                return True
            #change mode from scary to normal
            if command == "!mode":
                if parts[1] == "scary":
                    mode = 0
                    twitch_bot_utils.printer("Scary time!")
                    counter = time.time()
                    master=twitch_auth.get_streamer()
                    irc.msg("ITS SCARY TIME!!!")
                    modedefault()
                    return True
                if parts[1] == "normal":
                    mode = 1
                    twitch_bot_utils.printer("Normal time!")
                    irc.msg("Playing normal games")
                    modedefault()
                    return True
            if command == "!switchnext":
                twitch_bot_utils.printer("Setting next user to: %s" % parts[1])
                next=parts[1]
                return True

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
def flip(duration=20,scare=0):
    scare_lock(1)
    scare_status("Monitor is flipped!")
    #manually selecting monitor 2 (Windows reports monitor 2, is actually 1)
    device = win32.EnumDisplayDevices(None,1);
    twitch_bot_utils.printer("Rotate device %s (%s)"%(device.DeviceString,device.DeviceName));

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
    scare_status(-1)
    scare_lock(0)
    if scare==0:
        switch()
    return
    
#Slow strobe the monitor effect
def flicker(times=5,scare=0):
    scare_lock(1)
    pygame.display.set_mode((1280, 1024), pygame.NOFRAME  , 32)
    
    while True:
        time.sleep(0.001)
        try:
            hwnd = win32gui.FindWindow(None,"pygame window")
            print hwnd
            if hwnd:
                twitch_bot_utils.printer("Got hwnd Setting to topmost")
                win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,1,1,0)
                break
        except win32gui.error:
            print 'not found'
    
    if hwnd:
        for i in range(0,times):
            twitch_bot_utils.printer("Flicker off")
            pygame.display.set_mode((1280, 1024), pygame.NOFRAME  , 32)
            time.sleep(0.5)
            twitch_bot_utils.printer("Flicker on")
            pygame.display.set_mode((1, 1), pygame.NOFRAME  , 32)
            time.sleep(0.05)
    pygame.display.quit()
    scare_lock(0)
    if scare==0:
        switch()
      
def arduino_scare(pin,start,stop,command,msg,dur,wait,times,scare):
    scare_lock(1)
    scare_status(msg)
    twitch_bot_utils.printer("Arguino scare, scare=%s" % scare)
    status_length = 3
    twitch_bot_utils.printer("%s %s time(s)" % (msg,times))
    for i in range(0,times):
        writing_serial("#%c%c\x00%c" % (pin,start,command))
        time.sleep(dur)
        writing_serial("#%c%c\x00%c" % (pin,stop,command))
    time.sleep(status_length)
    scare_status(-1)
    time.sleep(wait-status_length)
    scare_lock(0)
    if scare==0:
        switch()
        
def notify():
    #play the sound
    twitch_bot_utils.printer("Playing notification sound to grab attention")
    sound_scare = pygame.mixer.Sound("./sounds/OOT_MainMenu_Select.ogg")
    channel = sound_scare.play()
    channel.set_volume(1,1) #set volume to full

    clock = pygame.time.Clock()
    while channel.get_busy():
       # check if playback has finished
       clock.tick(30)
    
def play_sound(song,left,right,scare=0):
    scare_lock(1)
    #play the sound
    twitch_bot_utils.printer("Playing sound %s" % song)
    sound_scare = pygame.mixer.Sound("./sounds/%s" % song)
    channel = sound_scare.play()
    channel.set_volume(left,right) #set volume to full
    

    clock = pygame.time.Clock()
    while channel.get_busy():
       # check if playback has finished
       #pygame.display.update()
       clock.tick(30)
    #pygame.mixer.quit() 
    scare_lock(0)
    if scare==0:
        switch()
    
def turn_off_monitors(msg,wait,scare=0):
    twitch_bot_utils.printer("Monitor scare")
    scare_status(msg)
    scare_lock(1)
    status_length = 3
    twitch_bot_utils.printer(msg)
    call(["nircmd.exe", "monitor", "off"])
    time.sleep(2.5+status_length)
    scare_status(-1)
    time.sleep(wait-status_length)
    scare_lock(0)
    if scare==0:
        switch()
    
def scare_status(status):
    f = open('scarestatus.txt', 'w')
    if status==-1:
        f.truncate()
    else:
        f.write(status)
    f.close()
      
#commands only accessible by the user in control      
twitch_profile("#Scary mode:")
twitch_profile("Spiffbot will randomly pick someone in chat to be \"in control\".")
twitch_profile("This person will have 5 minutes (with a 2.5 minute warning letting you know how much time is left) to use a \"scare\" command.")
twitch_profile("")
twitch_profile("##Scare Commands for the user in \"Control\"")
twitch_profile("**!randomscare** : Picks a action scare randomly  ")
twitch_profile("")
twitch_profile("**drop**, **quiet**, **door**, or **gun** :Drops a small cardboard box directly in front of me, that no matter how far in advance I know its coming, always seems to scare the pants off me...  ")
twitch_profile("")
twitch_profile("**brush**, **pants**, **spider**, or **crawl** :This is by far the most overpowered scare we have, its a server strapped to my leg, that grabs my pants and makes it feel like someone is tugging at my pants")
twitch_profile("")
twitch_profile("**touch**, **shoulder**, or **tapping** :This will move a servo (twice) attached to my shoulder that emulates someone tapping on it")
twitch_profile("")
twitch_profile("**rattle**, **fall**, **rumble**, or **vibe** :Turns on a vibration motor I took out of an xbox controller, that will rattle around making noise/vibrations/ and movement out of the corner of my eye... Will most likely also scare the pants off me...")
twitch_profile("")
twitch_profile("**heart**, **chest**, **buzz**, **neck** : Turns on a smaller vibration motor that I will attach to myself somehow (wear around neck, sit on thigh etc... I will actually feel this, and its pretty sure to scare any pants that are still left on me at this point....")
twitch_profile("")
twitch_profile("**!flip** : Flips my main monitor image 180 degrees (vertically) for 30 full seconds (everything should look normal on the stream though)")
twitch_profile("")
twitch_profile("**!monitor** : Turns off all monitors at once, for a solid 2.5 seconds")
twitch_profile("")
twitch_profile("##Sounds commands for the user in \"Control\"")
twitch_profile("**!pass** : allows you to pass control on to the person who has not had control in the longest instead of using it yourself. If you add a username after !pass, you can pass control to someone specifically") 
twitch_profile("**!randomsound** : Picks a sound scare randomly")

twitch_profile("##Commands for everyone (even if you don't have control)")
twitch_profile("These commands, are available to everyone (even when not in control)  ")
twitch_profile("")
twitch_profile("**!whosgotit** : lets you know who is currently in control  ")
twitch_profile("")
twitch_profile("**!timeleft** : lets you know much much time is left before control is shifted  ")
twitch_profile("")
twitch_profile("**!optout** : lets you opt out of getting picked for control")
twitch_profile("")
twitch_profile("**!optin** : lets you opt back in to get control")
twitch_profile("")
twitch_profile("**!game** : lets you know what game we are currently playing")
twitch_profile("")
sound_buffer = ""
for sound, file in sounds.iteritems():
    sound_buffer = "%s**%s**, " % (sound_buffer,sound)
twitch_profile(sound_buffer)
def master_commands(user,data):
    global master
    global sounds
    
    #check that the user is the master, and we are in scary mode
    if scaring==0 and switching==0 and (user.lower() == master.lower() or user.lower()==twitch_auth.get_streamer()) and mode==0:
        if user.lower()==twitch_auth.get_streamer():
            twitch_bot_utils.printer("User is admin, dont switch")
            admin = 1
        else:
            admin = 0 
        twitch_bot_utils.printer("User is in control, checking for commands")
        parts = data.lower().split()
        command = parts[0][1:]
        
        twitch_bot_utils.printer("%s == %s" % (user.lower(), master.lower()))
        #allow a user to pass to someone else, or to someone random
        if command == "!pass":
            if len(parts) == 2:
                if user.lower() != parts[1].lower():
                    if parts[1].lower() in db.getOptedUsers():
                        twitch_bot_utils.printer("%s pasing to %s" % (user.lower(),parts[1].lower()))
                        switch(parts[1],1)
                        return True
                    else:
                        irc.msg("Can't pass, %s is opted out!" % parts[1].lower())
                        twitch_bot_utils.printer("%s tried to pass to %s who is opted out" % (user.lower(),parts[1].lower()))
                        return True
                else:
                    irc.msg("You cant pass to yourself!")
                    twitch_bot_utils.printer("%s tried to pass to them-self" % user.lower())
                    return True
            if len(parts) == 1:
                switch(-1)
                return True
            
        #sound commands
        
        song = ''
        #select a random sound
        
        if command == "!randomsound":
            twitch_bot_utils.printer("Random sound")
            song = random.choice(sounds.values())
        #check message for all sound commands
        for sound, file in sounds.iteritems():
            if data.find(sound) != -1:
                twitch_bot_utils.printer("Found %s in %s" % (sound,data))
                song = file
                break #stop after the first sound command is found
        if song != '': #if a sound was selected
            #check for left/right
            left = 1
            right = 1
            if data.find("left") != -1:
                twitch_bot_utils.printer("Found left")
                right = 0
            elif data.find("right") != -1:
                twitch_bot_utils.printer("Found right")
                left = 0
            #Play sound in a thread
            scare = threading.Thread(target=play_sound,args=(song,left,right,admin))
            scare.daemon = True
            scare.start() 
            return True
        
        #select a random scare command
        if command == "!randomscare":
            data = random.choice(['quiet', "rattle", "heart"])
        wait = random.randint(2, 30)
        twitch_bot_utils.printer("Random wait: %s" % wait)
        #Drop the box on me by moving the arm down for 2 seconds, then waiting 20 seconds
        if data.find ( 'quiet' ) != -1 or data.find ( 'door' ) != -1 or data.find ( 'drop' ) != -1 or data.find ( 'gun' ) != -1:
            scare = threading.Thread(target=arduino_scare,args=(10,130,40,254,"Dropping box",1,wait,1,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #Drop the box on me by moving the arm down for 2 seconds, then waiting 20 seconds
        if data.find ( 'brush' ) != -1 or data.find ( 'pants' ) != -1 or data.find ( 'spider' ) != -1 or data.find ( 'crawl' ) != -1:
            scare = threading.Thread(target=arduino_scare,args=(9,130,40,254,"Moving leg servo",1,wait,1,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #Drop the box on me by moving the arm down for 2 seconds, then waiting 20 seconds 
        if data.find ( 'touch' ) != -1 or data.find ( 'shoulder' ) != -1 or data.find ( 'tapping' ) != -1:
            scare = threading.Thread(target=arduino_scare,args=(5,0,180,254,"Moving shoulder servo",1,wait,2,admin))
            scare.daemon = True
            scare.start() 
            return True
        
        #rattle the vibration motor for 2 seconds, then wait 20 seconds
        if data.find ( 'rattle' ) != -1 or data.find ( 'fall' ) != -1 or data.find ( 'rumble' ) != -1 or data.find ( 'vibe' ) != -1:
            scare = threading.Thread(target=arduino_scare,args=(11,1,0,253,"Desk vibe",2,wait,1,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #rattle the smaller vibration motor for 2 seconds, then wait 20 seconds
        if data.find ( 'heart' ) != -1 or data.find ( 'chest' ) != -1 or data.find ( 'buzz' ) != -1 or data.find ( 'neck' ) != -1:
            scare = threading.Thread(target=arduino_scare,args=(3,1,0,253,"Chest vibe",2,wait,1,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #flip the main monitor
        if data.find ( 'flip' ) != -1:
            scare = threading.Thread(target=flip,args=(30+wait,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #disable all monitors
        if data.find ( 'monitor' ) != -1:
            twitch_bot_utils.printer("Monitor scare1")
            scare = threading.Thread(target=turn_off_monitors,args=("Monitors disabled!",wait+3,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #flip the main monitor and switch control (broken atm)
        '''if data.find ( 'flicker' ) != -1:
            flicker()
            return True'''
            
#get current pixel colors and return into a list of lists
def get_pixels():
    global ser
    global writing
    pixels = {}
    
    wait_serial()
    writing = 1
    ser.flushInput()
    writing = 0
    writing_serial("#000%c0" % chr(252))
    wait_serial()
    writing = 1
    for x in range( 0, 30 ):
        line = ser.readline().split(",")
        pixels.update( {line[0] : [ int(line[1]),int(line[2]),int(line[3]) ] } )
    writing = 0
    return pixels

#fade from current color to new color using a number of "frames"
def fade(red,green,blue,steps,wait=2):
    global animating
    diff = {}
    pixels = get_pixels()
    twitch_bot_utils.printer("Fading")
    for x in range(0,30):
        temp = [red-pixels["%s"%x][0],green-pixels["%s"%x][1],blue-pixels["%s"%x][2]]
        diff.update({x:temp})
    for x in range(0, steps+1):
        for y in range(0, 30):
            r=int(round(pixels["%s"%y][0] + ((diff[y][0]/steps)*x)))
            if r<0:
                r=0
            g=int(round(pixels["%s"%y][1] + ((diff[y][1]/steps)*x)))
            if g<0:
                g=0
            b=int(round(pixels["%s"%y][2] + ((diff[y][2]/steps)*x)))
            if b<0:
                b=0
            writing_serial("#%c%c%c%c" % (r,g,b,y))
        writing_serial("!")
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping user command")
            writing_serial("#%c%c%c\xff!" % (red,green,blue))
            animating = 0
            return
        pygame.time.wait(wait)
    writing_serial("#%c%c%c\xff!" % (red,green,blue))
    animating = 0
    
#set the leds to black if in scary mode, fade up from black to white if normal mode
def modedefault():
    global animating
    animating = 1
    if mode == 0:
        fade_thread = threading.Thread(target=fade,args=(0,0,0,100))
        fade_thread.daemon = True
        fade_thread.start()
    if mode == 1:
        fade_thread = threading.Thread(target=fade,args=(255,255,255,100))
        fade_thread.daemon = True
        fade_thread.start() 
    return
    
#return a color from a 255 rainbow palette
def Wheel(WheelPos):
    WheelPos = 255 - WheelPos;
    if WheelPos < 85:
        return [255 - WheelPos * 3, 0, WheelPos * 3];
    elif WheelPos < 170:
        WheelPos -= 85;
        return [0, WheelPos * 3, 255 - WheelPos * 3];
    else:
        WheelPos -= 170;
        return [WheelPos * 3, 255 - WheelPos * 3, 0];

            
def disco():
    global animating
    wait_animating()
    animating = 1
    irc.msg("DISCO PARTY!!!!!!!!")
    for x in range(0, 5): #loop 5 mins
        for y in range(0, 255): #loop through all 255 colors
            rgb = twitch_bot_utils.Wheel(y)
            writing_serial("#%c%c%c\xff!" % (rgb[0],rgb[1],rgb[2]))
            if scaring==1:
                printer("Scare! Stopping user command")
                animating = 0
                return
            pygame.time.wait(5)
    modedefault()
    return
    
def strobe():
    global animating
    wait_animating()
    animating = 1
    irc.msg("SEIZURE PARTY!!!!!!!!")
    for x in range(0, 50): #flicker 200 times, for 30 ms on, then 30ms off
        writing_serial("#\xff\xff\xff\xff!")
        pygame.time.wait(40)
        writing_serial("#\x00\x00\x00\xff!")
        pygame.time.wait(40)
        if scaring==1:
            printer("Scare! Stopping user command")
            animating = 0
            return
    modedefault()
    return

def disco_strobe():
    global animating
    wait_animating()
    animating = 1
    irc.msg("DISCO SEIZURES!!!!!!!!")
    for y in range(0, 85): #loop through all 255 colors
        rgb = twitch_bot_utils.Wheel(y*3)
        writing_serial("#%c%c%c\xff!" % (rgb[0],rgb[1],rgb[2]))
        pygame.time.wait(40)
        writing_serial("#\x00\x00\x00\xff!")
        pygame.time.wait(40)
        if scaring==1:
            printer("Scare! Stopping user command")
            animating = 0
            return
    modedefault()
    return    

def chase(r, g, b,num=6):
    global animating
    wait_animating()
    animating = 1
    twitch_bot_utils.printer("%s,%s,%s" %(r,g,b))
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            for z in range(0,30): #draw the pixels
                if z>y-3 and z<y+3:
                    writing_serial("#%c%c%c%c" % (r,g,b,z))
                else:
                    writing_serial("#\x00\x00\x00%c" % z)
            writing_serial("!")
            if scaring==1:
                printer("Scare! Stopping user command")
                animating = 0
                return
            pygame.time.wait(10)       
        pygame.time.wait(500)
    animating = 0
    return
    
def bounce(r, g, b,num=6):
    global animating
    wait_animating()
    animating = 1
    twitch_bot_utils.printer("%s,%s,%s" %(r,g,b))
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            for z in range(0,30): #draw the pixels
                w = y * 2
                if y > 15:
                    w = (15 - (y - 15)) * 2
                if z>w-3 and z<w+3:
                    writing_serial("#%c%c%c%c" % (r,g,b,z))
                else:
                    writing_serial("#\x00\x00\x00%c" % z)
            writing_serial("!")
            if scaring==1:
                printer("Scare! Stopping user command")
                animating = 0
                return
            pygame.time.wait(10)       
        pygame.time.wait(500)
    animating = 0
    return  
    
def centerchase(r, g, b,num=6):
    global animating
    wait_animating()
    animating = 1
    twitch_bot_utils.printer("%s,%s,%s" %(r,g,b))
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            for z in range(0,30): #draw the pixels
                center = 15-abs(y-15)
                left = 15 + center
                right = 15 - center
                if (z>left-2 and z<left+2) or (z>right-2 and z<right+2):
                    writing_serial("#%c%c%c%c" % (r,g,b,z))
                else:
                    writing_serial("#\x00\x00\x00%c" % z)
            writing_serial("!")
            if scaring==1:
                printer("Scare! Stopping user command")
                animating = 0
                return
            pygame.time.wait(10)       
        pygame.time.wait(500)
    animating = 0
    return
    
def alternate(r1,g1,b1,r2,g2,b2):
    global animating
    wait_animating()
    animating = 1
    twitch_bot_utils.printer("%s,%s,%s,%s,%s,%s" %(r1,g1,b1,r2,g2,b2))
    for y in range( 0, 10 ):
        r1,r2 = r2,r1 #swap colors
        g1,g2 = g2,g1
        b1,b2 = b2,b1
        for x in range( 0, 30 ):
            if x<15: #draw the first color to 0-14
                writing_serial("#%c%c%c%c" % (r1,g1,b1,x)) 
            else: #and the second to 15-30
                writing_serial("#%c%c%c%c" % (r2,g2,b2,x))
        writing_serial("!")
        if scaring==1:
            printer("Scare! Stopping alternate")
            animating = 0
            return
        time.sleep(0.5)
    modedefault()
    return
    
def disco_alternate():
    global animating
    wait_animating()
    animating = 1
    w=0
    x=128
    for y in range(0, 255): #loop through all 255 colors
        if (y%24)==0:
            w,x = x,w
        rgb = twitch_bot_utils.Wheel((y+x)%255)
        rgb2 = twitch_bot_utils.Wheel((y+w)%255)
        for z in range( 0, 30 ):
            if z<15: #draw the first color to 0-14
                writing_serial("#%c%c%c%c" % (rgb[0],rgb[1],rgb[2],z)) 
            else: #and the second to 15-30
                writing_serial("#%c%c%c%c" % (rgb2[0],rgb2[1],rgb2[2],z)) 
        if scaring==1:
            printer("Scare! Stopping user command")
            animating = 0
            return
        writing_serial("!")    
        pygame.time.wait(5)
    modedefault()
    return

#fire animation using 2 colors
#todo add gradients
def fire(r1,g1,b1,r2,g2,b2):
    global animating
    wait_animating()
    animating = 1
    irc.msg("FIRE!!!")
    for y in range( 0, 30 ):
        for x in range( 0, 30 ):
            r = random.randrange(2)
            if r==1:
                writing_serial("#%c%c%c%c" % (r1,g1,b1,x) )
            else:
                writing_serial("#%c%c%c%c" % (r2,g2,b2,x) )
        writing_serial("!")
        if scaring==1:
            printer("Scare! Stopping fire")
            animating = 0
            return
        time.sleep(0.1)
    modedefault()
    return
    
#disco fire
#todo add gradients
def disco_fire():
    global animating
    wait_animating()
    animating = 1
    irc.msg("FIRE!!!")
    for y in range( 0, 30 ):
        for x in range( 0, 30 ):
            c = twitch_bot_utils.Wheel(((random.randint(1, 32)+random_color)*7)%255)
            writing_serial("#%c%c%c%c" % (c[0],c[1],c[2],x) )
        writing_serial("!")
        if scaring==1:
            printer("Scare! Stopping disco fire")
            animating = 0
            return
        time.sleep(0.1)
    modedefault()
    return
    
def allleds(r,g,b,wait):
    global animating
    wait_animating()
    animating = 1
    writing_serial("#%c%c%c\xff!" % (r,g,b) )
    user_wait(wait)
    modedefault()

def user_stack_consumer():
    global user_stack

    while True:
        if len(user_stack)>0 and scaring==0 and animating==0:
            twitch_bot_utils.printer("user stack consumer DEBUG!!!!!!!!!!!: %s %s %s" % (len(user_stack),scaring,animating))
            user,data = user_stack.pop(0)
            twitch_bot_utils.printer("Checking a buffered string: %s" % data)
            user_commands(user,data)
        time.sleep(1)
        
twitch_profile("#Commands for everyone (even if you don't have control) Scary & Normal mode  ")
twitch_profile("")
twitch_profile("**disco**: plays a crazy color animation  ")
twitch_profile("**disco fire**: plays another crazy color animation  ")
twitch_profile("**disco strobe**: plays yet another crazy color animation  ")
twitch_profile("**fire(red,blue)** : plays a fire animation with two colors ")
twitch_profile("**strobe** : plays a strobe animation  ")
twitch_profile("**rgb(yellow)** : Lets users pick a specific color  ")
twitch_profile("**chase(green)** : Lets users play a \"chase\" animation with a specific color  (chase also lets you use 3 color commands to chase in a row)")
twitch_profile("**centerchase(blue)** : Same as chase, but starts in the center and goes out from both left and right")
twitch_profile("**alternate(green,purple)** : plays an alternating animation (lights half the leds with one color, and the other, with the second)  ")
twitch_profile("")
twitch_profile("All colors/commands accept 0-255,0-255,0-255 rgb, as well as html color codes (copy pasted from w3's html color codes)  ")
twitch_profile("")
twitch_profile("For example: alternate(red,blue), will do the same thing as alternate(255,0,0,0,0,255)  ")
twitch_profile("")
twitch_profile("If you have an idea for new rules/scares/animations/things I should let viewers control while playing games... Let me know, I'm trying to add at least one new feature every night to keep things interesting.")

#commands accessible by all users
def user_commands(user,data):
    global user_stack
    global animating
    
    
    parts = data.lower().split()
    command = parts[0][1:]
    
    twitch_bot_utils.printer("Checking %s for user commands..." % data)
    
    #start commands
    if data.find ( 'test' ) != -1:
        irc.msg("test to you too!")
        return True
    
    #Scary mode only commands
    if mode == 0:
        if command == "!whosgotit":
            irc.msg("%s is currently in control!" % master)
            return True
        #opt a user in, and switch if they were in control
        if command == "!optin":
            opt(user,True)
            irc.msg("%s is now opted in!" %user)
            return True
        #allow a user to optout
        if command == "!optout":
            opt(user,False)
            irc.msg("%s is now opted out!" %user)
            return True
        #let viewers know how much time is left    
        if command == "!timeleft":
            timeleft = 300 - (time.time() - counter)
            irc.msg("%s has %s seconds left!" % (master,round(timeleft)))
            return True

    #Get current streaming game
    if command == "!nextgame" or ( data.find ( 'what game' ) != -1 and data.find ( 'next' ) != -1 ):
        irc.msg("The next game is: %s!" % get_next_game())
        return True
    
    if command == "!game" or data.find ( 'what game' ) != -1:
        irc.msg("The current game is: %s" % get_game())
        return True
    
    if command == "!spiff":
        elapsed = alert.notify()
        if elapsed > 0:
            irc.msg("Spiff was just notified %s seconds ago!" % elapsed )
        return True
        
    if scaring == 1 or animating == 1:
        twitch_bot_utils.printer("Busy, adding to stack")
        user_stack.append([user,data])
        #while len(user_stack)>5:
            #user_stack.pop()
        del user_stack[5:]
        temp = []
        for stack in user_stack:
            temp.append(stack[1])
        twitch_bot_utils.printer(string.join(temp," - "))
        return 
    else:
        twitch_bot_utils.printer("No scare or animation currently, checking for animations")
        #disco rainbow colors
        if data.find ( 'disco' ) != -1:
            if data.find ( 'strobe' ) != -1:
                disco_strobe()
            elif data.find ( 'fire' ) != -1:
                disco_fire()
            elif data.find ( 'alternate' ) != -1:
                disco_alternate()
            else:
                disco()
            return True

        #flickr strobe
        if data.find ( 'strobe' ) != -1:
            strobe()
            return True
                
        m = re.search('(\w+)\((.+(?:\|[a-zA-Z0-9#]+)*)\)',data,re.IGNORECASE)
        if m:
            twitch_bot_utils.printer("regex passed")
            parts = m.group(2).split("|")
            if m.group(1).lower()=="chase":
                if len(parts)>0:
                    while len(parts)>6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part,random_color)
                        if rgb:
                            num = round(6/len(parts))
                            chase(rgb[0],rgb[1],rgb[2],int(num))
                            time.sleep(1)
                        else:
                            twitch_bot_utils.printer("Invalid color: %s" % part)
                    modedefault()
                    return True
                else:
                    twitch_bot_utils.printer("Not enough colors to chase!")
            if m.group(1).lower()=="centerchase":
                if len(parts)>0:
                    while len(parts)>6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part,random_color)
                        if rgb:
                            num = round(6/len(parts))
                            centerchase(rgb[0],rgb[1],rgb[2],int(num))
                            time.sleep(1)
                        else:
                            twitch_bot_utils.printer("Invalid color: %s" % part)
                    modedefault()
                    return True
                else:
                    twitch_bot_utils.printer("Not enough colors to centerchase!")
            if m.group(1).lower()=="bounce":
                if len(parts)>0:
                    while len(parts)>6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part,random_color)
                        if rgb:
                            num = round(6/len(parts))
                            bounce(rgb[0],rgb[1],rgb[2],int(num))
                            time.sleep(1)
                        else:
                            twitch_bot_utils.printer("Invalid color: %s" % part)
                    modedefault()
                    return True
                else:
                    twitch_bot_utils.printer("Not enough colors to bounce!")
            if m.group(1).lower()=="cycle":
                if len(parts)>0:
                    while len(parts)>6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part,random_color)
                        if rgb:
                            num = round(6/len(parts))
                            allleds(rgb[0],rgb[1],rgb[2],num)
                        else:
                            twitch_bot_utils.printer("Invalid color: %s" % part)
                    return True
                else:
                    twitch_bot_utils.printer("Not enough colors to cycle!")
            if len(parts)==1:
                rgb = twitch_bot_utils.convertcolor(parts[0],random_color)
                if rgb:
                    if m.group(1).lower()=="rgb":
                        allleds(rgb[0],rgb[1],rgb[2],5)
                        time.sleep(1)
            if len(parts)==2:
                rgb = twitch_bot_utils.convertcolor(parts[0],random_color)
                rgb2 = twitch_bot_utils.convertcolor(parts[1],random_color)
                if rgb: 
                    if rgb2:
                        if m.group(1).lower()=="fire":
                            fire(rgb[0],rgb[1],rgb[2],rgb2[0],rgb2[1],rgb2[2])
                            time.sleep(1)
                            return True
                        if m.group(1).lower()=="alternate":
                            alternate(rgb[0],rgb[1],rgb[2],rgb2[0],rgb2[1],rgb2[2])
                            time.sleep(1)
                            return True
                    else:
                        twitch_bot_utils.printer("Invalid color: %s" % parts[1])
                else:
                    twitch_bot_utils.printer("Invalid color: %s" % parts[0])
                    return True
        #html color keys (single color, no animation)
        #todo replace with color converter
        for key, value in sorted(html_colors.colors.iteritems()):
            if data.find ( key.lower() ) != -1:
                animating = 1
                twitch_bot_utils.printer("key: %s value: %s : %s,%s,%s" % (key,value,int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)))
                irc.msg("%s!!!" % key.upper())
                writing_serial("#%c%c%c\xff!" % (int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)) )
                user_wait(5)
                modedefault()
                return True
                
def last_seen(user,data):
    db.updateLastSeen(user)
    
#constants
master = twitch_auth.get_streamer()
alert = twitch_bot_utils.notification("./sounds/OOT_MainMenu_Select.ogg",60)
user_stack = []
pass_counter = 3
random_color=1
scaring = 0
switching = 0
writing = 0
animating = 0
next = None
mode = twitch_bot_utils.scaryDay()

#serial stuff
#todo: add code to find arduino dynamically
ser = serial.Serial("Com4", 115200)

#db stuff
db = twitch_db.twitchdb(twitch_auth.get_db_user(),twitch_auth.get_db_pass(),"127.0.0.1","twitch")

#Display init for flicker
#pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)
#pygame.init()
#setup audio
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
twitch_bot_utils.printer("Initiated Pygame Mixer:")
twitch_bot_utils.printer(pygame.mixer.get_init())
twitch_bot_utils.printer(pygame.mixer.get_num_channels())

#Midi initialization 
#pygame.midi.init()
#midi_device = getMidi("MIDISPORT 1x1 In")
#twitch_bot_utils.printer("Got midi: %s" % midi_device)
#midi = pygame.midi.Input(midi_device)

irc = twitch_bot_utils.irc_connection("irc.twitch.tv","6667",twitch_auth.get_bot(),twitch_auth.get_oauth(),
    twitch_auth.get_streamer(),[autoOptIn,last_seen,admin_commands,master_commands,user_commands])    
    
#Midi Thread start
#t = threading.Thread(target=midiThread)
#t.daemon = True
#t.start()

#Switch Timer Thread start
t2 = threading.Thread(target=mastertimer)
t2.daemon = True
t2.start()


twitch_bot_utils.printer("Blacking out all pixels!")
writing_serial("#\x00\x00\x00\xff!")
time.sleep(2)
modedefault()
time.sleep(1)
twitch_bot_utils.printer("READY!")


user_stack_thread = threading.Thread(target=user_stack_consumer)
user_stack_thread.daemon = True
user_stack_thread.start()

#Main loop
while True:
    #ser.flushInput() #ignore serial input, todo: log serial input without locking loop
    
    time.sleep(1)