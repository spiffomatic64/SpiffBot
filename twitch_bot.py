import re
import time
import serial
import pygame
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
import twitch_bot_midi
import twitch_bot_serial
import subprocess
import twitch_volume
import ctypes
import twitch_bot_input

next_scary_game = "http://strawpoll.me/3743145"

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
"normalzombie" : "zombie_scare.ogg",
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
"subtlebirds" : "subtle_birds.ogg",
"scream" : "female_scream.ogg",
"footsteps" : "footsteps.ogg",
"rezombie" : "rezombie.ogg",
"recreature" : "recreature.ogg",
"subsonic" : "subsonic.ogg",
"mgalert" : "metalgearalert.ogg"
}

class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_1

XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

vibration = XINPUT_VIBRATION(0, 0)
XInputSetState(0, ctypes.byref(vibration))

def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
    XInputSetState(controller, ctypes.byref(vibration))

def set_animating(status):
    global animating
    
    twitch_bot_utils.printer("Setting animating to: %s" % status)
    animating = status

def setMode(type):
    global mode
    
    if type == "scary" or type == 0:
        mode = 0
        twitch_bot_utils.printer("Scary time!")
        counter = time.time()
        master=auth.get_streamer()
        irc.msg("ITS SCARY TIME!!!")
        modedefault()
        return True
    if type == "troll" or type == 1:
        mode = 1
        twitch_bot_utils.printer("Troll time!")
        irc.msg("LETS TROLL SPIFF!!!")
        modedefault()
        return True
    if type == "light" or type == 2:
        mode = 2
        twitch_bot_utils.printer("Lights time!")
        irc.msg("LIGHTS ARE PRETTY!!!")
        modedefault()
        return True

def inBetween(stuff,first,last):
    return stuff[stuff.find(first)+len(first):stuff.find(last)]

def get_next_game():
    try:
        url = "http://api.twitch.tv/api/channels/%s/panels" % auth.get_streamer()
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
        return False
    except:
        return False

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
twitch_profile("Spiffbot has 3 main modes: Scary (Thurs-Sunday), Troll (Mon-Weds), Light (Only control of lights)")
twitch_profile("")

def opt(user,inout,passed=None):
    user=user.lower()
    if inout:
        if not db.getUserOpted(user):
            db.updateUserOpted(user,1)
            if master==auth.get_bot():
                switch(user)
    else:
        if user == auth.get_streamer():
            switch()
        elif db.getUserOpted(user):
            db.updateUserOpted(user,0)
            if user == master:
                if passed:
                    switch(passed)
                else:
                    switch()
                
def autoOptIn(user,data):
    global next
    if user not in db.getUsers():
        twitch_bot_utils.printer("Auto Opting %s in!" % user)
        opt(user,True)
        irc.msg("Check out this 1 minute video that explains my stream! https://www.youtube.com/watch?v=q0q8SML6d_I")
        twitch_bot_utils.printer("Setting next user to: %s" % user)
        irc.msg("Giving next control to our newest viewer: %s" % user)
        next=user
        return True

def scare_lock(status):
    global scaring
    twitch_bot_utils.printer("Setting scaring: %s" % status)
    scaring = status

        
def wait_animating():
    while animating==1:
        pygame.time.wait(10)

def user_wait(duration):
    stop = time.time()+duration
    while time.time() < stop and scaring==0:
        time.sleep(0.5)
    return

#gets a "live" list of viewers in chat
def get_viewers(opted=True):
    url = "https://tmi.twitch.tv/group/user/%s/chatters" % auth.get_streamer()
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
        if db.getUserOpted(viewer) and viewer!=auth.get_bot() and viewer!=auth.get_streamer():
            viewers.append(viewer)
            twitch_bot_utils.printer(viewer)
    return viewers

# This will pick a random user from those that are opted in and display the winner in chat
def raffle():
    users_for_raffle = get_viewers(opted=True)
    irc.msg('And the winner is ...'+str(random.choice(users_for_raffle)))
    
def get_game():
    try:
        url = "https://api.twitch.tv/kraken/streams/%s" % auth.get_streamer()
        twitch_bot_utils.printer("Checking game...")
        data = requests.get(url=url)
        binary = data.content
        output = json.loads(binary)
        game = output['stream']['game']
        return game
    except:
        return False
    
#Thread responsible for switching control
def mastertimer():
    global counter
    global master
    global switching
    global mode

    warn_timer = 0
    counter = time.time()
    
    while True:
        if mode <= 1:
            elapsed = time.time() - counter
            if elapsed >390 or elapsed<0:
                scare_lock(0)
                switching = 0
                twitch_bot_utils.printer("Elapsed out of bounds!: %s" % elapsed);
                
            if scaring == 0 and switching == 0:
                #every 5 minutes switch control, and remove master from optedin list 300
                if elapsed>300:
                    if master!=auth.get_bot():
                        irc.msg("5 Minutes elapsed! Switching control, and opting %s out!" % master)  
                        twitch_bot_utils.printer("Passing control and opting out %s(due to timeout from mastertimer)" % master)
                        if last_pass:
                            twitch_bot_utils.printer("Passing back to user %s" % last_pass)
                            opt(master,False,last_pass)
                        else:
                            opt(master,False)
                    twitch_bot_utils.printer("Master switch")
                    counter = time.time()
                    warn_timer = 0
                #every 2.5 minutes warn the user in control 150 (make sure to only warn once)
                elif elapsed>150 and warn_timer == 0:
                    if master!=auth.get_bot():
                        try:
                            viewers = get_viewers()
                            if master in viewers:
                                irc.msg( "2.5 Minutes left %s!" % master)  
                                twitch_bot_utils.printer("Sending 2.5 minute warning")
                            else:
                                irc.msg( "%s is not in viewer list, Switching control!" % master)  
                                if last_pass:
                                    switch(last_pass)
                                else:
                                    switch(-1)
                                counter = time.time()
                        except:
                            irc.msg( "2.5 Minutes left %s!" % master)  
                            twitch_bot_utils.printer("Sending 2.5 minute warning")
                    warn_timer = 1
                
                twitch_bot_utils.printer(elapsed)
                twitch_bot_utils.printer(last_pass)
        time.sleep(1)
        
