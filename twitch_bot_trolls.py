#! python2

# Not used, for debugging to list all monitors
def printAllScreen():
    i = 0
    while True:
        try:
            device = win32.EnumDisplayDevices(None, i)
            print("[%d] %s (%s)" % (i, device.DeviceString, device.DeviceName))
            i += 1
        except:
            break
    return i


# Flip the monitor using winapi's
def flip(duration=20, scare=0):
    scare_lock(1)
    scare_status("Monitor is flipped!")
    # manually selecting monitor 2 (Windows reports monitor 2, is actually 1)
    device = win32.EnumDisplayDevices(None, 0)
    logging.log(logging.DEBUG, "Rotate device %s (%s)" % (device.DeviceString, device.DeviceName))

    dm = win32.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
    dm.DisplayOrientation = win32con.DMDO_180  # flip 180 degrees
    dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
    dm.Fields = dm.Fields & win32con.DM_DISPLAYORIENTATION
    win32.ChangeDisplaySettingsEx(device.DeviceName, dm)
    time.sleep(duration)
    dm.DisplayOrientation = win32con.DMDO_DEFAULT  # flip back to normal
    dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
    dm.Fields = dm.Fields & win32con.DM_DISPLAYORIENTATION
    win32.ChangeDisplaySettingsEx(device.DeviceName, dm)
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()
    return


# Flip the monitor using winapi's
def wiggle(times=20, scare=0):
    global counter
    scare_lock(1)
    scare_status("Wiggling window!")
    # manually selecting monitor 2 (Windows reports monitor 2, is actually 1)
    while True:
        time.sleep(0.001)
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                logging.log(logging.INFO, "Found window! hwnd: %s" % hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                x = rect[0]
                y = rect[1]
                w = rect[2] - x
                h = rect[3] - y
                logging.log(logging.INFO, "x: %d y: %d w: %d h: %d" % (x, y, w, h))
                break
            else:
                logging.log(logging.ERROR, "No windows %s" % hwnd)
        except win32gui.error:
            logging.log(logging.ERROR, "Error: window not found")
    try:
        for i in range(0, times):
            win32gui.SetWindowPos(hwnd, None, random.randint(-2312, 2712 - w), random.randint(0, 1024 - h), 0, 0, 1)
            time.sleep(1)
        win32gui.SetWindowPos(hwnd, None, x, y, w, h, 1)
    except:
        irc.msg("Wiggle failed! Returning control to %s" % master)
        scare_status(-1)
        scare_lock(0)
        counter = time.time()
        return
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()
    return


# Slow strobe the monitor effect
def flicker(scare=0):
    scare_lock(1)
    scare_status("Flickering Monitor!")
    p = subprocess.Popen(["python", "twitch_bot_flicker.py"])
    p.wait()
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()


def dark(scare=0):
    scare_lock(1)
    scare_status("Dimming Monitor!")
    p = subprocess.Popen(["python", "twitch_bot_dim.py"])
    p.wait()
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()


def box(scare=0):
    scare_lock(1)
    scare_status("Drawing Blind Spot!")
    p = subprocess.Popen(["python", "twitch_bot_box.py"])
    p.wait()
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()


def drunk(scare=0):
    scare_lock(1)
    scare_status("DRUNK MOUSE!")
    p = subprocess.Popen(["python", "twitch_bot_drunk.py"])
    p.wait()
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()


def gif(wait, scare=0):
    scare_lock(1)
    scare_status("GIF SCARE!")
    status_length = 3
    p = subprocess.Popen(["python", "twitch_bot_gif.py"])
    p.wait()
    time.sleep(status_length)
    scare_status(-1)
    time.sleep(wait - status_length)
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()


def noput(scare=0):
    logging.log(logging.INFO, "NOPUT!!!")
    scare_lock(1)
    times = random.randint(30, 60)
    stop = time.time() + times
    while time.time() < stop:
        ctypes.windll.user32.BlockInput(1)
        scare_status("REDLIGHT!")
        time.sleep(random.randint(1, 10) / 10.0)
        ctypes.windll.user32.BlockInput(0)
        scare_status("GREENLIGHT!")
        time.sleep(random.randint(1, 8) / 5.0)
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()
    return

def turn_off_monitors(msg, wait, scare=0):
    scare_status("Monitors disabled!")
    scare_lock(1)
    status_length = 3
    call(["nircmd.exe", "monitor", "off"])
    time.sleep(2.5 + status_length)
    scare_status(-1)
    time.sleep(wait - status_length)
    scare_lock(0)
    if scare == 0:
        switch()


def change_volume(wait, level, scare=0):
    scare_lock(1)
    scare_status("Changing volume!")
    logging.log(logging.INFO, "Changing volume: %d" % level)
    vol_scare.set_volume(level)
    time.sleep(wait)
    vol_scare.set_volume(-20.0)
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()
    return

def vibrate(wait, left, right, scare=0):
    scare_lock(1)
    scare_status("Vibrating controller!")
    logging.log(logging.INFO, "Vibrating controller: %d:%d" % (left, right))
    stop = time.time() + wait
    while time.time() < stop:
        time.sleep(0.5)
        set_vibration(0, left, right)
    set_vibration(0, 0, 0)
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()
    return


def wasd(scare=0):
    scare_lock(1)

    times = random.randint(30, 60)
    keys = [["W", 0x11, 0x57], ["A", 0x1e, 0x41], ["S", 0x1f, 0x53], ["D", 0x20, 0x44]]

    stop = time.time() + times
    while time.time() < stop:
        key = random.choice(keys)
        twitch_bot_input.PressKey(key[1], key[2], True)
        scare_status("Pressing [%s]" % key[0])
        time.sleep(random.randint(1, 10) / 10.0)
        twitch_bot_input.PressKey(key[1], key[2], False)
        scare_status("Pressing")
        time.sleep(random.randint(1, 8) / 5.0)
    scare_status(-1)
    scare_lock(0)
    if scare == 0:
        switch()
    return


def minimize(wait, scare):
    win = 0x5B
    d = 0x44
    scare_lock(1)
    scare_status("Minimize!!!")
    status_length = 3
    twitch_bot_input.PressKey(0, win, True)
    twitch_bot_input.PressKey(0, d, True)
    time.sleep(0.5)
    twitch_bot_input.PressKey(0, d, False)
    twitch_bot_input.PressKey(0, win, False)
    time.sleep(status_length)
    scare_status(-1)
    time.sleep(wait - status_length)
    scare_lock(0)
    if scare == 0:
        switch()

