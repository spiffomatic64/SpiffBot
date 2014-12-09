SpiffBot
========

Interactive Twitch IRC bot

This is my IRC bot I threw together hastily night by night to add some fun interactivity to twitch.

I'm using an arduino currently to drive some leds/servo's/vibration motors, but I plan on expanding this.

The code is VERY ugly, VERY buggy, and is changed just about daily... Its literally cobbled together every night about 30 minutes before I stream to add a few features/fix a few bugs here and there. (I avoid large re-writes because it would mean downtime for the stream) which makes it even uglier lol...

<h1>Current list of added features:</h1>
<ol>
<li>Midi Drum input</li>
<li>alternate(color,color)</li>
<li>chase(color)</li>
<li>chase(color,color,color) in series</li>
<li>fire animation</li>
<li>disco animation</li>
<li>strobe animation</li>
<li>disco strobe</li>
<li>Started threading the bot</li>
<li>"command mode" to select a viewer at random, and let them use priviledged commands</li>
<li>!optin, and !optout commands to allow users to opt in and out of "command mode"</li>
<li>!pass command to allow users to pass to someone else, or a specific user</li>
<li>sound scares</li>
<li>servo/drop scare</li>
<li>vibration motor scares</li>
<li>timer thread to automatically give up control from afk users</li>
<li>using html color codes</li>
<li>switching mode from scary to normal</li>
<li>after light command, fade to white during normal, and go to black during scary</li>
<li>color commands only run for a set amount of time</li>
<li>letting viewers flip main monitor upside down</li>
</ol>