#switch control to a random person (or specific person if specified)
def switch(user="",pass_control=0):
    global counter
    global master
    global switching
    global next
    global pass_counter
    global last_pass
    
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
            irc.msg("Too many passes to specific users, use a command, or !pass without a username") 
            switching = 0
            return
            
        old = master
        twitch_bot_utils.printer("getting viewers")
        try:
            viewers = get_viewers()
        except:
            twitch_bot_utils.printer("*************Twitch Api is borked*************")
            master=auth.get_bot()
            last_pass = None
            twitch_bot_utils.printer("%s is now in control!" % master)
            irc.msg("%s is now in control!" % master) 
            twitch_bot_utils.printer("Switching from %s to %s" % (old,master))
            db.updateLastControl(master)
            counter = time.time()
            switching = 0
            return

        #remove the current controller from available viewers to prevent switching to the same person
        if master in viewers:
            viewers.remove(master)
            
        #add logic for fairness

        
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
            last_pass = None
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
                master=auth.get_bot()
            last_pass = None
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
    global stayAlive
    
    #if user.lower() == auth.get_streamer():
    if auth.is_admin(user):
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
        if command == "!restart" or command == "!reload":
            stayAlive = 0
        if command == "!whosoptedin":
            optedin = ""
            try:
                viewers = get_viewers()
                for optins in db.getOptedUsers():
                    if optins in viewers:
                        optedin = "%s %s " % (optedin,optins)
                irc.msg("%s" % optedin)
            except:
                irc.msg("Twitch api is borked :(")
            return True
        if command == "!midi":
            twitch_bot_utils.printer(midi.toggleMidi())
        if command == "!raffle":
            raffle()
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
            #change mode between scary troll and light
            if command == "!mode":
                if setMode(parts[1]):
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
    
