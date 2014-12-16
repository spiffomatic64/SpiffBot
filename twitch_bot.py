import socket
import time
import random

bot_username = "botname"                                        #Put the twitch username of your bot here (A bot needs a twitch account to function in chat)
channel = "channel"                                             #Put the channelname of the stream you want the bot to join (most likely will be your twitch username)
oauth = "xxxxxxxxxxxxxxxxxxxxxx"                                #Put the oauth token of the bot's twitch account here (Login to twitch as your bot, then go here http://www.twitchapps.com/tmi/ 
                                                                #click "connect to twitch" then copy the text that is after oauth: 
    
network = 'irc.twitch.tv'                                       #the twitch server, leave this alone
port = 6667                                                     #the port the irc server is running, leave this alone
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )      #This sets up the connection
irc.connect ( ( network, port ) )                               #This starts the connection
print ("connected")                                             #Lets you know in the console that you connected
irc.send ( 'PASS oauth:%s\r\n' % oauth)                         #This sends your password (that we defined above)
irc.send ( 'NICK %s\r\n' % bot_username )                       #This sends your nick name (must be the same as username which we defined above)
irc.send ( 'USER %s %s %s :Python IRC\r\n' % (bot_username,bot_username,bot_username))      #This sets your username name (that we defined above)
time.sleep(1)                                                   #waits 1 second to get some data back from the server
print ("listening...")                                          #lets you know its listening for data
print (irc.recv ( 4096 ))                                       #gets data from the irc server
print ("Got stuff")                                             #lets you know it got stuff
irc.send ( 'JOIN #%s\r\n' % channel)                            #joins the channel we defined above
while True:                                                     #main loop, this will run until you close the program
    orig = irc.recv ( 4096 )                                    #gets data from the irc server
    parts = orig.split()                                        #Split the irc data into chunks in between "spaces"
    
    if orig.find ( 'PING' ) != -1:                              #Needed to keep connected to IRC, without this, twitch will disconnect
        irc.send ( 'PONG ' + orig.split() [ 1 ] + '\r\n' )
    if len(parts)>3:                                            #all user input data has at least 3 parts user, PRIVMSG, #channel
        user = parts.pop(0)                                     #get rid of the first part, we dont need it
        user = user[1:user.find("!")]                           #get the username from the next "part"
        parts.pop(0)                                            #throw away the next two parts, we dont need them
        parts.pop(0)
        
        responses = ['a', 'b', 'c', 'd', 'e']
        
        if parts[0][1:2]=="!":                                  #check that the first word someone says starts with a !
            command = parts[0][1:]                              #grab the first word the user says and put it into the "command" variable
            print ("user: %s command: %s" % (user,command))     #print out what user and their "command" for debugging purposes
            if command=="!test":                                #check if they said !test
                irc.send ( 'PRIVMSG #%s :test to you too!\r\n' % channel )  #Make the bot reply back with "test to you too!"
            if len(parts)>1:
                if command=="!kill":                            #check if they said !kill
                    irc.send ( 'PRIVMSG #%s :%s %s\r\n' % (channel,parts[1],random.choice(responses)))  #send a message saying <username> then a random string from the responses list above
                                                                #Put all parts back together into data variable, and lowercase it
                                                                #data will contain anything a user says in chat
        data = ""
        for part in parts:                                      #grab the entire message and put it into data
            data = data + part + " "
        data = data.lower()                                     #(set data to lowercase for easier parsing)

        print ("user: %s message: %s" % (user,data))            #print out the username and whatever they said for debug purposes
    print (orig)