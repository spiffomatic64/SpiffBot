SpiffBot
========

Interactive Twitch IRC bot

This is my IRC bot I threw together hastily night by night to add some fun interactivity to twitch.

I'm using an arduino currently to drive some leds/servo's/vibration motors, but I plan on expanding this.

The code is VERY ugly, VERY buggy, and is changed just about daily... Its literally cobbled together every night about 30 minutes before I stream to add a few features/fix a few bugs here and there. (I avoid large re-writes because it would mean downtime for the stream) which makes it even uglier lol...

Current list of added features:
  Midi Drum input
  alternate(color,color)
  chase(color)
  chase(color,color,color) in series
  fire animation
  disco animation
  strobe animation
  disco strobe
  Started threading the bot
  "command mode" to select a viewer at random, and let them use priviledged commands
  !optin, and !optout commands to allow users to opt in and out of "command mode"
  !pass command to allow users to pass to someone else, or a specific user
  sound scares
  servo/drop scare
  vibration motor scares
  timer thread to automatically give up control from afk users
  using html color codes
  switching mode from scary to normal
  after light command, fade to white during normal, and go to black during scary
  color commands only run for a set amount of time
  letting viewers flip main monitor upside down

bugs fixed:
  prevent users from passing to themselves
  prevent user from being pitcked twice
  prevent skipping users (thread problems could switch twice in a row quickly)
  servo buzzing during light commands
  
known current bugs:
  servo randomly going nuts
  motors not turning off
  commands queue (in control commands should also trump normal commands)
  
future features:
  ################################
  #Normal Ideas
  ################################
    keep track of data via sql
    poll functionality built into bot, or lauch straw poll
    move full led control to pyton, up serial baud rate
    throttle normal users light use (in scary mode)
    keep track of "current" color (so we can fade from/back to)
    dont overwrite colors with drum lights (fading)
    implement bass something (leds?)
    secret commands/easter eggs
    n64 mario party multiplayer kailera server(select viewers to play, take turns)
    cycle multiple colors cycle(red,white,blue) (fade too)
    take picture, convert to leds
    game color get pixels from emulator 
    skeleton text to speech (python) servo, jaw (mix audio to be slightly to the right)
    puppy cam/feeder
    random single color
    fire(random)
  ################################
  #Scary Ideas
  ################################
    shake webcam command-viewer scare
    scare idea: throw something at me
    net drop
    reduce volume over time, then crank for sound scare
    door open quickly-rubber banded
    add relays to monitors 
    on relays, control fan
    let viewers mess with my controls
    mess with monitors dimness
    random scare command
    shock
    string to brush
    vibrator motor to chair
    
  ################################
  #interactive scares for viewers
  ################################
  ability to scare viewers (making skeleton move, overlay ghost, loud jump scare)
  ability for viewers to opt out of being scared (via ajax web interface on p[ersonal server)
  ability to stream viewers webcam/mic to me, to twitch, if users is scared (motion/audio)
  link to special twitch viewer (html overlays)
  people in command, can also perform viewer scares (individual, all)
  flash app, to capture scares, and incorperate into my stream
  show peoples reactions using special viewer/flash
  show people all the time based on points/etc
  
  ################################
  #Points System
  ################################
  default: 1
  follower for longer than 1 week: 1
  if you refer someone: 1
  if you watch longer than 45 mins: 1
  points/referrals carry over