#Flip the monitor using winapi's
def wiggle(times=20,scare=0):
    scare_lock(1)
    scare_status("Wiggling window!")
    #manually selecting monitor 2 (Windows reports monitor 2, is actually 1)
    while True:
        time.sleep(0.001)
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                twitch_bot_utils.printer("Found window! hwnd: %s" % hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                x = rect[0]
                y = rect[1]
                w = rect[2] - x
                h = rect[3] - y
                twitch_bot_utils.printer("x: %d y: %d w: %d h: %d" % (x,y,w,h))
                break
            else:
                twitch_bot_utils.printer("No windows %s" % hwnd)
        except win32gui.error:
            twitch_bot_utils.printer("Error: window not found")
            
    for i in range(0,times):
        win32gui.SetWindowPos(hwnd,None,random.randint(-2312, 2712-w),random.randint(0, 1024-h),0,0,1)
        time.sleep(1)
    win32gui.SetWindowPos(hwnd,None,x,y,w,h,1)
    scare_status(-1)
    scare_lock(0)
    if scare==0:
        switch()
    return
    
#Slow strobe the monitor effect
def flicker(times=5,scare=0):
    twitch_bot_utils.printer("Flicker!")
    scare_lock(1)
    scare_status("Flickering Monitor!")
    p = subprocess.Popen(["python", "twitch_bot_flicker.py"])
    p.wait()
    scare_status(-1)
    scare_lock(0)
    if scare==0:
        switch()
        
def dark(times=5,scare=0):
    twitch_bot_utils.printer("Dimming Monitor!")
    scare_lock(1)
    scare_status("Dimming Monitor!")
    p = subprocess.Popen(["python", "twitch_bot_dim.py"])
    p.wait()
    scare_status(-1)
    scare_lock(0)
    if scare==0:
        switch()
        
def box(times=5,scare=0):
    twitch_bot_utils.printer("Drawing Box!")
    scare_lock(1)
    scare_status("Drawing Blind Spot!")
    p = subprocess.Popen(["python", "twitch_bot_box.py"])
    p.wait()
    scare_status(-1)
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
        ser.write("#%c%c\x00%c" % (pin,start,command))
        time.sleep(dur)
        ser.write("#%c%c\x00%c" % (pin,stop,command))
    time.sleep(status_length)
    scare_status(-1)
    time.sleep(wait-status_length)
    scare_lock(0)
    if scare==0:
        switch()
        
def spasm_scare(wait,scare):
    scare_lock(1)
    scare_status("Spasm!!!!!")
    twitch_bot_utils.printer("Spasm scare, scare=%s" % scare)
    status_length = 3
    ser.write("#%c%c\x00%c" % (10,130,254))
    ser.write("#%c%c\x00%c" % (9,130,254))
    ser.write("#%c%c\x00%c" % (3,0,254))
    ser.write("#%c%c\x00%c" % (11,1,253))
    ser.write("#%c%c\x00%c" % (5,0,254))
    time.sleep(status_length)
    ser.write("#%c%c\x00%c" % (10,40,254))
    ser.write("#%c%c\x00%c" % (9,40,254))
    ser.write("#%c%c\x00%c" % (3,180,254))
    ser.write("#%c%c\x00%c" % (11,0,253))
    ser.write("#%c%c\x00%c" % (5,180,254))
    time.sleep(status_length)
    scare_status(-1)
    time.sleep(wait-status_length)
    scare_lock(0)
    if scare==0:
        switch()
    
def play_sound(sound,left,right):
    twitch_bot_utils.printer(pygame.mixer.get_init())
    twitch_bot_utils.printer("Playing sound %s" % sound)
    mixer = pygame.mixer.Sound("./sounds/%s" % sound)
    channel = mixer.play()
    channel.set_volume(left,right)

    clock = pygame.time.Clock()
    # wait for playback to be finished
    while channel.get_busy():
       clock.tick(30)
        
def sound_scare(sound,left,right,scare=0):
    scare_lock(1)
    play_sound(sound,left,right)
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
        
def change_volume(wait,level,scare=0):
    scare_lock(1)
    scare_status("Changing volume!")
    vol_scare.set_volume(level)
    time.sleep(wait)
    vol_scare.set_volume(-20.0)
    scare_status(-1)
    scare_lock(0)
    if scare==0:
        switch()
    return
    
def vibrate(wait,left,right,scare=0):
    scare_lock(1)
    scare_status("Vibrating controller!")
    stop = time.time()+wait
    while time.time() < stop:
        time.sleep(0.5)
        set_vibration(0,left,right)
    set_vibration(0,0,0)
    scare_status(-1)
    scare_lock(0)
    if scare==0:
        switch()
    return
    
def wasd(wait,scare=0):
    scare_lock(1)
    scare_status("Random WASD!")
    
    times = random.randint(30, 60)
    keys = [[0x11,0x57],[0x1e,0x41],[0x1f,0x53],[0x20,0x44]]
    
    stop = time.time()+times
    while time.time() < stop:
        key = random.choice(keys)
        twitch_bot_input.PressKey(key[0],key[1],True)
        time.sleep(random.randint(1, 10)/10.0)
        twitch_bot_input.PressKey(key[0],key[1],False)
        time.sleep(random.randint(1, 8)/2.0)
    scare_status(-1)
    scare_lock(0)
    if scare==0:
        switch()
    return
    
def scare_status(status):
    f = open('scarestatus.txt', 'w')
    if status==-1:
        f.truncate()
    else:
        f.write(status)
    f.close()
      
#Twitch profile generator
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
twitch_profile("**rattle**, **fall**, or **desk** :Turns on a vibration motor I took out of an xbox controller, that will rattle around making noise/vibrations/ and movement out of the corner of my eye... Will most likely also scare the pants off me...")
twitch_profile("")
twitch_profile("**back**, **spine**, **buzz**, **neck** : This will move a servo (twice) attached to my neck that emulates someone tapping on it")
twitch_profile("")
twitch_profile("**flip** : Flips my main monitor image 180 degrees (vertically) for 30 full seconds (everything should look normal on the stream though)")
twitch_profile("")
twitch_profile("**monitor** : Turns off all monitors at once, for a solid 2.5 seconds")
twitch_profile("")
twitch_profile("**flicker** : Strobes the monitor (30 frames of black 10 frames of video)")
twitch_profile("")
twitch_profile("**volume**, **mute** : Disables audio completely (for me only) for a short period of time (cheatme1)")
twitch_profile("")
twitch_profile("**spasm**, **shake**, **shiver** or **electrocute&& : Enables all scares for a short second (Falconslaver87)")
twitch_profile("")
twitch_profile("##Scary sound commands for the user in \"Control\"")
twitch_profile("You can preview the sounds [Here](http://spiffomatic64.com/twitch/sounds)")
twitch_profile("")
twitch_profile("**!randomsound** : Picks a sound scare randomly")
twitch_profile("")

sound_buffer = ""
for sound, file in sounds.iteritems():
    sound_buffer = "%s**%s**, " % (sound_buffer,sound)
twitch_profile(sound_buffer)
twitch_profile("")
twitch_profile("##Other commands for the user in \"Control\"")
twitch_profile("**!pass** : allows you to pass control on to the person who has not had control in the longest instead of using it yourself. If you add a username after !pass, you can pass control to someone specifically") 

#commands only accessible by the user in control  
def master_commands(user,data):
    global master
    global sounds
    global last_pass
    
    #check that the user is the master, and we are in scary mode
    if scaring==0 and switching==0 and (user.lower() == master.lower() or user.lower()==auth.get_streamer()) and mode <= 1:
        if user.lower()==auth.get_streamer():
            twitch_bot_utils.printer("User is admin, dont switch")
            admin = 1
        else:
            admin = 0 
        twitch_bot_utils.printer("User is in control, checking for commands")
        parts = data.lower().split()
        command = parts[0][1:]
        
        twitch_bot_utils.printer("%s == %s" % (user.lower(), master.lower()))
        #allow a user to pass to someone else, or to someone random
        if command == "!passnew":
            twitch_bot_utils.printer("%s pasing to whoever has not had control in the longest!" % user.lower())
            switch(-1)
            return True
            
        if command == "!pass":
            if len(parts) == 1:
                twitch_bot_utils.printer("%s pasing to whoever has not had control in the longest!" % user.lower())
                switch(-1)
                last_pass = user
                return True
            if len(parts) == 2:
                if user.lower() != parts[1].lower():
                    if parts[1].lower() in db.getOptedUsers():
                        twitch_bot_utils.printer("%s pasing to %s" % (user.lower(),parts[1].lower()))
                        switch(parts[1],1)
                        last_pass = user
                        return True
                    elif parts[1].lower() == "new" or parts[1].lower() == "newuser":
                        twitch_bot_utils.printer("%s pasing to whoever has not had control in the longest!" % user.lower())
                        switch(-1)
                        last_pass = user
                        return True
                    else:
                        irc.msg("Can't pass, %s is opted out!" % parts[1].lower())
                        twitch_bot_utils.printer("%s tried to pass to %s who is opted out" % (user.lower(),parts[1].lower()))
                        return True
                else:
                    irc.msg("You cant pass to yourself!")
                    twitch_bot_utils.printer("%s tried to pass to them-self" % user.lower())
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
            scare = threading.Thread(target=sound_scare,args=(song,left,right,admin))
            scare.daemon = True
            scare.start() 
            return True
        
        #select a random scare command
        if command == "!randomscare" and mode == 0:
            data = random.choice(["drop","brush","tapping","spine","rattle","spasm","vibe","flip","monitor","mute","wiggle","flicker","dark","blindspot","wasd"])
            
        if command == "!randomtroll" and mode == 1:
            data = random.choice(["flip","monitor","mute","wiggle","flicker","dark","blindspot","wasd"])
        
        wait = random.randint(4, 30)
        twitch_bot_utils.printer("Random wait: %s" % wait)
        
        #flip the main monitor
        if data.find ( 'flip' ) != -1:
            scare = threading.Thread(target=flip,args=(30+wait,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #disable all monitors
        if data.find ( 'monitor' ) != -1:
            twitch_bot_utils.printer("Monitor scare!")
            scare = threading.Thread(target=turn_off_monitors,args=("Monitors disabled!",wait+3,admin))
            scare.daemon = True
            scare.start() 
            return True
        #changes volume
        if data.find ( 'volume' ) != -1 or data.find ( 'mute' ) != -1:
            twitch_bot_utils.printer("Setting Volume!")
            scare = threading.Thread(target=change_volume,args=(wait+3,-50.0,admin))
            scare.daemon = True
            scare.start() 
            return True    
            
        #Wiggle active window
        if data.find ( 'wiggle' ) != -1:
            twitch_bot_utils.printer("WIGGLE WIGGLE!!")
            scare = threading.Thread(target=wiggle,args=(wait+3,admin))
            scare.daemon = True
            scare.start() 
            return True 
            
        #flip the main monitor and switch control (broken atm)
        if data.find ( 'flicker' ) != -1:
            scare = threading.Thread(target=flicker,args=(wait+3,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #Dim the main monitor
        if data.find ( 'dark' ) != -1:
            scare = threading.Thread(target=dark,args=(wait+3,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #Dim the main monitor
        if data.find ( 'blindspot' ) != -1:
            scare = threading.Thread(target=box,args=(wait+3,admin))
            scare.daemon = True
            scare.start() 
            return True
            
        #send random wasd keys
        if data.find ( 'wasd' ) != -1:
            scare = threading.Thread(target=wasd,args=(wait+3,admin))
            scare.daemon = True
            scare.start() 
            return True
        
        if mode == 0:
            #Drop the box on me by moving the arm down for 2 seconds, then waiting 20 seconds
            if data.find ( 'quiet' ) != -1 or data.find ( 'door' ) != -1 or data.find ( 'drop' ) != -1 or data.find ( 'gun' ) != -1:
                scare = threading.Thread(target=arduino_scare,args=(10,130,40,254,"Dropping box",1,wait,1,admin))
                scare.daemon = True
                scare.start() 
                return True
                
            #Move the servo attached to my legs
            if data.find ( 'brush' ) != -1 or data.find ( 'pants' ) != -1 or data.find ( 'spider' ) != -1 or data.find ( 'crawl' ) != -1:
                scare = threading.Thread(target=arduino_scare,args=(9,130,40,254,"Moving leg servo",1,wait,1,admin))
                scare.daemon = True
                scare.start() 
                return True
                
            #Move the servo attached to my shoulder
            if data.find ( 'touch' ) != -1 or data.find ( 'shoulder' ) != -1 or data.find ( 'tapping' ) != -1:
                scare = threading.Thread(target=arduino_scare,args=(3,0,180,254,"Moving shoulder servo",1,wait,3,admin))
                scare.daemon = True
                scare.start() 
                return True
            
            #rattle the vibration motor for 2 seconds, then wait 20 seconds
            if data.find ( 'rattle' ) != -1 or data.find ( 'fall' ) != -1 or data.find ( 'desk' ) != -1:
                scare = threading.Thread(target=arduino_scare,args=(11,1,0,253,"Desk vibe",2,wait,1,admin))
                scare.daemon = True
                scare.start() 
                return True
                
            #Move the servo down my shirt
            if data.find ( 'back' ) != -1 or data.find ( 'spine' ) != -1 or data.find ( 'buzz' ) != -1 or data.find ( 'neck' ) != -1:
                scare = threading.Thread(target=arduino_scare,args=(5,0,180,254,"Moving spine servo",1,wait,3,admin))
                scare.daemon = True
                scare.start() 
                return True
                
            #rattle the smaller vibration motor for 2 seconds, then wait 20 seconds
            if data.find ( 'spasm' ) != -1 or data.find ( 'shake' ) != -1 or data.find ( 'shiver' ) != -1 or data.find ( 'electrocute' ) != -1:
                scare = threading.Thread(target=spasm_scare,args=(wait,admin))
                scare.daemon = True
                scare.start() 
                return True
                
            if data.find ( 'vibe' ) != -1:
                left = 0
                right = 0
                if data.find ( 'left' ) != -1:
                    left = 1
                if data.find ( 'right' ) != -1:
                    right = 1
                if left==0 and right==0:
                    left = 1
                    right = 1
                if data.find ( 'soft' ) != -1:
                    left = left * 0.3
                    right = right * 0.3
                
                scare = threading.Thread(target=vibrate,args=(wait+3,left,right,admin))
                scare.daemon = True
                scare.start() 
                return True

#fade from current color to new color using a number of "frames"
def fade(red,green,blue,steps,wait=2):
    twitch_bot_utils.printer("Starting Fade")
    diff = {}
    pixels = ser.get_pixels()
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
            ser.write("#%c%c%c%c" % (r,g,b,y))
        ser.write("!")
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping user command")
            ser.write("#%c%c%c\xff!" % (red,green,blue))
            set_animating(0)
            return
        pygame.time.wait(wait)
    ser.write("#%c%c%c\xff!" % (red,green,blue))
    set_animating(0)
    
#set the leds to black if in scary mode, fade up from black to white if normal mode
def modedefault():
    set_animating(1)
    if mode == 0:
        fade_thread = threading.Thread(target=fade,args=(0,0,0,100))
        fade_thread.daemon = True
        fade_thread.start()
    if mode >= 1:
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
    wait_animating()
    set_animating(1)
    irc.msg("DISCO PARTY!!!!!!!!")
    for x in range(0, 5): #loop 5 mins
        for y in range(0, 255): #loop through all 255 colors
            rgb = twitch_bot_utils.Wheel(y)
            ser.write("#%c%c%c\xff!" % (rgb[0],rgb[1],rgb[2]))
            if scaring==1:
                twitch_bot_utils.printer("Scare! Stopping user command")
                modedefault()
                return
            pygame.time.wait(5)
    modedefault()
    return
    
def strobe():
    wait_animating()
    set_animating(1)
    irc.msg("SEIZURE PARTY!!!!!!!!")
    for x in range(0, 50): #flicker 200 times, for 30 ms on, then 30ms off
        ser.write("#\xff\xff\xff\xff!")
        pygame.time.wait(40)
        ser.write("#\x00\x00\x00\xff!")
        pygame.time.wait(40)
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping user command")
            set_animating(0)
            return
    modedefault()
    return

def disco_strobe():
    wait_animating()
    set_animating(1)
    irc.msg("DISCO SEIZURES!!!!!!!!")
    for y in range(0, 85): #loop through all 255 colors
        rgb = twitch_bot_utils.Wheel(y*3)
        ser.write("#%c%c%c\xff!" % (rgb[0],rgb[1],rgb[2]))
        pygame.time.wait(40)
        ser.write("#\x00\x00\x00\xff!")
        pygame.time.wait(40)
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping user command")
            set_animating(0)
            return
    modedefault()
    return    

def chase(r, g, b,num=6):
    wait_animating()
    set_animating(1)
    twitch_bot_utils.printer("%s,%s,%s" %(r,g,b))
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            for z in range(0,30): #draw the pixels
                if z>y-3 and z<y+3:
                    ser.write("#%c%c%c%c" % (r,g,b,z))
                else:
                    ser.write("#\x00\x00\x00%c" % z)
            ser.write("!")
            if scaring==1:
                twitch_bot_utils.printer("Scare! Stopping user command")
                set_animating(0)
                return
            pygame.time.wait(10)       
        pygame.time.wait(500)
    set_animating(0)
    return
    
def disco_chase(num=6):
    wait_animating()
    set_animating(1)
    twitch_bot_utils.printer("Disco Chase")
    irc.msg("DISCO CHASES!!!!!!!!")
    color=0
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            color=color+10
            if color>255:
                color=0
            rgb = twitch_bot_utils.Wheel(color)
            for z in range(0,30): #draw the pixels
                if z>y-3 and z<y+3:
                    ser.write("#%c%c%c%c" % (rgb[0],rgb[1],rgb[2],z))
                else:
                    ser.write("#\x00\x00\x00%c" % z)
            ser.write("!")
            if scaring==1:
                twitch_bot_utils.printer("Scare! Stopping user command")
                set_animating(0)
                return
            pygame.time.wait(10)       
        pygame.time.wait(500)
    set_animating(0)
    modedefault()
    return
    
def bounce(r, g, b,num=6):
    wait_animating()
    set_animating(1)
    twitch_bot_utils.printer("%s,%s,%s" %(r,g,b))
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            for z in range(0,30): #draw the pixels
                w = y * 2
                if y > 15:
                    w = (15 - (y - 15)) * 2
                if z>w-3 and z<w+3:
                    ser.write("#%c%c%c%c" % (r,g,b,z))
                else:
                    ser.write("#\x00\x00\x00%c" % z)
            ser.write("!")
            if scaring==1:
                twitch_bot_utils.printer("Scare! Stopping user command")
                set_animating(0)
                return
            pygame.time.wait(10)       
        pygame.time.wait(500)
    set_animating(0)
    return  
    
def centerchase(r, g, b,num=6):
    wait_animating()
    set_animating(1)
    twitch_bot_utils.printer("%s,%s,%s" %(r,g,b))
    for x in range(0, num): #chase animation num times
        for y in range(0, 30): #chase across all 30 leds
            for z in range(0,30): #draw the pixels
                center = 15-abs(y-15)
                left = 15 + center
                right = 15 - center
                if (z>left-2 and z<left+2) or (z>right-2 and z<right+2):
                    ser.write("#%c%c%c%c" % (r,g,b,z))
                else:
                    ser.write("#\x00\x00\x00%c" % z)
            ser.write("!")
            if scaring==1:
                twitch_bot_utils.printer("Scare! Stopping user command")
                set_animating(0)
                return
            pygame.time.wait(10)       
        pygame.time.wait(500)
    set_animating(0)
    return
    
def alternate(r1,g1,b1,r2,g2,b2):
    wait_animating()
    set_animating(1)
    twitch_bot_utils.printer("%s,%s,%s,%s,%s,%s" %(r1,g1,b1,r2,g2,b2))
    for y in range( 0, 10 ):
        r1,r2 = r2,r1 #swap colors
        g1,g2 = g2,g1
        b1,b2 = b2,b1
        for x in range( 0, 30 ):
            if x<15: #draw the first color to 0-14
                ser.write("#%c%c%c%c" % (r1,g1,b1,x)) 
            else: #and the second to 15-30
                ser.write("#%c%c%c%c" % (r2,g2,b2,x))
        ser.write("!")
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping alternate")
            set_animating(0)
            return
        time.sleep(0.5)
    modedefault()
    return
    
def disco_alternate():
    wait_animating()
    set_animating(1)
    w=0
    x=128
    for y in range(0, 255): #loop through all 255 colors
        if (y%24)==0:
            w,x = x,w
        rgb = twitch_bot_utils.Wheel((y+x)%255)
        rgb2 = twitch_bot_utils.Wheel((y+w)%255)
        for z in range( 0, 30 ):
            if z<15: #draw the first color to 0-14
                ser.write("#%c%c%c%c" % (rgb[0],rgb[1],rgb[2],z)) 
            else: #and the second to 15-30
                ser.write("#%c%c%c%c" % (rgb2[0],rgb2[1],rgb2[2],z)) 
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping user command")
            set_animating(0)
            return
        ser.write("!")    
        pygame.time.wait(5)
    modedefault()
    return

#fire animation using 2 colors
#todo add gradients
def fire(r1,g1,b1,r2,g2,b2):
    wait_animating()
    set_animating(1)
    irc.msg("FIRE!!!")
    for y in range( 0, 30 ):
        for x in range( 0, 30 ):
            r = random.randrange(2)
            if r==1:
                ser.write("#%c%c%c%c" % (r1,g1,b1,x) )
            else:
                ser.write("#%c%c%c%c" % (r2,g2,b2,x) )
        ser.write("!")
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping fire")
            set_animating(0)
            return
        time.sleep(0.1)
    modedefault()
    return
    
#disco fire
#todo add gradients
def disco_fire():
    wait_animating()
    set_animating(1)
    irc.msg("FIRE!!!")
    for y in range( 0, 30 ):
        for x in range( 0, 30 ):
            c = twitch_bot_utils.Wheel(((random.randint(1, 32)+random_color)*7)%255)
            ser.write("#%c%c%c%c" % (c[0],c[1],c[2],x) )
        ser.write("!")
        if scaring==1:
            twitch_bot_utils.printer("Scare! Stopping disco fire")
            set_animating(0)
            return
        time.sleep(0.1)
    modedefault()
    return
    
def allleds(r,g,b,wait):
    wait_animating()
    set_animating(1)
    ser.write("#%c%c%c\xff!" % (r,g,b) )
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

twitch_profile("##Commands for everyone (even if you don't have control)")
twitch_profile("These commands, are available to everyone (even when not in control)  ")
twitch_profile("**!status** : lets you know who is currently in control, and how much time left they have  ")
twitch_profile("**!whosgotit** : lets you know who is currently in control  ")
twitch_profile("**!timeleft** : lets you know much much time is left before control is shifted  ")
twitch_profile("**!optout** : lets you opt out of getting picked for control")
twitch_profile("**!optin** : lets you opt back in to get control")
twitch_profile("**!opted username** : lets you check if a specific user is opted in or out")
twitch_profile("**!game** : lets you know what game we are currently playing")
twitch_profile("**!nextgame** : lets you know what game we are going to play next")
twitch_profile("**!nextscarygame** : Brings up the current poll for what scary game is next")
twitch_profile("")
        
twitch_profile("#Commands for everyone (even if you don't have control) Scary & Normal mode  ")
twitch_profile("")
twitch_profile("**disco**: plays a crazy color animation  ")
twitch_profile("**disco fire**: plays another crazy color animation  ")
twitch_profile("**disco strobe**: plays yet another crazy color animation  ")
twitch_profile("**fire(red|blue)** : plays a fire animation with two colors ")
twitch_profile("**strobe** : plays a strobe animation  ")
twitch_profile("**rgb(yellow)** : Lets users pick a specific color  ")
twitch_profile("**chase(green)** : Lets users play a \"chase\" animation with a specific color  (chase also lets you use 3 color commands separated by a pipe \"|\" to chase in a row)")
twitch_profile("**centerchase(blue)** : Same as chase, but starts in the center and goes out from both left and right")
twitch_profile("**alternate(green,purple)** : plays an alternating animation (lights half the leds with one color, and the other, with the second)  ")
twitch_profile("**disco alternate** : plays an alternating animation (lights half the leds with one color, and the other, with the second) with the disco palette  ")
twitch_profile("**randomcolor** : picks a random color to show on the led bar ")
twitch_profile("")
twitch_profile("All colors/commands accept 0-255,0-255,0-255 rgb, as well as html color codes (copy pasted from w3's html color codes)  ")
twitch_profile("")
twitch_profile("For example: alternate(red,blue), will do the same thing as alternate(255,0,0,0,0,255)  ")
twitch_profile("")
twitch_profile("If you have an idea for new rules/scares/animations/things I should let viewers control while playing games... Let me know, I'm trying to add at least one new feature every night to keep things interesting.")

#commands accessible by all users
def user_commands(user,data):
    global user_stack
    
    parts = data.split()
    command = parts[0][1:]
    
    twitch_bot_utils.printer("Checking %s for user commands..." % data)
    
    #start commands
    if data.find ( 'test' ) != -1:
        irc.msg("test to you too!")
        return True
    
    #Scary mode only commands
    if mode <= 1:
        hide = False
        if data.find("!hide") != -1:
            hide = True
        if data.find("!scarecommands") != -1 or data.find("!scarelist") != -1 or data.find("!scares") != -1:
            irc.msg("Scare commands: !randomscare, drop, brush, tapping, rattle, spine, flip, monitor, flicker, mute, dark, wasd, wiggle, and spasm. Use !scaresounds to list sound scares.",hide)
            return True
        if data.find("!trollcommands") != -1 or data.find("!trolllist") != -1 or data.find("!trolls") != -1:
            irc.msg("Troll commands: !randomtroll, flip, monitor, flicker, mute, dark, wasd, wiggle, vibe and spasm. Use !sounds to list sounds.",hide)
            return True
        if data.find("!sounds") != -1 or data.find("!soundscares") != -1 or data.find("!soundlist") != -1:
            temp = ""
            for sound, file in sounds.iteritems():
                temp = temp + sound + ", "
            temp = temp[:-2]
            irc.msg("Available sounds: %s" % temp,hide)
            return True
        if data.find("!patience") != -1:
            irc.msg("You can only do scares/trolls when it is your turn as long as you are optin'd spiffbot will pick you at random",hide)
            return True
        if data.find("!status") != -1 or data.find("!timeleft") != -1 or data.find("!whosgotit") != -1:
            if scaring == 1:
                if mode == 0:
                    irc.msg("%s is currently scaring..." % master,hide)
                if mode == 1:
                    irc.msg("%s is currently trolling..." % master,hide)
                return True
            if data.find("!status") != -1:
                timeleft = round(300 - (time.time() - counter))
                irc.msg("%s is currently in control, with %s seconds left!" % (master,timeleft),hide)
                return True
            #let viewers know how much time is left    
            if data.find("!timeleft") != -1:
                timeleft = 300 - (time.time() - counter)
                irc.msg("%s has %s seconds left!" % (master,round(timeleft)),hide)
                return True
            if data.find("!whosgotit") != -1:
                irc.msg("%s is currently in control!" % (master),hide)
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
        if command == "!opted":
            opt_status = "out"
            if len(parts)==1:
                parts.append(user)
            if db.getUserOpted(parts[1]):
                opt_status = "in"
            irc.msg("%s is opted %s!" % (parts[1],opt_status))
            return True
        if data.find("am i opted") != -1:
            if user in db.getOptedUsers():
                opted = "in"
            else:
                opted = "out"
            irc.msg("%s is opted %s" % (user,opted))
            return True

    #Get current streaming game
    if command == "!nextgame" or ( data.find ( 'what game' ) != -1 and data.find ( 'next' ) != -1 ):
        irc.msg("The next game is: %s! and vote/check the status of the next scary game here: %s" % (get_next_game(),next_scary_game) )
        return True
        
    #Get current streaming game
    if command == "!nextscarygame" or ( data.find ( 'what game' ) != -1 and data.find ( 'next' ) != -1 ):
        irc.msg("The next scary game is determined by you! Vote/Check the status here: %s!" % next_scary_game )
        return True
    if command == "!colors":
        irc.msg("Color commands: disco, disco strobe, disco alternate, disco chase, disco fire, fire(red|blue), strobe, chase(red|white|blue), centerhase(red|white|blue), alternate(red|blue), randomcolor")
        return True
    if command == "!intro":
        irc.msg("Check out this 1 minute video that explains my stream! https://www.youtube.com/watch?v=q0q8SML6d_I")
        return True
        
    if command == "!github":
        irc.msg("Add suggestions here! https://github.com/spiffomatic64/SpiffBot/issues")
        return True
        
    if command == "!twitter":
        irc.msg("Follow me on twitter for stream related updates! https://twitter.com/spiffomatic64")
        return True
    
    if command == "!game" or data.find ( 'what game' ) != -1:
        irc.msg("The current game is: %s" % get_game())
        return True
        
    if command == "!games":
        irc.msg("List of \"Best of the best\" https://docs.google.com/spreadsheets/d/1m1Jq_zOJg-BUWDY-Ir7KFGQsKCU3RcdU3eLW5_czKis/edit#gid=0")
        return True
        
    if command == "!halley":
        irc.msg("Wife Scare Part 1: https://www.youtube.com/watch?v=Q-xaW7IIa3I Part 2: https://www.youtube.com/watch?v=VROLA7HS8KI")
        return True
    
    if data.find("!spiff") != -1:
        elapsed = alert.notify()
        if elapsed > 0:
            irc.msg("Spiff was just notified %s seconds ago!" % elapsed )
        return True
    
    if command == "!getmode" or command == "!whichmode":
        if mode == 0:
            irc.msg("ITS SCARY TIME!!!")
            return True
        if mode == 1:
            irc.msg("LETS TROLL SPIFF!!!")
            return True
        if mode == 2:
            irc.msg("LIGHTS ARE PRETTY!!!")
            return True

    if scaring == 1 or animating == 1:
        twitch_bot_utils.printer("Busy, adding to stack: scaring: %s animating: %s" % (scaring,animating))
        user_stack.append([user,data])
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
                animation = threading.Thread(target=disco_strobe)
                animation.daemon = True
                animation.start() 
            elif data.find ( 'fire' ) != -1:
                animation = threading.Thread(target=disco_fire)
                animation.daemon = True
                animation.start() 
            elif data.find ( 'alternate' ) != -1:
                animation = threading.Thread(target=disco_alternate)
                animation.daemon = True
                animation.start() 
            elif data.find ( 'chase' ) != -1:
                animation = threading.Thread(target=disco_chase)
                animation.daemon = True
                animation.start() 
            else:
                animation = threading.Thread(target=disco)
                animation.daemon = True
                animation.start() 
            return True

        #flickr strobe
        if data.find ( 'strobe' ) != -1:
            strobe()
            return True
        
        if data.find ( 'randomcolor' ) != -1:
            rgb = twitch_bot_utils.convertcolor("random",random_color)
            allleds(rgb[0],rgb[1],rgb[2],10)
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
                        allleds(rgb[0],rgb[1],rgb[2],10)
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
                set_animating(1)
                twitch_bot_utils.printer("key: %s value: %s : %s,%s,%s" % (key,value,int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)))
                irc.msg("%s!!!" % key.upper())
                ser.write("#%c%c%c\xff!" % (int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)) )
                user_wait(5)
                modedefault()
                return True
                
def last_seen(user,data):
    db.updateLastSeen(user)
    
#constants
auth = twitch_auth.auth()
auth.add_admin("spiffbot")
master = auth.get_streamer()
alert = twitch_bot_utils.notification("./sounds/OOT_MainMenu_Select.ogg",60)
user_stack = []
pass_counter = 3
last_pass = None
random_color=1
scaring = 0
switching = 0
writing = 0
set_animating(0)
next = None
stayAlive = 1

mode = twitch_bot_utils.scaryDay()

#serial stuff
#todo: add code to find arduino dynamically
ser = twitch_bot_serial.twitch_serial("Com4",115200)

#db stuff
db = twitch_db.twitchdb(auth.get_db_user(),auth.get_db_pass(),"127.0.0.1","twitch")

#import external scares
vol_scare = twitch_volume.volume_change()

#setup audio
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
twitch_bot_utils.printer("Initiated Pygame Mixer:")
twitch_bot_utils.printer(pygame.mixer.get_init())
twitch_bot_utils.printer(pygame.mixer.get_num_channels())

irc = twitch_bot_utils.irc_connection("irc.twitch.tv","6667",auth.get_bot(),auth.get_oauth(),
    auth.get_streamer(),[autoOptIn,last_seen,admin_commands,master_commands,user_commands])    

#Switch Timer Thread start
t2 = threading.Thread(target=mastertimer)
t2.daemon = True
t2.start()
midi = twitch_bot_midi.midi_lights("MIDISPORT 1x1 In",ser)
midi.startMidi()


twitch_bot_utils.printer("Blacking out all pixels!")
ser.write("#\x00\x00\x00\xff!")
time.sleep(2)
modedefault()
time.sleep(1)
wait_animating()
twitch_bot_utils.printer("READY!")
irc.msg("READY!")


user_stack_thread = threading.Thread(target=user_stack_consumer)
user_stack_thread.daemon = True
user_stack_thread.start()

#Main loop
while stayAlive:
    time.sleep(1)
