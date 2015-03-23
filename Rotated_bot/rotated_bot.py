import re
import time
import threading
import random
import json
import requests
import string
import os

from hue_auth import ACCESSTOKEN,BRIDGEID
from rgb_cie import Converter


import twitch_auth
import twitch_bot_colors
import twitch_bot_utils

API_ADDRESS_CONTROL = 'https://www.meethue.com/api/sendmessage'
API_STATUS_ADDRESS = 'https://www.meethue.com/api/getbridge'
ContentType='application/x-www-form-urlencoded'
headers = {'content-type':ContentType}


def constructCustomMsg(apiEndPoint, command, method):
  custom_control_message_structure = 'clipmessage={ bridgeId: "'+BRIDGEID+'", clipCommand: { url: "/api/0/'+apiEndPoint+'", method: "'+method+'", body: '+command+' } }'
  return custom_control_message_structure
  
def hueCommand(url, command, method):
  payload = {'token':ACCESSTOKEN};
  msg = 'clipmessage={ bridgeId: "'+BRIDGEID+'", clipCommand: { url: "/api/0/'+url+'", method: "'+method+'", body: '+command+' } }'
  r = requests.post(API_ADDRESS_CONTROL, params=payload,headers=headers,data=msg);
  twitch_bot_utils.printer("Command: %s Result: %s" % (command,r))
  return r.text

def set_animating(status):
    global animating
    
    twitch_bot_utils.printer("Setting animating to: %s" % status)
    animating = status
        
def wait_animating():
    while animating==1:
        time.sleep(0.1)

def user_wait(duration):
    stop = time.time()+duration
    while time.time() < stop:
        time.sleep(0.5)
    return

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

#commands that will only work for streamer (and moderators in the future)
def admin_commands(user,data):
    global stayAlive
    
    #if user.lower() == auth.get_streamer():
    if auth.is_admin(user):
        #split irc messages into parts by white space 
        parts = data.lower().split()
        twitch_bot_utils.printer("User is admin, checking for commands")
        command = parts[0][1:] #get the first "word" and remove the first character which is ":"
        
        if command == "!restart" or command == "!reload":
            stayAlive = 0
        if command == "!raffle":
            raffle()
            return True

def user_stack_consumer():
    global user_stack

    while True:
        if len(user_stack)>0 and animating==0:
            twitch_bot_utils.printer("user stack consumer DEBUG!!!!!!!!!!!: %s %s" % (len(user_stack),animating))
            user,data = user_stack.pop(0)
            twitch_bot_utils.printer("Checking a buffered string: %s" % data)
            user_commands(user,data)
        time.sleep(1)

def modedefault():
    wait_animating()
    color =  converter.rgbToCIE1931(255,255,255)
    sendToAll("{ \"on\": true, \"bri\": 254, \"xy\":%s,  \"effect\": \"none\"}" % color)

