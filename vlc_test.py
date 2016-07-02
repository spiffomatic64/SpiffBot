#! python3

import math,sys
import os.path
import vlc
from PyQt4 import QtGui, QtCore
from pytube import YouTube #pip install pytube
import time

start = time.clock()


def getYoutubeUrl(input_url):
    if input_url[:32] == "https://www.youtube.com/watch?v=":
        yt = YouTube(input_url)  # additional sanitization needed
        uid = input_url[32:]
    elif input_url[:31] == "http://www.youtube.com/watch?v=":
        yt = YouTube(input_url)  # additional sanitization needed
        uid = input_url[31:]
    else:
        yt = YouTube("https://www.youtube.com/watch?v=%s" % input_url)

    yt.set_filename("intro-%s" % input_url)

    video = yt.get('mp4', '360p')

    return video.url

    # video.download("./")


class Overlay(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(0, 0, 0, 127)))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        for i in range(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(127 + (self.counter % 5) * 32, 127, 127)))
            else:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width() / 2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.height() / 2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                20, 20)

        painter.end()

    def showEvent(self, event):

        self.timer = self.startTimer(50)
        self.counter = 0

    def timerEvent(self, event):

        self.counter += 1
        self.update()
        if self.counter == 60:
            self.killTimer(self.timer)
            self.hide()

class Player(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False

    def createUI(self):
        """Set up the user interface, signals & slots
        """

        widget = QtGui.QWidget(self)

        self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window,
                              QtGui.QColor(0, 0, 0))
        self.palette.setColor(QtGui.QPalette.Background,
                              QtGui.QColor(255, 0, 255))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        layout = QtGui.QVBoxLayout(widget)
        layout.addWidget(self.videoframe)
        self.setCentralWidget(widget)
        self.overlay = Overlay(self.videoframe)
        self.overlay.show()
        #widget.setLayout(layout)


        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)
        print("12")

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return

            self.mediaplayer.play()
            #self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        #self.playbutton.setText("Play")

    

    def setVideoUrl(self, url):
        # if a file is already running, then stop it.
        self.Stop()

        self.media = self.instance.media_new(url)
        self.mediaplayer.set_media(self.media)
        # set the window id where to render VLC's video output
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())


    def setVolume(self, Volume):
        self.mediaplayer.audio_set_volume(Volume)


    def fade_away(self):
        volume = self.mediaplayer.audio_get_volume()
        if volume > 0:
            volume -= 1

            self.setVolume(volume)
            print(volume)

        else:
            sys.exit(app.exec_())

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        #self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        tyme = self.mediaplayer.get_time()
        
        if tyme > 10000:
            self.fade_away()
        else:
            if(self.mediaplayer.is_playing()==True):
                self.mediaplayer.audio_set_volume(40)

def elapsed(message):
    end = time.clock()
    print("%f - %s" % (end - start, message))

if __name__ == "__main__":

    print(sys.argv[1])
    elapsed("Getting youtube")
    ytUrl = getYoutubeUrl(sys.argv[1])

    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)

    elapsed("Setting URL")
    player.setVideoUrl(ytUrl)
    time.sleep(7)
    elapsed("Playing")
    player.PlayPause()

    sys.exit(app.exec_())