#! python2

import logging
import requests
import json

class twitch_json:
    def __init__(self, streamer):
        self.streamer = streamer
        try:
            logging.log(logging.INFO, "Checking streamId...")
            url = "https://api.twitch.tv/kraken/streams/%s" % self.streamer
            data = requests.get(url)
            binary = data.content
            output = json.loads(binary)
            self.streamId = output['stream']['_id']
        except:
            return False

    def getStreamId(self):
        return self.streamId