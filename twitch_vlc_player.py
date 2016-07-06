#! python3

#TODO: fix length, and audio fadeout
#TODO: Look into transition at the end

import vlc  # download https://git.videolan.org/?p=vlc/bindings/python.git;a=blob_plain;f=generated/vlc.py;hb=HEAD
from pytube import YouTube  # pip install pytube
import sys

import tkinter as Tk
from tkinter import ttk

# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform

start = time.clock()


def getYoutubeUrl(input_url):
    if input_url[:32] == "https://www.youtube.com/watch?v=":
        yt = YouTube(input_url)  # additional sanitization needed
        uid = input_url[32:]
    elif input_url[:31] == "http://www.youtube.com/watch?v=":
        yt = YouTube(input_url)  # additional sanitization needed
        uid = input_url[31:]
    else:
        try:
            yt = YouTube("https://www.youtube.com/watch?v=%s" % input_url)
        except Exception as e:
            sys.exit("Error message: %s" % format(e))

    videos = yt.get_videos()
    for video in videos:
        print(video)
    yt.set_filename("intro-%s" % input_url)

    video = yt.get('mp4', '360p')

    return video.url

    # video.download("./")


class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """

    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters


class Player(Tk.Frame):
    """The main window has to deal with events.
    """

    def __init__(self, parent, title=None):
        Tk.Frame.__init__(self, parent)

        self.parent = parent

        if title == None:
            title = "Not ready"
        self.parent.title(title)

        # self.parent.overrideredirect(1)
        w = 640  # width for the Tk root
        h = 360  # height for the Tk root

        # get screen width and height
        ws = self.parent.winfo_screenwidth()  # width of the screen
        hs = self.parent.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.parent.wm_attributes('-topmost', 1)

        # The second panel holds controls
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.parent.bind("<KeyPress>", self.keydown)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        self.timer = ttkTimer(self.OnTimer, 0.1)
        self.timer.start()
        # self.parent.update()

        # self.setVideo("C:\\Users\\spiffomatic64\\Google Drive\\nerd stuff\\twitch\\tests\\intro-9JoeVoyKH8M.mp4")

        # self.setUrlVideo("https://www.youtube.com/watch?v=9JoeVoyKH8M")
        # self.parent.attributes("-alpha", 0.5)

    def initTK(self):
        Tk.Frame.__init__(self, self.parent)

    def keydown(self, e):
        print ("Pressed: %d" % e.keycode)
        if e.keycode == 27:
            _quit()
        if e.keycode == 32:
            self.player.pause()

    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()

    def setVideo(self, fullname):
        # if a file is already running, then stop it.
        self.OnStop()

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        p = pathlib.Path(os.path.expanduser("~"))
        # fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        if os.path.isfile(fullname):
            dirname = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            # Creation
            self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)

            # set the window id where to render VLC's video output
            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                self.player.set_xwindow(self.GetHandle())  # this line messes up windows
            # FIXME: this should be made cross-platform
            self.OnPlay()

    def setVideoUrl(self, url):
        # if a file is already running, then stop it.
        self.OnStop()

        self.Media = self.Instance.media_new(url)
        self.player.set_media(self.Media)
        # set the window id where to render VLC's video output
        if platform.system() == 'Windows':
            self.player.set_hwnd(self.GetHandle())
        else:
            self.player.set_xwindow(self.GetHandle())  # this line messes up windows
            # FIXME: this should be made cross-platform

    def OnPlay(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        print("Playing!")
        if not self.player.get_media():
            self.OnOpen()
        else:
            # Try to launch the media, if this fails display an error message
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    # def OnPause(self, evt):
    def OnPause(self):
        """Pause the player.
        """
        self.player.pause()

    def OnStop(self):
        """Stop the player.
        """
        self.player.stop()
        # reset the time slider
        # self.timeslider.set(0)

    def OnTimer(self):
        if self.player == None:
            return

        # update the time on the slider
        tyme = self.player.get_time()

        if tyme > 5000:
            self.fade_away()
        elif tyme > 100:
            self.SetVolume(75)

    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def SetVolume(self, volume):
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            print("Failed to set volume")

    def errorDialog(self, errormessage):
        print('Error: %s', errormessage)

    # need to add a color/chroma based wipe here
    def fade_away_old(self):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.01
            self.parent.attributes("-alpha", alpha)
            self.SetVolume(int(alpha * 50))
            self.after(100, self.fade_away)
        else:
            _quit()

    def fade_away(self):
        cur_vol = self.player.audio_get_volume()
        print(cur_vol)
        if cur_vol > 0:
            self.player.audio_set_volume(cur_vol - 5)
        else:
            _quit()

    def drawthings(self):
        self.canvas.create_oval(10, 10, 80, 80, outline="gray", fill="gray", width=2)


def Tk_get_root():
    if not hasattr(Tk_get_root, "root"):  # (1)
        Tk_get_root.root = Tk.Tk()  # initialization call is inside the function
    return Tk_get_root.root


def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()  # stops mainloop
    # root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)


def elapsed(message):
    end = time.clock()
    print("%f - %s" % (end - start, message))


if __name__ == "__main__":
    if(len(sys.argv)!=2):
        sys.exit('Usage: %s youtube url' % sys.argv[0])

    elapsed("Getting youtube: %s" % sys.argv[1])
    #ytUrl = getYoutubeUrl("9JoeVoyKH8M")
    #TODO sanitize argv[1]
    print(sys.argv[1])

    ytUrl = getYoutubeUrl(sys.argv[1])

    # Create a Tk.App(), which handles the windowing system event loop
    elapsed("Creating TK")
    root = Tk_get_root()
    root.protocol("WM_DELETE_WINDOW", _quit)

    elapsed("Creating player (this is what shows the box)")
    player = Player(root, title="tkinter vlc")

    elapsed("Setting URL")
    player.setVideoUrl(ytUrl)
    elapsed("Starting to play")

    player.OnPlay()

    while not player.player.is_playing():
        time.sleep(0.001)
        # print(player.player.get_state())
    # player.player.pause()
    elapsed("VLC says its playing")
    time.sleep(0.1)
    # player.drawthings()

    # player.player.play()
    # show the player window centred and run the application
    root.mainloop()