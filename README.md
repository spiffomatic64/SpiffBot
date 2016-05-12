SpiffBot 
========

Interactive Twitch IRC bot

This is my IRC bot I threw together hastily night by night to add some fun interactivity to twitch. 

I'm using an arduino currently to drive some leds/servo's/vibration motors, but I plan on expanding this.

The code is VERY ugly, VERY buggy, and is changed just about daily... Its literally cobbled together every night about 30 minutes before I stream to add a few features/fix a few bugs here and there. (I avoid large re-writes because it would mean downtime for the stream) which makes it even uglier lol...

<h1>Setup</h1>
Software Requirements:
<ol>
    <li>Python 2.7.* x86 (latest) https://www.python.org/downloads/</li>
    <li>Mysql http://www.easyphp.org/</li>
    <ol>
        <li>Add sql setup here</li>
    </ol>
    <li>pyserial (pip install pyserial)</li>
    <li>pygame http://www.pygame.org/download.shtml</li>
    <li>requests (pip install requests)</li>
    <li>win32api https://sourceforge.net/projects/pywin32/files/</li>
    <li>mysql https://dev.mysql.com/downloads/connector/python/</li>
    <li>comtypes (pip install comtypes)</li>
    <li>pil (http://www.pythonware.com/products/pil/)</li>
</ol>
Configuration:
<ol>
    <li>Update twitch_auth.py</li>
    <ol>
        <li>get_oauth: https://twitchapps.com/tmi/</li>
        <li>get_bot: Twitch bot username</li>
        <li>get_db_user: username configured in mysql db</li>
        <li>get_db_pass: password configured for mysql db user</li>
    </ol>
</ol>


<h1>Scare features</h1>
<ol>
    <li>Open cdrom</li>
    <li>Vibrate control (if using one)</li>
    <li>Drop a box</li>
    <li>Grab fabric of pants with servo strapped to leg</li>
    <li>Tap shoulder</li>
    <li>Vibrate chest</li>
    <li>Rattle vibration motor on desk</li>
    <li>Touch neck/back with servo</li>
    <li>Pop up scary gif</li>
    <li>write scare status to txt for OBS display</li>

    <h1>Troll features (also available during scary games)</h1>
    <ol>
        <li>Playing sounds (in center/left/right ears)</li>
        <li>Turning off all monitors</li>
        <li>Turning off all volume</li>
        <li>Move game window around monitors randomly</li>
        <li>Strobe game sccreen</li>
        <li>Dim game screen</li>
        <li>Draw a randomly sized black box in the middle of the screen</li>
        <li>Turning off all monitors</li>
        <li>Randomly press keyboard buttons</li>
        <li>Randomly move mouse around</li>
        <li>Randomly disable all keyboard and mouse input</li>
        <li>Minimize all windows</li>
        <li>Turning off all monitors</li>
    </ol>
</ol>

<h1>LED/light features</h1>
<ol>
    <li>Midi Drum input to light output</li>
    <li>alternate(color,color)</li>
    <li>chase(color|*)</li>
    <li>fire(color|color) animation</li>
    <li>disco fire</li>
    <li>disco animation</li>
    <li>disco strobe</li>
    <li>strobe animation</li>
    <li>accept html ffffff #ffffff 0xffffff ff,ff,ff 255,255,255 in all animations for colors </li>
    <li>after light command, fade to white during normal, and go to black during scary</li>
    <li>color commands only run for a set amount of time</li>
    <li>prevent light animations from occuring while scares are going on</li>
</ol>


<h1>Additional features:</h1>
<ol>
    <li>"command mode" to select a viewer at random, and let them use priviledged commands</li>
    <li>!optin, and !optout commands to allow users to opt in and out of "command mode"</li>
    <li>database persistence</li>
    <li>!pass command to allow users to pass to someone else, or a specific user</li>
    <li>timer thread to automatically give up control from afk users</li>
    <li>switching mode from scary to normal</li>
    <li>switch if user in control opts out</li>
    <li>get viewers as well as moderators</li>
    <li>allow streamer to use any command without causing a switch</li>
    <li>!game command lets viewers know what game is being played</li>
    <li>admin commands allowing manual switch's, and switch next (to not steal the current persons turn)</li>
    <li>!whosgotit command to let viewers know who currently has control</li>
    <li>!timeleft command to let viewers know how much time is left</li>
    <li>!opted command to let viewers know if they are opted in or not</li>
</ol>


