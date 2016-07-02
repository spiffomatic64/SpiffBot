#! python2

import logging
import urllib
import subprocess
import time
import os

class image_handler:
    def __init__(self):
        self.p = None
        self.image_url = ""

    def display_image(self,image_url):
        try:
            urllib.urlretrieve (image_url, "brb.jpg")
            self.p = subprocess.Popen(["C:\\Program Files (x86)\\FullScreen Photo Viewer\\FullScreen Photo Viewer.exe", ".\\brb.jpg", "\/s"])
            return True
        except:
            logging.log(logging.INFO,"Failed to download and diplsy image: %s" % image_url)
            return False
    def close_image(self):
        try:
            self.p.terminate();
            os.remove("brb.jpg")
            return True
        except:
            logging.log(logging.INFO, "Failed to close image")
            return False