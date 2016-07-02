#! python2

# add user join hook
# add start-time parameter
# add duration parameter to intro
# add lock mechanism for video playing
# add queue for videos to be played
# add irc message for failed youtube video

import time
import logging

import twitch_auth
import twitch_bot_db
import twitch_bot_utils
import twitch_user_parsers
import twitch_bot_lights
import twitch_bot_serial

# constants
auth = twitch_auth.auth()
auth.add_admin(twitch_auth.get_bot())

stayAlive = 1

# db stuff
db = twitch_bot_db.twitchdb(twitch_auth.get_db_user(), twitch_auth.get_db_pass(), "spiffomatic64.com", "spiffo_twitch")

irc = twitch_bot_utils.irc_connection("irc.twitch.tv", "6667", twitch_auth.get_bot(),
                                      twitch_auth.get_oauth(), twitch_auth.get_streamer())

user_parsers = twitch_user_parsers.userParsers(db,irc)
#ser = twitch_bot_serial.twitch_serial(115200)
#lights = twitch_bot_lights.lights(ser,irc,1)

#TODO: Add parsers via config file
#TODO: Look into enabling/disabling parsers in real time(monitor config file)
irc.add_msgParser(user_parsers.testParse)
irc.add_msgParser(user_parsers.last_seen)
irc.add_msgParser(user_parsers.introHandler)
irc.add_msgParser(user_parsers.streamIdHandler)
irc.add_msgParser(user_parsers.brbHandler)
#irc.add_msgParser(lights.parser)

time.sleep(1)
logging.log(logging.INFO, "READY!")
irc.msg("READY!")
# irc.send("CAP REQ :twitch.tv/membership  \r\n")

# Main loop
while stayAlive:
    time.sleep(1)
