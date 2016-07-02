#! python2

import threading
import subprocess
import logging
import Queue

class intro_thread:
    def __init__(self):
        self.queue = Queue.Queue()
        self.alive = False

    def thread_loop(self):
        while self.alive:
            try:
                intro_url = self.queue.get(True,1)
                logging.log(logging.INFO, "Playing intro: %s",intro_url)
                p = subprocess.Popen(["py", "twitch_vlc_player.py", intro_url])
                p.wait()
            except Queue.Empty:
                pass


    def run(self):
        self.alive = True
        self.running = threading.Thread(target=self.thread_loop)
        self.running.daemon = True
        self.running.start()
        logging.log(logging.INFO,"Started Intro Video Queue Thread")

    def stop(self):
        self.alive = False

    def addIntro(self,intro):
        self.queue.put(intro)