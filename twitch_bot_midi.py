#! python2

import pygame.midi
import threading
import twitch_bot_utils
import time
import logging


class midi_lights:
    def getMidi(self, midi_device):
        c = 0
        for x in range(0, pygame.midi.get_count()):
            logging.log(logging.DEBUG, pygame.midi.get_device_info(x)[1])
            if pygame.midi.get_device_info(x)[1] == midi_device:
                logging.log(logging.INFO, "Found midi: %s" % c)
                return c
            c += 1

    def __init__(self, devicename, serial_device):
        # Midi initialization
        pygame.midi.init()
        midi_device = self.getMidi("MIDISPORT 1x1 In")
        logging.log(logging.INFO, "Got midi: %s" % midi_device)
        self.ser = serial_device
        self.midi = pygame.midi.Input(midi_device)
        # setup thread object
        self.t = threading.Thread(target=self.midiDrumsThread)
        self.t.daemon = True

    def startMidi(self):
        self.midiActive = True
        # Midi Thread start
        if self.t.isAlive():
            return False
        else:
            self.t = None
            self.t = threading.Thread(target=self.midiDrumsThread)
            self.t.daemon = True
            self.t.start()

    def stopMidi(self):
        self.midiActive = False
        stop = time.time() + 3
        while time.time() < stop and self.t.isAlive():
            time.sleep(0.1)
        if self.t.isAlive():
            return False
        else:
            return True

    def toggleMidi(self):
        if self.midiActive:
            if self.stopMidi():
                return "Stopped Midi!"
            else:
                return "Failed to stop Midi!"
        else:
            if self.startMidi():
                return "Started Midi!"
            else:
                return "Midi is already running!"

    # Midi thread, gets midi data, translates to html rgb values
    # and lights leds based on that color for 50ms, then turns all leds off
    def midiDrumsThread(self):
        logging.log(logging.INFO, "Started Midi Thread!")
        while self.midi.poll():
            self.midi.read(1000)
        drums = {38: "ffffff",  # snare
                 40: "ffffff",  # snare rim
                 26: "ffff00",  # highhat edge
                 46: "ffff00",  # highhat crown
                 55: "00ff00",  # crash edge
                 49: "00ff00",  # crash crown
                 48: "0000ff",  # left tom
                 45: "ff00ff",  # right tom
                 59: "00ffff",  # ride edge
                 51: "00ffff",  # ride crown
                 41: "ff8000",  # floor tom
                 36: "ff0000"}  # bass

        # run the event loop
        # Todo: ability to start/stop, or enable/disable the thread
        value = 0
        while self.midiActive:
            if self.midi.poll():
                # read 1000 bytes from midi device
                events = self.midi.read(1000)
                for e in events:
                    if e[0][2] != 64:  # ignore note off packets
                        # logging.log(logging.INFO,"%s:%s" % (e[0][1],e[0][2])) #debug, comment this out while playing
                        intensity = abs(e[0][2]) * 2
                        if intensity > 255:
                            intensity = 255

                        if e[0][1] in drums:
                            # logging.log(logging.INFO,drums[e[0][1]]) #debug, comment this out while playing
                            value = drums[e[0][1]]
                        rgb = twitch_bot_utils.hex2chr(value)
                        # before = get_pixels()

                        self.ser.write("#%c%c%c\xff!" % (rgb[0], rgb[1], rgb[2]))
                        pygame.time.wait(50)
                        # too slow, just write to black
                        '''for x in range(0,30):
                            writing_serial("#%c%c%c%c" % (before["%s"%x][0],before["%s"%x][1],before["%s"%x][2],x))
                        writing_serial("!")'''
                        self.ser.write("#\x00\x00\x00\xff!")

            # wait 10ms - this is arbitrary, but wait(0) still resulted
            # in 100% cpu utilization
            pygame.time.wait(10)
        logging.log(logging.INFO, "Stopped Midi Thread!")
