import socket
import time
import subprocess


bot_username = "spiffbot"
channel = "spiffomatic64"
oauth = "drqvq0h2jruebvxz1ufzgciyw8a488"

network = 'irc.twitch.tv'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print "connected"
irc.send ( 'PASS oauth:%s\r\n' % oauth)
irc.send ( 'NICK %s\r\n' % bot_username )
irc.send ( 'USER %s %s %s :Python IRC\r\n' % (bot_username,bot_username,bot_username))
time.sleep(1)
print "listening..."
print irc.recv ( 4096 )
print "Got stuff"
irc.send ( 'JOIN #%s\r\n' % channel)
while True:
    orig = irc.recv ( 4096 )
    parts = orig.split() #Split irc data by white space
    
    if orig.find ( 'PING' ) != -1: #Needed to keep connected to IRC, without this, twitch will disconnect
        irc.send ( 'PONG ' + orig.split() [ 1 ] + '\r\n' )
    if len(parts)>3: #all user input data has at least 3 parts user, PRIVMSG, #channel
        user = parts.pop(0) 
        user = user[1:user.find("!")] #get the username from the first "part"
        parts.pop(0) #throw away the next two parts
        parts.pop(0)
        #Put all parts back together into data variable, and lowercase it
        data = ""
        if parts[0][1:2]=="!": #check that the first word someone says starts with a !
            command = parts[0][1:] #grab set the word (including the !)
            print "user: %s command: %s" % (user,command) #debug
            if command=="!test": #check if they said !test
                irc.send ( 'PRIVMSG #%s :test to you too!\r\n' % channel )  
            else:
                p = subprocess.Popen(["py", "C:\\Users\\spiffomatic64\\Documents\\GitHub\\SpiffBot\\vlc_test.py" , command[1:]])
                print "py vlctest.py %s" % command[1:]
                p.wait()
        for part in parts: #grab the entire message and put it into data
            data = data + part + " "
        data = data.lower() #(set data to lowercase for easier parsing)

        print "user: %s message: %s" % (user,data) #debug
    print orig