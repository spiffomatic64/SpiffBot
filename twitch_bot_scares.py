#! python2

import twitch_bot_utils
import ctypes
import logging
import time

class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

class scares:
    def __init__(self, ser, irc,event):
        self.next_scary_game = "http://strawpoll.me/3800715"
        self.event = event

        # Map of sound commands to sound files
        self.sounds = {"slam": "SOUND_1277.ogg",
                  "screech": "SOUND_1288.ogg",
                  "heartbeat": "SOUND_1323.ogg",
                  "crash": "SOUND_1399.ogg",
                  "highbang": "SOUND_1463.ogg",
                  "deep": "SOUND_1465.ogg",
                  "eery": "SOUND_1467.ogg",
                  "creak": "SOUND_1507.ogg",
                  "lownoise": "SOUND_1511.ogg",
                  "deepbang": "SOUND_1528.ogg",
                  "clang": "SOUND_1598.ogg",
                  "boom": "SOUND_1603.ogg",
                  "scrape": "SOUND_1604.ogg",
                  "creepy": "SOUND_1608.ogg",
                  "techno": "SOUND_1630.ogg",
                  "animal": "SOUND_0004.ogg",
                  "creeky": "SOUND_0012.ogg",
                  "robot": "SOUND_0029.ogg",
                  "rhythm": "SOUND_0030.ogg",
                  "open": "SOUND_0042.ogg",
                  "locked": "SOUND_0072.ogg",
                  "hiss": "SOUND_0195.ogg",
                  "moan": "SOUND_0296.ogg",
                  "static": "sh2static2.ogg",
                  "kids": "kids.ogg",
                  "cutting": "3dcut.ogg",
                  "sawing": "3dbread.ogg",
                  "normalzombie": "zombie_scare.ogg",
                  "tentacle": "stinger_tentacle.ogg",
                  "sting": "sting.ogg",
                  "bigzombie": "large_zombie.ogg",
                  "hunter": "hunter.ogg",
                  "brute": "brute.ogg",
                  "zombieattack": "zombie_attack_walk.ogg",
                  "spawn": "aslt_spwn_01.ogg",
                  "birds": "birdflock_calls_medium_loop_v1.ogg",
                  "teleport": "taken_flanker_tele_01.ogg",
                  "wings": "birdflock_wings_medium_loop_v1.ogg",
                  "subtlebirds": "subtle_birds.ogg",
                  "scream": "female_scream.ogg",
                  "footsteps": "footsteps.ogg",
                  "rezombie": "rezombie.ogg",
                  "recreature": "recreature.ogg",
                  "subsonic": "subsonic.ogg",
                  "mgalert": "metalgearalert.ogg",
                  "headshot": "headshot.ogg",
                  "ding": "ding.ogg"
                  }
        xinput = ctypes.windll.xinput1_1

        self.XInputSetState = xinput.XInputSetState
        self.XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
        self.XInputSetState.restype = ctypes.c_uint

        vibration = XINPUT_VIBRATION(0, 0)
        self.XInputSetState(0, ctypes.byref(vibration))

    def set_event(self, event):
        self.event = event

    def set_vibration(self,controller, left_motor, right_motor):
        vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
        self.XInputSetState(controller, ctypes.byref(vibration))

    def cdrom(self, wait, scare):

        ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
        ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door closed", None, 0, None)
        time.sleep(status_length)
        scare_status(-1)
        time.sleep(wait - status_length)
        scare_lock(0)
        if scare == 0:
            switch()


    def arduino_scare(self, pin, start, stop, command, msg, dur, wait, times, scare):
        scare_lock(1)
        scare_status(msg)
        logging.log(logging.INFO, "Arguino scare, scare=%s" % scare)
        status_length = 3
        logging.log(logging.DEBUG, "%s %s time(s)" % (msg, times))
        for i in range(0, times):
            ser.write("#%c%c\x00%c" % (pin, start, command))
            time.sleep(dur)
            ser.write("#%c%c\x00%c" % (pin, stop, command))
        time.sleep(status_length)
        scare_status(-1)
        time.sleep(wait - status_length)
        scare_lock(0)
        if scare == 0:
            switch()


    def spasm_scare(self, wait, scare):
        scare_lock(1)
        scare_status("Spasm!!!!!")
        status_length = 3
        ser.write("#%c%c\x00%c" % (10, 130, 254))
        ser.write("#%c%c\x00%c" % (9, 130, 254))
        ser.write("#%c%c\x00%c" % (3, 0, 254))
        ser.write("#%c%c\x00%c" % (11, 1, 253))
        ser.write("#%c%c\x00%c" % (5, 0, 254))
        time.sleep(status_length)
        ser.write("#%c%c\x00%c" % (10, 40, 254))
        ser.write("#%c%c\x00%c" % (9, 40, 254))
        ser.write("#%c%c\x00%c" % (3, 180, 254))
        ser.write("#%c%c\x00%c" % (11, 0, 253))
        ser.write("#%c%c\x00%c" % (5, 180, 254))
        time.sleep(status_length)
        scare_status(-1)
        time.sleep(wait - status_length)
        scare_lock(0)
        if scare == 0:
            switch()


    def play_sound(self, sound, left, right):
        logging.log(logging.DEBUG, pygame.mixer.get_init())
        logging.log(logging.INFO, "Playing sound %s" % sound)
        mixer = pygame.mixer.Sound("./sounds/%s" % sound)
        channel = mixer.play()
        channel.set_volume(left, right)

        clock = pygame.time.Clock()
        # wait for playback to be finished
        while channel.get_busy():
            clock.tick(30)


    def sound_scare(self, sound, left, right, scare=0):
        scare_lock(1)
        play_sound(sound, left, right)
        scare_lock(0)
        if scare == 0:
            switch()

    def profile(self):
        # Twitch profile generator
        twitch_bot_utils.twitch_profile("#Scary mode:")
        twitch_bot_utils.twitch_profile("%s will randomly pick someone in chat to be \"in control\"." % auth.get_bot())
        twitch_bot_utils.twitch_profile(
            "This person will have 5 minutes (with a 2.5 minute warning letting you know how much time is left) to use a \"scare\" command.")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("##Scare Commands for the user in \"Control\"")
        twitch_bot_utils.twitch_profile("**!randomscare** : Picks a action scare randomly  ")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**drop**, **quiet**, **door**, or **gun** :Drops a small cardboard box directly in front of me, that no matter how far in advance I know its coming, always seems to scare the pants off me...  ")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**brush**, **pants**, **spider**, or **crawl** :This is by far the most overpowered scare we have, its a server strapped to my leg, that grabs my pants and makes it feel like someone is tugging at my pants")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**touch**, **shoulder**, or **tapping** :This will move a servo (twice) attached to my shoulder that emulates someone tapping on it")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**rattle**, **fall**, or **desk** :Turns on a vibration motor I took out of an xbox controller, that will rattle around making noise/vibrations/ and movement out of the corner of my eye... Will most likely also scare the pants off me...")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**back**, **spine**, **buzz**, **neck** : This will move a servo (twice) attached to my neck that emulates someone tapping on it")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**flip** : Flips my main monitor image 180 degrees (vertically) for 30 full seconds (everything should look normal on the stream though)")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("**monitor** : Turns off all monitors at once, for a solid 2.5 seconds")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("**flicker** : Strobes the monitor (30 frames of black 10 frames of video)")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**volume**, **mute** : Disables audio completely (for me only) for a short period of time (cheatme1)")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**spasm**, **shake**, **shiver** or **electrocute** : Enables all scares for a short second (Falconslayer87)")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**spoopy**: Show scary gif in the middle of the monitor for split second (MolecularSwords)")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile(
            "**noput**: Disable mouse and keyboard sporadically (Falconslayer87/MolecularSwords)")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("**cdrom**: Open Cdrom drive SillyBilly79")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("**minimize**: Minimize all windows SillyBilly79")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("##Scary sound commands for the user in \"Control\"")
        twitch_bot_utils.twitch_profile("You can preview the sounds [Here](http://spiffomatic64.com/twitch/sounds)")
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("**!randomsound** : Picks a sound scare randomly")
        twitch_bot_utils.twitch_profile("")

        sound_buffer = ""
        for sound, file in self.sounds.iteritems():
            sound_buffer = "%s**%s**, " % (sound_buffer, sound)
        twitch_bot_utils.twitch_profile(sound_buffer)
        twitch_bot_utils.twitch_profile("")
        twitch_bot_utils.twitch_profile("##Other commands for the user in \"Control\"")
        twitch_bot_utils.twitch_profile(
            "**!pass** : allows you to pass control on to the person who has not had control in the longest instead of using it yourself. If you add a username after !pass, you can pass control to someone specifically")