def sendToAll(command):
    response = hueCommand("lights/1/state", command, "PUT")
    response = hueCommand("lights/2/state", command , "PUT")
    response = hueCommand("lights/3/state", command , "PUT")

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
    
    if command == "!game" or data.find ( 'what game' ) != -1:
        irc.msg("The current game is: %s" % get_game())
        return True
        
    if command == "!colors":
        irc.msg("The available colors are listed here: http://www.w3schools.com/html/html_colornames.asp" )
        return True

    if animating == 1:
        twitch_bot_utils.printer("Busy, adding to stack: animating: %s" % (animating))
        user_stack.append([user,data])
        del user_stack[10:]
        temp = []
        for stack in user_stack:
            temp.append(stack[1])
        twitch_bot_utils.printer(string.join(temp," - "))
        return 
    else:
        twitch_bot_utils.printer("No animation currently, checking for animations")
        if data.find ( 'randomcolor' ) != -1:
                rgb = twitch_bot_utils.convertcolor("random",1)
                set_animating(1)
                irc.msg("RANDOMCOLOR!!!!!!!")
                color =  converter.rgbToCIE1931(rgb[0], rgb[1], rgb[2])
                twitch_bot_utils.printer("Colors: %d %d %d" % (rgb[0], rgb[1], rgb[2]))
                twitch_bot_utils.printer(color)
                
                sendToAll("{ \"bri\": 254, \"xy\":%s }" % color)
                user_wait(light_length)
                set_animating(0)
                modedefault()
                return True
        if data.find ( "fire" ) != -1:
            set_animating(1)
            irc.msg("FIRE!!!")
            color =  converter.rgbToCIE1931(255,255,0)
            hueCommand("lights/1/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
            color =  converter.rgbToCIE1931(255,0,0)
            hueCommand("lights/2/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
            color =  converter.rgbToCIE1931(255,255,0)
            hueCommand("lights/3/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
            sendToAll("{ \"alert\": \"lselect\" }")
            user_wait(light_length)
            set_animating(0)
            modedefault()
            return True    
        if data.find ( "disco" ) != -1:
                if data.find ( "strobe" ) != -1:
                    set_animating(1)
                    irc.msg("DISCO SEIZURE PARTY!!!")
                    color =  converter.rgbToCIE1931(255,0,0)
                    hueCommand("lights/1/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
                    color =  converter.rgbToCIE1931(0,255,0)
                    hueCommand("lights/2/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
                    color =  converter.rgbToCIE1931(0,0,255)
                    hueCommand("lights/3/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
                    sendToAll("{ \"alert\": \"lselect\" }")
                    user_wait(light_length)
                    set_animating(0)
                    modedefault()
                    return True    
                set_animating(1)
                irc.msg("DISCO PARTY!!!")
                sendToAll("{ \"effect\": \"colorloop\" }")
                user_wait(light_length)
                set_animating(0)
                modedefault()
                return True
        if data.find ( "strobe" ) != -1:
            set_animating(1)
            irc.msg("SEIZURE PARTY!!!")
            sendToAll("{ \"alert\": \"lselect\" }")
            user_wait(light_length)
            set_animating(0)
            modedefault()
            return True
        if data.find( "spoopy" ) != -1:
            set_animating(1)
            irc.msg("2SPOOPY4EVERYONE!!!")
            sendToAll("{ \"on\": false }")
            user_wait(light_length)
            set_animating(0)
            modedefault()
            return True
        if data.find ( "police" ) != -1:
            set_animating(1)
            irc.msg("CHEESE IT!!!")
            color =  converter.rgbToCIE1931(0,0,255)
            hueCommand("lights/1/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
            color =  converter.rgbToCIE1931(255,0,0)
            hueCommand("lights/2/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
            color =  converter.rgbToCIE1931(0,0,255)
            hueCommand("lights/3/state","{ \"bri\": 254, \"xy\":%s }" % color ,"PUT")
            sendToAll("{ \"alert\": \"lselect\" }")
            user_wait(light_length)
            set_animating(0)
            modedefault()
            return True 
        #for key, value in twitch_bot_colors.colors.iteritems():          
        for k in sorted(twitch_bot_colors.colors, key=len, reverse=True):
            if data.find ( k.lower() ) != -1:
                value = twitch_bot_colors.colors[k]
                set_animating(1)
                twitch_bot_utils.printer("key: %s value: %s : %s,%s,%s" % (k,value,int("0x"+value[0:2],0),int("0x"+value[2:4],0),int("0x"+value[4:6],0)))
                irc.msg("%s!!!" % k.upper())
                color =  converter.rgbToCIE1931(int("0x"+value[0:2],0), int("0x"+value[2:4],0), int("0x"+value[4:6],0))
                twitch_bot_utils.printer("Colors: %d %d %d" % (int("0x"+value[0:2],0), int("0x"+value[2:4],0), int("0x"+value[4:6],0)))
                twitch_bot_utils.printer(color)
                sendToAll("{ \"bri\": 254, \"xy\":%s }" % color)
                user_wait(light_length)
                set_animating(0)
                modedefault()
                return True
    
#constants
auth = twitch_auth.auth()
auth.add_admin("spiffbot")
master = auth.get_streamer()
user_stack = []
set_animating(0)
stayAlive = 1
converter = Converter()
light_length = 15

irc = twitch_bot_utils.irc_connection("irc.twitch.tv","6667",auth.get_bot(),auth.get_oauth(),
    auth.get_streamer(),[admin_commands,user_commands])    

twitch_bot_utils.printer("READY!")
irc.msg("READY!")


user_stack_thread = threading.Thread(target=user_stack_consumer)
user_stack_thread.daemon = True
user_stack_thread.start()

#Main loop
while stayAlive:
    time.sleep(1)
