#! python2

import logging
import requests
import json

class twitch_json:
    def __init__(self, streamer):
        self.streamer = streamer
        try:
            url = "https://api.twitch.tv/kraken/streams/%s" % self.streamer
            data = requests.get(url)
            binary = data.content
            output = json.loads(binary)
            self.streamId = output['stream']['_id']
            logging.log(logging.INFO, "Got StreamID: %s" % self.streamId)
        except:
            logging.log(logging.ERROR,("Failed to setup json!"))
            #add while to wait for streamid

    def getStreamId(self):
        if self.streamId:
            return self.streamId
        else:
            return False