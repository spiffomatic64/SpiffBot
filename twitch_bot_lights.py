#! python2

import logging
import twitch_bot_utils
import pygame
import threading
import time
import random
import re
import twitch_bot_colors


class lights:
    def __init__(self, ser, irc, event):
        self.ser = ser
        self.irc = irc
        self.random_color = 1
        self.animating = 0
        self.event = event
        self.mode = 1

    def parser(self,user,data):

        if data.find('disco') != -1:
            if data.find('strobe') != -1:
                animation = threading.Thread(target=self.disco_strobe)
                animation.daemon = True
                animation.start()
            elif data.find('fire') != -1:
                animation = threading.Thread(target=self.disco_fire)
                animation.daemon = True
                animation.start()
            elif data.find('alternate') != -1:
                animation = threading.Thread(target=self.disco_alternate)
                animation.daemon = True
                animation.start()
            elif data.find('chase') != -1:
                animation = threading.Thread(target=self.disco_chase)
                animation.daemon = True
                animation.start()
            else:
                animation = threading.Thread(target=self.disco)
                animation.daemon = True
                animation.start()
            return True

        # flickr strobe
        if data.find('strobe') != -1:
            self.strobe()
            return True

        if data.find('randomcolor') != -1:
            rgb = twitch_bot_utils.convertcolor("random", self.random_color)
            self.allleds(rgb[0], rgb[1], rgb[2], 10)
            return True

        m = re.search('(\w+)\((.+(?:\|[a-zA-Z0-9#]+)*)\)', data, re.IGNORECASE)
        if m:
            logging.log(logging.DEBUG, "regex passed")
            parts = m.group(2).split("|")
            if m.group(1).lower() == "chase":
                if len(parts) > 0:
                    while len(parts) > 6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part, self.random_color)
                        if rgb:
                            num = round(6 / len(parts))
                            self.chase(rgb[0], rgb[1], rgb[2], int(num))
                            time.sleep(1)
                        else:
                            logging.log(logging.ERROR, "Invalid color: %s" % part)
                    self.modedefault()
                    return True
                else:
                    logging.log(logging.ERROR, "Not enough colors to chase!")
            if m.group(1).lower() == "centerchase":
                if len(parts) > 0:
                    while len(parts) > 6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part, self.random_color)
                        if rgb:
                            num = round(6 / len(parts))
                            self.centerchase(rgb[0], rgb[1], rgb[2], int(num))
                            time.sleep(1)
                        else:
                            logging.log(logging.ERROR, "Invalid color: %s" % part)
                    self.modedefault()
                    return True
                else:
                    logging.log(logging.ERROR, "Not enough colors to centerchase!")
            if m.group(1).lower() == "bounce":
                if len(parts) > 0:
                    while len(parts) > 6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part, self.random_color)
                        if rgb:
                            num = round(6 / len(parts))
                            self.bounce(rgb[0], rgb[1], rgb[2], int(num))
                            time.sleep(1)
                        else:
                            logging.log(logging.ERROR, "Invalid color: %s" % part)
                            self.modedefault()
                    return True
                else:
                    logging.log(logging.ERROR, "Not enough colors to bounce!")
            if m.group(1).lower() == "cycle":
                if len(parts) > 0:
                    while len(parts) > 6:
                        parts.pop(6)
                    for part in parts:
                        rgb = twitch_bot_utils.convertcolor(part, self.random_color)
                        if rgb:
                            num = round(6 / len(parts))
                            self.allleds(rgb[0], rgb[1], rgb[2], num)
                        else:
                            logging.log(logging.ERROR, "Invalid color: %s" % part)
                    return True
                else:
                    logging.log(logging.ERROR, "Not enough colors to cycle!")
            if len(parts) == 1:
                rgb = twitch_bot_utils.convertcolor(parts[0], self.random_color)
                if rgb:
                    if m.group(1).lower() == "rgb":
                        self.allleds(rgb[0], rgb[1], rgb[2], 10)
                        time.sleep(1)
            if len(parts) == 2:
                rgb = twitch_bot_utils.convertcolor(parts[0], self.random_color)
                rgb2 = twitch_bot_utils.convertcolor(parts[1], self.random_color)
                if rgb:
                    if rgb2:
                        if m.group(1).lower() == "fire":
                            self.fire(rgb[0], rgb[1], rgb[2], rgb2[0], rgb2[1], rgb2[2])
                            time.sleep(1)
                            return True
                        if m.group(1).lower() == "alternate":
                            self.alternate(rgb[0], rgb[1], rgb[2], rgb2[0], rgb2[1], rgb2[2])
                            time.sleep(1)
                            return True
                    else:
                        logging.log(logging.ERROR, "Invalid color: %s" % parts[1])
                else:
                    logging.log(logging.ERROR, "Invalid color: %s" % parts[0])
                    return True
        # html color keys (single color, no animation)
        # todo replace with color converter
        for key, value in sorted(twitch_bot_colors.colors.iteritems()):
            if data.find(key.lower()) != -1:
                self.set_animating(1)
                logging.log(logging.INFO, "key: %s value: %s : %s,%s,%s" % (
                    key, value, int("0x" + value[0:2], 0), int("0x" + value[2:4], 0), int("0x" + value[4:6], 0)))
                self.irc.msg("%s!!!" % key.upper())
                self.ser.write(
                    "#%c%c%c\xff!" % (int("0x" + value[0:2], 0), int("0x" + value[2:4], 0), int("0x" + value[4:6], 0)))
                self.user_wait(5)
                self.modedefault()
                return True

    def profile(self):
        twitch_bot_utils.twitch_profile("#Commands for everyone (even if you don't have control) Scary & Normal mode  ")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("**disco**: plays a crazy color animation  ")
        twitch_bot_utils.twitch_profile("**disco fire**: plays another crazy color animation  ")
        twitch_bot_utils.twitch_profile("**disco strobe**: plays yet another crazy color animation  ")
        twitch_bot_utils.twitch_profile("**fire(red|blue)** : plays a fire animation with two colors ")
        twitch_bot_utils.twitch_profile("**strobe** : plays a strobe animation  ")
        twitch_bot_utils.twitch_profile("**rgb(yellow)** : Lets users pick a specific color  ")
        twitch_bot_utils.twitch_profile(
            "**chase(green)** : Lets users play a \"chase\" animation with a specific color  (chase also lets you use 3 color commands separated by a pipe \"|\" to chase in a row)")
        twitch_bot_utils.twitch_profile("**centerchase(blue)** : Same as chase, but starts in the center and goes out from both left and right")
        twitch_bot_utils.twitch_profile(
            "**alternate(green,purple)** : plays an alternating animation (lights half the leds with one color, and the other, with the second)  ")
        twitch_bot_utils.twitch_profile(
            "**disco alternate** : plays an alternating animation (lights half the leds with one color, and the other, with the second) with the disco palette  ")
        twitch_bot_utils.twitch_profile("**randomcolor** : picks a random color to show on the led bar ")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "All colors/commands accept 0-255,0-255,0-255 rgb, as well as html color codes (copy pasted from w3's html color codes)  ")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("For example: alternate(red,blue), will do the same thing as alternate(255,0,0,0,0,255)  ")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "If you have an idea for new rules/scares/animations/things I should let viewers control while playing games... Let me know, I'm trying to add at least one new feature every night to keep things interesting.")

    def user_wait(self, duration):
        stop = time.time() + duration
        while time.time() < stop and self.event == 0:
            time.sleep(0.5)
        return

    def wait_animating(self):
        while self.animating == 1:
            pygame.time.wait(10)

    def set_animating(self, status):
        logging.log(logging.INFO, "Setting animating to: %s" % status)
        self.animating = status


    # fade from current color to new color using a number of "frames"
    def fade(self, red, green, blue, steps, wait=2):
        logging.log(logging.INFO, "Starting Fade")
        diff = {}
        pixels = self.ser.get_pixels()
        logging.log(logging.INFO, "Fading")
        for x in range(0, len(pixels)):
            temp = [red - pixels["%s" % x][0], green - pixels["%s" % x][1], blue - pixels["%s" % x][2]]
            diff.update({x: temp})
        for x in range(0, steps + 1):
            for y in range(0, len(pixels)):
                r = int(round(pixels["%s" % y][0] + ((diff[y][0] / steps) * x)))
                if r < 0:
                    r = 0
                g = int(round(pixels["%s" % y][1] + ((diff[y][1] / steps) * x)))
                if g < 0:
                    g = 0
                b = int(round(pixels["%s" % y][2] + ((diff[y][2] / steps) * x)))
                if b < 0:
                    b = 0
                self.ser.write("#%c%c%c%c" % (r, g, b, y))
            self.ser.write("!")
            # make into function
            if self.event == 1:
                logging.log(logging.INFO, "Event! Stopping user command")
                self.ser.write("#%c%c%c\xff!" % (red, green, blue))
                self.set_animating(0)
                return
            pygame.time.wait(wait)
        self.ser.write("#%c%c%c\xff!" % (red, green, blue))
        self.set_animating(0)

    def set_mode(self, mode):
        self.mode = mode

    # set the leds to black if in scary mode, fade up from black to white if normal mode
    def modedefault(self):
        self.set_animating(1)
        if self.mode == 0:
            fade_thread = threading.Thread(target=self.fade, args=(0, 0, 0, 100))
            fade_thread.daemon = True
            fade_thread.start()
        if self.mode >= 1:
            fade_thread = threading.Thread(target=self.fade, args=(255, 255, 255, 100))
            fade_thread.daemon = True
            fade_thread.start()
        return

    def disco(self):
        self.wait_animating()
        self.set_animating(1)
        self.irc.msg("DISCO PARTY!!!!!!!!")
        for x in range(0, 5):  # loop 5 mins
            for y in range(0, 255):  # loop through all 255 colors
                rgb = twitch_bot_utils.Wheel(y)
                self.ser.write("#%c%c%c\xff!" % (rgb[0], rgb[1], rgb[2]))
                if self.event == 1:
                    logging.log(logging.INFO, "Scare! Stopping user command")
                    self.modedefault()
                    return
                pygame.time.wait(5)
        self.modedefault()
        return

    def strobe(self):
        self.wait_animating()
        self.set_animating(1)
        self.irc.msg("SEIZURE PARTY!!!!!!!!")
        for x in range(0, 50):  # flicker 200 times, for 30 ms on, then 30ms off
            self.ser.write("#\xff\xff\xff\xff!")
            pygame.time.wait(40)
            self.ser.write("#\x00\x00\x00\xff!")
            pygame.time.wait(40)
            if self.event == 1:
                logging.log(logging.INFO, "Event! Stopping user command")
                self.set_animating(0)
                return
        self.modedefault()
        return

    def disco_strobe(self):
        self.wait_animating()
        self.set_animating(1)
        self.irc.msg("DISCO SEIZURES!!!!!!!!")
        for y in range(0, 85):  # loop through all 255 colors
            rgb = twitch_bot_utils.Wheel(y * 3)
            self.ser.write("#%c%c%c\xff!" % (rgb[0], rgb[1], rgb[2]))
            pygame.time.wait(40)
            self.ser.write("#\x00\x00\x00\xff!")
            pygame.time.wait(40)
            if self.event == 1:
                logging.log(logging.INFO, "Event! Stopping user command")
                self.set_animating(0)
                return
        self.modedefault()
        return

    def chase(self, r, g, b, num=6):
        self.wait_animating()
        self.set_animating(1)
        logging.log(logging.DEBUG, "%s,%s,%s" % (r, g, b))
        for x in range(0, num):  # chase animation num times
            for y in range(0, 30):  # chase across all 30 leds
                for z in range(0, 30):  # draw the pixels
                    if z > y - 3 and z < y + 3:
                        self.ser.write("#%c%c%c%c" % (r, g, b, z))
                    else:
                        self.ser.write("#\x00\x00\x00%c" % z)
                        self.ser.write("!")
                if self.event == 1:
                    logging.log(logging.INFO, "Event! Stopping user command")
                    self.set_animating(0)
                    return
                pygame.time.wait(10)
            pygame.time.wait(500)
        self.set_animating(0)
        return

    def disco_chase(self, num=6):
        self.wait_animating()
        self.set_animating(1)
        logging.log(logging.INFO, "Disco Chase")
        self.irc.msg("DISCO CHASES!!!!!!!!")
        color = 0
        for x in range(0, num):  # chase animation num times
            for y in range(0, 30):  # chase across all 30 leds
                color += 10
                if color > 255:
                    color = 0
                rgb = twitch_bot_utils.Wheel(color)
                for z in range(0, 30):  # draw the pixels
                    if z > y - 3 and z < y + 3:
                        self.ser.write("#%c%c%c%c" % (rgb[0], rgb[1], rgb[2], z))
                    else:
                        self.ser.write("#\x00\x00\x00%c" % z)
                self.ser.write("!")
                if self.event == 1:
                    logging.log(logging.INFO, "Event! Stopping user command")
                    self.set_animating(0)
                    return
                pygame.time.wait(10)
            pygame.time.wait(500)
        self.set_animating(0)
        self.modedefault()
        return

    def bounce(self, r, g, b, num=6):
        self.wait_animating()
        self.set_animating(1)
        logging.log(logging.DEBUG, "%s,%s,%s" % (r, g, b))
        for x in range(0, num):  # chase animation num times
            for y in range(0, 30):  # chase across all 30 leds
                for z in range(0, 30):  # draw the pixels
                    w = y * 2
                    if y > 15:
                        w = (15 - (y - 15)) * 2
                    if z > w - 3 and z < w + 3:
                        self.ser.write("#%c%c%c%c" % (r, g, b, z))
                    else:
                        self.ser.write("#\x00\x00\x00%c" % z)
                self.ser.write("!")
                if self.event == 1:
                    logging.log(logging.INFO, "Event! Stopping user command")
                    self.set_animating(0)
                    return
                pygame.time.wait(10)
            pygame.time.wait(500)
        self.set_animating(0)
        return

    def centerchase(self, r, g, b, num=6):
        self.wait_animating()
        self.set_animating(1)
        logging.log(logging.DEBUG, "%s,%s,%s" % (r, g, b))
        for x in range(0, num):  # chase animation num times
            for y in range(0, 30):  # chase across all 30 leds
                for z in range(0, 30):  # draw the pixels
                    center = 15 - abs(y - 15)
                    left = 15 + center
                    right = 15 - center
                    if (z > left - 2 and z < left + 2) or (z > right - 2 and z < right + 2):
                        self.ser.write("#%c%c%c%c" % (r, g, b, z))
                    else:
                        self.ser.write("#\x00\x00\x00%c" % z)
                self.ser.write("!")
                if self.event == 1:
                    logging.log(logging.INFO, "Event! Stopping user command")
                    self.set_animating(0)
                    return
                pygame.time.wait(10)
            pygame.time.wait(500)
        self.set_animating(0)
        return

    def alternate(self, r1, g1, b1, r2, g2, b2):
        self.wait_animating()
        self.set_animating(1)
        logging.log(logging.DEBUG, "%s,%s,%s,%s,%s,%s" % (r1, g1, b1, r2, g2, b2))
        for y in range(0, 10):
            r1, r2 = r2, r1  # swap colors
            g1, g2 = g2, g1
            b1, b2 = b2, b1
            for x in range(0, 30):
                if x < 15:  # draw the first color to 0-14
                    self.ser.write("#%c%c%c%c" % (r1, g1, b1, x))
                else:  # and the second to 15-30
                    self.ser.write("#%c%c%c%c" % (r2, g2, b2, x))
            self.ser.write("!")
            if self.event == 1:
                logging.log(logging.INFO, "Event! Stopping alternate")
                self.set_animating(0)
                return
            time.sleep(0.5)
        self.modedefault()
        return

    def disco_alternate(self):
        self.wait_animating()
        self.set_animating(1)
        w = 0
        x = 128
        for y in range(0, 255):  # loop through all 255 colors
            if (y % 24) == 0:
                w, x = x, w
            rgb = twitch_bot_utils.Wheel((y + x) % 255)
            rgb2 = twitch_bot_utils.Wheel((y + w) % 255)
            for z in range(0, 30):
                if z < 15:  # draw the first color to 0-14
                    self.ser.write("#%c%c%c%c" % (rgb[0], rgb[1], rgb[2], z))
                else:  # and the second to 15-30
                    self.ser.write("#%c%c%c%c" % (rgb2[0], rgb2[1], rgb2[2], z))
            if self.event == 1:
                logging.log(logging.INFO, "Event! Stopping user command")
                self.set_animating(0)
                return
            self.ser.write("!")
            pygame.time.wait(5)
        self.modedefault()
        return

    # fire animation using 2 colors
    # todo add gradients
    def fire(self, r1, g1, b1, r2, g2, b2):
        self.wait_animating()
        self.set_animating(1)
        self.irc.msg("FIRE!!!")
        for y in range(0, 30):
            for x in range(0, 30):
                r = random.randrange(2)
                if r == 1:
                    self.ser.write("#%c%c%c%c" % (r1, g1, b1, x))
                else:
                    self.ser.write("#%c%c%c%c" % (r2, g2, b2, x))
            self.ser.write("!")
            if self.event == 1:
                logging.log(logging.INFO, "Event! Stopping fire")
                self.set_animating(0)
                return
            time.sleep(0.1)
        self.modedefault()
        return

    # disco fire
    # todo add gradients
    def disco_fire(self):
        self.wait_animating()
        self.set_animating(1)
        self.irc.msg("DISCO FIRE!!!")
        for y in range(0, 30):
            for x in range(0, 30):
                c = twitch_bot_utils.Wheel(((random.randint(1, 32) + self.random_color) * 7) % 255)
                self.ser.write("#%c%c%c%c" % (c[0], c[1], c[2], x))
            self.ser.write("!")
            if self.event == 1:
                logging.log(logging.INFO, "Event! Stopping disco fire")
                self.set_animating(0)
                return
            time.sleep(0.1)
        self.modedefault()
        return

    def allleds(self, r, g, b, wait):
        self.wait_animating()
        self.set_animating(1)
        self.ser.write("#%c%c%c\xff!" % (r, g, b))
        self.user_wait(wait)
        self.modedefault()
