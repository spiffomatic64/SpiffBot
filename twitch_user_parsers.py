import logging

import twitch_auth
import twitch_bot_json
import twitch_bot_intro
import twitch_bot_image


class userParsers:
    def __init__(self,db,irc):
        self.db = db
        self.irc = irc
        self.json = twitch_bot_json.twitch_json(twitch_auth.get_streamer())
        self.intro = twitch_bot_intro.intro_thread()
        self.intro.run()
        self.image_viewer = twitch_bot_image.image_handler()

    def last_seen(self, user, data):
        self.db.updateLastSeen(user)

    def testParse(self, user,data):
        logging.log(logging.INFO, "\nuser: %s\ndata: %s" % (user,data))
        if data.find('test') != -1:
            self.irc.msg("Test to you too!")

    #TODO: handle invalid videos check before inserting
    #TODO: handle only mods
    def introHandler(self, user,data):
        parts = data.split()
        if parts[0].lower() == "!intro":
            #TODO Sanitize parts[1]
            self.db.updateIntro(user,parts[1])
            self.irc.msg("Added https://www.youtube.com/watch?v=%s as the intro for %s's mom" % (parts[1],user))


    def streamIdHandler(self, user,data):
        streamid = self.db.getStreamId(user)
        if not streamid or streamid != self.json.getStreamId():
            logging.log(logging.INFO, "New StreamID: %s" % self.json.getStreamId())
            self.db.updateStreamId(user, self.json.getStreamId())
            intro_url = self.db.getIntro(user)
            logging.log(logging.INFO, "Adding intro to queue: %s" % intro_url)
            self.intro.addIntro(intro_url)

    def brbHandler(self, user,data):
        parts = data.split()
        if parts[0].lower() == "!brb":
            # TODO Sanitize parts[1]
            if len(parts)>1:
                self.irc.msg("user: %s is displaying brb image: %s" % (user, parts[1]))
                self.image_viewer.display_image(parts[1])
        if parts[0].lower() == "!back":
            self.image_viewer.close_image()