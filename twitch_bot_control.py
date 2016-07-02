#! python2

import logging
import twitch_bot_utils
import threading

class event:
    def __init__(self):
        self.active = 0

    def isActive(self):
        return self.active

    def setActive(self,active):
        self.active = active

class control:
    def __init__(self, irc, db):
        self.event = event()
        self.irc = irc
        self.db = db

        master = auth.get_streamer()
        pass_counter = 3
        last_pass = None
        switching = 0
        next_user = []
        scaring = 0

        mode = 2  # twitch_bot_utils.scaryDay()


    def opt(self, user, inout, passed=None):
        user = user.lower()
        if inout:
            if not self.db.getUserOpted(user):
                self.db.updateUserOpted(user, 1)
                if master == auth.get_bot():
                    switch(user)
        else:
            if user == auth.get_streamer():
                switch()
            elif db.getUserOpted(user):
                db.updateUserOpted(user, 0)
                if user == master:
                    if passed:
                        switch(passed)
                    else:
                        switch()


    def autoOptIn(user, data):
        global next_user

        users = db.getUsers()

        if not users or user not in db.getUsers():
            logging.log(logging.INFO, "Auto Opting %s in!" % user)
            opt(user, True)
            irc.msg("Check out this 1 minute video that explains my stream! https://www.youtube.com/watch?v=q0q8SML6d_I")
            logging.log(logging.INFO, "Setting next user to: %s" % user)
            if mode == 0:
                irc.msg("Giving next control to our newest viewer: %s" % user)
                next_user.append(user)
            return True

    def scare_lock(status):
        global scaring
        logging.log(logging.INFO, "Setting scaring: %s" % status)
        scaring = status

    # Thread responsible for switching control
    def mastertimer():
        global counter
        global switching

        warn_timer = 0
        counter = time.time()

        while True:
            if mode <= 1:
                elapsed = time.time() - counter
                if elapsed > 390 or elapsed < 0:
                    scare_lock(0)
                    switching = 0
                    logging.log(logging.WARNING, "Elapsed out of bounds!: %s" % elapsed)

                if scaring == 0 and switching == 0:
                    # every 5 minutes switch control, and remove master from optedin list 300
                    if elapsed > 300:
                        if master != auth.get_bot():
                            irc.msg("5 Minutes elapsed! Switching control, and opting %s out!" % master)
                            logging.log(logging.WARNING,
                                        "Passing control and opting out %s(due to timeout from mastertimer)" % master)
                            if last_pass:
                                logging.log(logging.INFO, "Passing back to user %s" % last_pass)
                                opt(master, False, last_pass)
                            else:
                                opt(master, False)
                        logging.log(logging.INFO, "Master switch")
                        counter = time.time()
                        warn_timer = 0
                    # every 2.5 minutes warn the user in control 150 (make sure to only warn once)
                    elif elapsed > 150 and warn_timer == 0:
                        if master != auth.get_bot():
                            try:
                                viewers = get_viewers()
                                if master in viewers:
                                    irc.msg("2.5 Minutes left %s!" % master)
                                    logging.log(logging.WARNING, "Sending 2.5 minute warning")
                                else:
                                    irc.msg("%s is not in viewer list, Switching control!" % master)
                                    if last_pass:
                                        switch(last_pass)
                                    else:
                                        switch(-1)
                                    counter = time.time()
                            except:
                                irc.msg("2.5 Minutes left %s!" % master)
                                logging.log(logging.WARNING, "Sending 2.5 minute warning")
                        warn_timer = 1

                    logging.log(logging.DEBUG, elapsed)
                    logging.log(logging.DEBUG, last_pass)
            elif mode == 2:
                elapsed = time.time() - counter
                logging.log(logging.DEBUG, elapsed)
                if elapsed > 300 or elapsed < 0:
                    spam_msg = random.choice(spam.keys())
                    send = spam[spam_msg]
                    irc.msg(spam[spam_msg])
                    user_commands(auth.get_bot(), spam_msg)
                    counter = time.time()
            time.sleep(1)


    # switch control to a random person (or specific person if specified)
    def switch(user="", pass_control=0):
        global counter
        global master
        global switching
        global next_user
        global pass_counter
        global last_pass

        logging.log(logging.INFO, "Switching with user: %s" % user)
        # if warn timer is not -1, set warn timer to -1, then back to 0 at the end of the function
        # This is used to lock the switch thread (to prevent double switching)
        if switching == 0 and scaring == 0 and mode <= 2:
            switching = 1

            # pass limiting logic
            logging.log(logging.INFO, "Pass Counter: %s" % pass_counter)
            if pass_control == 0:  # reset pass counter
                pass_counter = 0
            elif pass_control == 1:  # increment pass_counter
                pass_counter += 1
            if pass_counter > 2 and pass_control != -1:
                irc.msg("Too many passes to specific users, use a command, or !pass without a username")
                switching = 0
                return

            old = master
            logging.log(logging.INFO, "getting viewers")
            try:
                viewers = get_viewers()
            except:
                logging.log(logging.ERROR, "*************Twitch Api is borked*************")
                master = auth.get_bot()
                last_pass = None
                logging.log(logging.WARNING, "%s is now in control!" % master)
                irc.msg("%s is now in control!" % master)
                logging.log(logging.WARNING, "Switching from %s to %s" % (old, master))
                db.updateLastControl(master)
                counter = time.time()
                switching = 0
                return

            # remove the current controller from available viewers to prevent switching to the same person
            if master in viewers:
                viewers.remove(master)

            # add logic for fairness


            # if a "next" user is specified, switch to that user
            if len(next_user) > 0:
                logging.log(logging.INFO, "next_user was set to: %s" % next_user)
                if user == "":
                    logging.log(logging.WARNING, "user is not set")
                    user = next_user.pop(0)

            # Switch to user if specified
            if user in viewers:
                logging.log(logging.INFO, "User is set: %s" % user)
                master = user
                last_pass = None
            else:
                # if there are more than 0 viewers, pick a random viewer
                if len(viewers) > 0:

                    if user == -1:
                        master = db.getLastControl(viewers)
                    else:
                        random.shuffle(viewers)  # probably not needed, but what the hell :-P
                        master = random.choice(viewers)
                else:
                    logging.log(logging.WARNING, "No valid viewers to switch to")
                    master = auth.get_bot()
                last_pass = None
            # reset counter and notify chat that a new viewer is in control
            logging.log(logging.INFO, "%s is now in control!" % master)
            irc.msg("%s is now in control!" % master)
            logging.log(logging.INFO, "Switching from %s to %s" % (old, master))
            db.updateLastControl(master)
            counter = time.time()
            switching = 0
        else:
            logging.log(logging.WARNING, "Another switch is in progress")

    def setMode(type):
        global mode
        global counter

        if type == "scary" or type == 0:
            mode = 0
            logging.log(logging.INFO, "Scary time!")
            counter = time.time()
            master = auth.get_streamer()
            irc.msg("ITS SCARY TIME!!!")
            modedefault()
            return True
        if type == "troll" or type == 1:
            mode = 1
            logging.log(logging.INFO, "Troll time!")
            counter = time.time()
            irc.msg("LETS TROLL %s!!!" % auth.get_streamer_short().upper())
            modedefault()
            return True
        if type == "light" or type == 2:
            mode = 2
            logging.log(logging.INFO, "Lights time!")
            irc.msg("LIGHTS ARE PRETTY!!!")
            modedefault()
            return True

    # commands that will only work for me (and moderators in the future)
    def admin_commands(user, data):
        global next_user
        global stayAlive

        # if user.lower() == auth.get_streamer():
        if auth.is_admin(user):
            # split irc messages into parts by white space
            parts = data.lower().split()
            logging.log(logging.INFO, "User is admin, checking for commands")
            command = parts[0][1:]  # get the first "word" and remove the first character which is ":"
            if command == "!switch":
                # if there is something after switch command, try to switch to that user
                if len(parts) == 2:
                    switch(parts[1], -1)
                    return True
                if len(parts) == 1:
                    switch()
                    return True
            if command == "!restart" or command == "!reload":
                stayAlive = 0
            if command == "!whosoptedin":
                optedin = ""
                try:
                    viewers = get_viewers()
                    for optins in db.getOptedUsers():
                        if optins in viewers:
                            optedin = "%s %s " % (optedin, optins)
                    irc.msg("%s" % optedin)
                except:
                    irc.msg("Twitch api is borked :(")
                return True
            '''if command == "!midi":
                logging.log(logging.INFO,midi.toggleMidi())'''
            if command == "!raffle":
                raffle()
                return True

            # if there are at least 2 words in the message
            if len(parts) == 2:
                for part in parts:
                    logging.log(logging.DEBUG, part)
                # add user to opted in list
                if command == "!optin":
                    opt(parts[1], True)
                    irc.msg("Opting %s in" % parts[1])
                    return True
                # optout a user
                if command == "!optout":
                    # check that user is already opted in
                    opt(parts[1], False)
                    return True
                # change mode between scary troll and light
                if command == "!mode":
                    if setMode(parts[1]):
                        return True
                if command == "!switchnext":
                    logging.log(logging.INFO, "Setting next user to: %s" % parts[1])
                    next_user.append(parts[1])
                    return True

    def event_status(status):
        logging.log(logging.INFO, "Scare status: %s" % status)
        f = open('scarestatus.txt', 'w')
        if status == -1:
            f.truncate()
        else:
            f.write(status)
        f.close()

    twitch_profile(-1)
    twitch_profile("Here are the commands you can use to play along, and interact with my \"%s\"" % auth.get_bot())
    twitch_profile("")
    twitch_profile(
        "%s has 3 main modes: Scary (Thurs-Sunday), Troll (Mon-Weds), Light (Only control of lights)" % auth.get_bot)
    twitch_profile("")

    # commands only accessible by the user in control
    def master_commands(user, data):
        global master
        global sounds
        global last_pass

        # check that the user is the master, and we are in scary mode
        if scaring == 0 and switching == 0 and (
                user.lower() == master.lower() or user.lower() == auth.get_streamer()) and mode <= 1:
            if user.lower() == auth.get_streamer():
                logging.log(logging.INFO, "User is admin, dont switch")
                admin = 1
            else:
                admin = 0
            logging.log(logging.INFO, "User is in control, checking for commands")
            parts = data.lower().split()
            command = parts[0][1:]

            logging.log(logging.INFO, "%s == %s" % (user.lower(), master.lower()))
            # allow a user to pass to someone else, or to someone random
            if command == "!passnew":
                logging.log(logging.INFO, "%s pasing to whoever has not had control in the longest!" % user.lower())
                switch(-1)
                return True

            if command == "!pass":
                if len(parts) == 1:
                    logging.log(logging.INFO, "%s pasing to whoever has not had control in the longest!" % user.lower())
                    switch(-1)
                    last_pass = user
                    return True
                if len(parts) == 2:
                    if user.lower() != parts[1].lower():
                        if parts[1].lower() in db.getOptedUsers():
                            logging.log(logging.INFO, "%s pasing to %s" % (user.lower(), parts[1].lower()))
                            switch(parts[1], 1)
                            last_pass = user
                            return True
                        elif parts[1].lower() == "new" or parts[1].lower() == "newuser":
                            logging.log(logging.INFO,
                                        "%s pasing to whoever has not had control in the longest!" % user.lower())
                            switch(-1)
                            last_pass = user
                            return True
                        else:
                            irc.msg("Can't pass, %s is opted out!" % parts[1].lower())
                            logging.log(logging.WARNING,
                                        "%s tried to pass to %s who is opted out" % (user.lower(), parts[1].lower()))
                            return True
                    else:
                        irc.msg("You cant pass to yourself!")
                        logging.log(logging.WARNING, "%s tried to pass to them-self" % user.lower())
                        return True

            # sound commands
            song = ''

            # select a random sound
            if command == "!randomsound":
                logging.log(logging.INFO, "Random sound")
                song = random.choice(sounds.values())

            # check message for all sound commands
            for sound, file in sounds.iteritems():
                if data.find(sound) != -1:
                    logging.log(logging.DEBUG, "Found %s in %s" % (sound, data))
                    song = file
                    break  # stop after the first sound command is found
            if song != '':  # if a sound was selected
                # check for left/right
                left = 1
                right = 1
                if data.find("left") != -1:
                    logging.log(logging.DEBUG, "Found left")
                    right = 0
                elif data.find("right") != -1:
                    logging.log(logging.DEBUG, "Found right")
                    left = 0
                # Play sound in a thread
                scare = threading.Thread(target=sound_scare, args=(song, left, right, admin))
                scare.daemon = True
                scare.start()
                return True

            # select a random scare command
            if (command == "!randomscare" or command == "!butts") and mode == 0:
                data = random.choice(
                    ["drop", "brush", "tapping", "spine", "rattle", "spasm", "vibe", "flip", "monitor", "mute", "wiggle",
                     "flicker", "dark", "blindspot", "spoopy", "wasd"])

            if command == "!randomtroll" and mode == 1:
                data = random.choice(["flip", "monitor", "mute", "wiggle", "flicker", "dark", "blindspot", "wasd"])

            # make this configurable
            wait = random.randint(4, 30)
            logging.log(logging.INFO, "Random wait: %s" % wait)

            # flip the main monitor
            if data.find('flip') != -1:
                scare = threading.Thread(target=flip, args=(30 + wait, admin))
                scare.daemon = True
                scare.start()
                return True

            # disable all monitors
            if data.find('monitor') != -1:
                scare = threading.Thread(target=turn_off_monitors, args=("Monitors disabled!", wait + 3, admin))
                scare.daemon = True
                scare.start()
                return True
            # changes volume
            if data.find('volume') != -1 or data.find('mute') != -1:
                scare = threading.Thread(target=change_volume, args=(wait + 3, -50.0, admin))
                scare.daemon = True
                scare.start()
                return True

                # Wiggle active window
            if data.find('wiggle') != -1:
                scare = threading.Thread(target=wiggle, args=(wait + 3, admin))
                scare.daemon = True
                scare.start()
                return True

                # flip the main monitor and switch control (broken atm)
            if data.find('flicker') != -1:
                scare = threading.Thread(target=flicker, args=(admin,))
                scare.daemon = True
                scare.start()
                return True

            # Dim the main monitor
            if data.find('dark') != -1:
                scare = threading.Thread(target=dark, args=(admin,))
                scare.daemon = True
                scare.start()
                return True

            # Dim the main monitor
            if data.find('blindspot') != -1:
                scare = threading.Thread(target=box, args=(admin,))
                scare.daemon = True
                scare.start()
                return True

            # Show gif scare
            if data.find('spoopy') != -1:
                scare = threading.Thread(target=gif, args=(wait + 3, admin))
                scare.daemon = True
                scare.start()
                return True

            # send random wasd keys
            if data.find('wasd') != -1:
                scare = threading.Thread(target=wasd, args=(admin,))
                scare.daemon = True
                scare.start()
                return True

            if data.find('vibe') != -1:
                left = 0
                right = 0
                if data.find('left') != -1:
                    left = 1
                if data.find('right') != -1:
                    right = 1
                if left == 0 and right == 0:
                    left = 1
                    right = 1
                if data.find('soft') != -1:
                    left *= 0.3
                    right *= 0.3

                scare = threading.Thread(target=vibrate, args=(wait + 3, left, right, admin))
                scare.daemon = True
                scare.start()
                return True

            if data.find('noput') != -1:
                scare = threading.Thread(target=noput, args=(admin,))
                scare.daemon = True
                scare.start()
                return True

            if data.find('minimize') != -1:
                scare = threading.Thread(target=minimize, args=(wait, admin))
                scare.daemon = True
                scare.start()
                return True

            if data.find('drunk') != -1:
                scare = threading.Thread(target=drunk, args=(admin,))
                scare.daemon = True
                scare.start()
                return True

            if mode == 0:
                # Drop the box on me by moving the arm down for 2 seconds, then waiting 20 seconds
                if data.find('quiet') != -1 or data.find('door') != -1 or data.find('drop') != -1 or data.find('gun') != -1:
                    scare = threading.Thread(target=arduino_scare,
                                             args=(10, 130, 40, 254, "Dropping box", 1, wait, 1, admin))
                    scare.daemon = True
                    scare.start()
                    return True

                # Move the servo attached to my legs
                if data.find('brush') != -1 or data.find('pants') != -1 or data.find('spider') != -1 or data.find(
                        'crawl') != -1:
                    scare = threading.Thread(target=arduino_scare,
                                             args=(9, 130, 40, 254, "Moving leg servo", 1, wait, 1, admin))
                    scare.daemon = True
                    scare.start()
                    return True

                # Move the servo attached to my shoulder
                if data.find('touch') != -1 or data.find('shoulder') != -1 or data.find('tapping') != -1:
                    scare = threading.Thread(target=arduino_scare,
                                             args=(3, 0, 180, 254, "Moving shoulder servo", 1, wait, 3, admin))
                    scare.daemon = True
                    scare.start()
                    return True

                # rattle the vibration motor for 2 seconds, then wait 20 seconds
                if data.find('rattle') != -1 or data.find('fall') != -1 or data.find('desk') != -1:
                    scare = threading.Thread(target=arduino_scare, args=(11, 1, 0, 253, "Desk vibe", 2, wait, 1, admin))
                    scare.daemon = True
                    scare.start()
                    return True

                # Move the servo down my shirt
                if data.find('back') != -1 or data.find('spine') != -1 or data.find('buzz') != -1 or data.find(
                        'neck') != -1:
                    scare = threading.Thread(target=arduino_scare,
                                             args=(5, 0, 180, 254, "Moving spine servo", 1, wait, 3, admin))
                    scare.daemon = True
                    scare.start()
                    return True

                # rattle the smaller vibration motor for 2 seconds, then wait 20 seconds
                if data.find('spasm') != -1 or data.find('shake') != -1 or data.find('shiver') != -1 or data.find(
                        'electrocute') != -1:
                    scare = threading.Thread(target=spasm_scare, args=(wait, admin))
                    scare.daemon = True
                    scare.start()
                    return True

                # rattle the smaller vibration motor for 2 seconds, then wait 20 seconds
                if data.find('cdrom') != -1:
                    scare = threading.Thread(target=cdrom, args=(wait, admin))
                    scare.daemon = True
                    scare.start()
                    return True

    twitch_profile("##Commands for everyone (even if you don't have control)")
    twitch_profile("These commands, are available to everyone (even when not in control)  ")
    twitch_profile("**!status** : lets you know who is currently in control, and how much time left they have  ")
    twitch_profile("**!whosgotit** : lets you know who is currently in control  ")
    twitch_profile("**!timeleft** : lets you know much much time is left before control is shifted  ")
    twitch_profile("**!optout** : lets you opt out of getting picked for control")
    twitch_profile("**!optin** : lets you opt back in to get control")
    twitch_profile("**!opted username** : lets you check if a specific user is opted in or out")
    twitch_profile("**!game** : lets you know what game we are currently playing")
    twitch_profile("**!nextgame** : lets you know what game we are going to play next")
    twitch_profile("**!nextscarygame** : Brings up the current poll for what scary game is next")
    twitch_profile("")

    # commands accessible by all users
    def user_commands(user, data):
        global user_stack

        parts = data.split()
        command = parts[0][1:]

        logging.log(logging.DEBUG, "Checking %s for user commands..." % data)

        # start commands
        if data.find('test') != -1:
            irc.msg("test to you too!")
            return True

        # Scary mode only commands
        if mode <= 1:
            hide = False
            if data.find("!hide") != -1:
                hide = True
            if data.find("!scarecommands") != -1 or data.find("!scarelist") != -1 or data.find("!scares") != -1:
                irc.msg(
                    "!hide Scare commands: !randomscare, drop, brush, tapping, rattle, spine, flip, monitor, flicker, mute, dark, wasd, wiggle, and spasm. Use !scaresounds to list sound scares.",
                    hide)
                return True
            if data.find("!trollcommands") != -1 or data.find("!trolllist") != -1 or data.find("!trolls") != -1:
                irc.msg(
                    "!hide Troll commands: !randomtroll, flip, monitor, flicker, mute, dark, wasd, wiggle, vibe and blindspot. Use !sounds to list sounds.",
                    hide)
                return True
            if data.find("!sounds") != -1 or data.find("!soundscares") != -1 or data.find("!soundlist") != -1:
                temp = ""
                for sound, file in sounds.iteritems():
                    temp = temp + sound + ", "
                temp = temp[:-2]
                irc.msg("!hide Available sounds: %s" % temp, hide)
                return True
            if data.find("!patience") != -1:
                irc.msg(
                    "You can only do scares/trolls when it is your turn as long as you are optin'd %s will pick you at random" % auth.get_bot(),
                    hide)
                return True
            if data.find("!status") != -1 or data.find("!timeleft") != -1 or data.find("!whosgotit") != -1:
                if scaring == 1:
                    if mode == 0:
                        irc.msg("%s is currently scaring..." % master, hide)
                    if mode == 1:
                        irc.msg("%s is currently trolling..." % master, hide)
                    return True
                if data.find("!status") != -1:
                    timeleft = round(300 - (time.time() - counter))
                    irc.msg("%s is currently in control, with %s seconds left!" % (master, timeleft), hide)
                    return True
                # let viewers know how much time is left
                if data.find("!timeleft") != -1:
                    timeleft = 300 - (time.time() - counter)
                    irc.msg("%s has %s seconds left!" % (master, round(timeleft)), hide)
                    return True
                if data.find("!whosgotit") != -1:
                    irc.msg("%s is currently in control!" % (master), hide)
                    return True
            # opt a user in, and switch if they were in control
            if command == "!optin":
                opt(user, True)
                irc.msg("%s is now opted in!" % user)
                return True
            # allow a user to optout
            if command == "!optout":
                opt(user, False)
                irc.msg("%s is now opted out!" % user)
                return True
            if command == "!opted":
                opt_status = "out"
                if len(parts) == 1:
                    parts.append(user)
                if db.getUserOpted(parts[1]):
                    opt_status = "in"
                irc.msg("%s is opted %s!" % (parts[1], opt_status))
                return True
            if data.find("am i opted") != -1:
                if user in db.getOptedUsers():
                    opted = "in"
                else:
                    opted = "out"
                irc.msg("%s is opted %s" % (user, opted))
                return True

        # Get current streaming game
        if command == "!nextgame" or (data.find('what game') != -1 and data.find('next') != -1):
            irc.msg("The next game is: %s! and vote/check the status of the next scary game here: %s" % (
            get_next_game(), next_scary_game))
            return True

        # Get current streaming game
        if command == "!nextscarygame" or (data.find('what game') != -1 and data.find('next') != -1):
            irc.msg("The next scary game is determined by you! Vote/Check the status here: %s!" % next_scary_game)
            return True
        if command == "!colors":
            irc.msg(
                "Color commands: disco, disco strobe, disco alternate, disco chase, disco fire, fire(red|blue), strobe, chase(red|white|blue), centerhase(red|white|blue), alternate(red|blue), randomcolor")
            return True
        if command == "!intro":
            irc.msg("Check out this 1 minute video that explains my stream! https://www.youtube.com/watch?v=q0q8SML6d_I")
            return True

        if command == "!multi" or command == "!multitwitch":
            irc.msg("Watch me and %s here: http://multitwitch.tv/%s/%s" % (
            auth.get_multi(), auth.get_streamer(), auth.get_multi()))
            return True

        if data.find("!whiteboard") != -1:
            irc.msg("Draw on my screen here: http://webwhiteboard.com/#cra5z59h")
            return True

        if command == "!github":
            irc.msg("Add suggestions here! https://github.com/spiffomatic64/SpiffBot/issues")
            return True

        if command == "!twitter":
            irc.msg("Follow me on twitter for stream related updates! https://twitter.com/%s" % auth.get_twitter())
            return True

        if command == "!game" or data.find('what game') != -1:
            irc.msg("The current game is: %s" % get_game())
            return True

        if command == "!games":
            irc.msg(
                "List of \"Best of the best\" https://docs.google.com/spreadsheets/d/1m1Jq_zOJg-BUWDY-Ir7KFGQsKCU3RcdU3eLW5_czKis/edit#gid=0")
            return True

        if command == "!halley":
            irc.msg(
                "Wife Scare Part 1: https://www.youtube.com/watch?v=Q-xaW7IIa3I Part 2: https://www.youtube.com/watch?v=VROLA7HS8KI")
            return True

        if command == "!pots":
            irc.msg(
                "My wife busting into the room banging pots and pans to scare me: https://www.youtube.com/watch?v=ZDkJJJQbN8Q")
            return True

        if data.find("!%s" % auth.get_streamer_short()) != -1:
            elapsed = alert.notify()
            if elapsed > 0:
                irc.msg("%s was just notified %s seconds ago!" % (auth.get_streamer_short(), elapsed))
            return True

        if command == "!getmode" or command == "!whichmode":
            if mode == 0:
                irc.msg("ITS SCARY TIME!!!")
                return True
            if mode == 1:
                irc.msg("LETS TROLL %s!!!" % auth.get_streamer_short().upper())
                return True
            if mode == 2:
                irc.msg("LIGHTS ARE PRETTY!!!")
                return True

        if scaring == 1 or animating == 1:
            logging.log(logging.INFO, "Busy, adding to stack: scaring: %s animating: %s" % (scaring, animating))
            user_stack.append([user, data])
            del user_stack[10:]
            temp = []
            for stack in user_stack:
                temp.append(stack[1])
            logging.log(logging.INFO, string.join(temp, " - "))
            return
        else:
            logging.log(logging.INFO, "No scare or animation currently, checking for animations")
            # disco rainbow colors
