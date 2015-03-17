import urllib2

urls = ["http://www.gamesradar.com/best-ps2-games-all-time/",
        "http://www.gamesradar.com/best-ds-games/",
        "http://www.gamesradar.com/best-game-boy-games-all-time/",
        "http://www.gamesradar.com/best-psx-games/",
        "http://www.gamesradar.com/best-wii-games-all-time/",
        "http://www.gamesradar.com/best-xbox-360-games/",
        "http://www.gamesradar.com/best-gba-games/",
        "http://www.gamesradar.com/best-ps3-games/",
        "http://www.gamesradar.com/best-psp-games/",
        "http://www.gamesradar.com/best-nes-games-all-time/",
        "http://www.gamesradar.com/best-snes-games-all-time/",
        "http://www.gamesradar.com/best-sega-genesis-games-all-time/",
        "http://www.gamesradar.com/best-n64-games-all-time/",
        "http://www.gamesradar.com/best-atari-2600-games-all-time/",
        "http://www.gamesradar.com/best-xbox-games-all-time/",
        "http://www.gamesradar.com/best-gamecube-games/",
        "http://www.gamesradar.com/best-master-system-games/",
        "http://www.gamesradar.com/best-game-gear-games-all-time/",
        "http://www.gamesradar.com/best-dreamcast-games-all-time/",
        "http://www.gamesradar.com/best-ps2-games-all-time/",
        "http://www.gamesradar.com/best-pc-games/"]

def getgames(url):
    response = urllib2.urlopen(url)
    html = response.read()
    
    print "----------------------------------------"
    print html[html.find("Best")+5:html.find(" ",html.find("Best")+5)]
    print "----------------------------------------"
    
    chunks = html.split("<div class=\"gallery_title\">")
    chunks.pop(0)
    chunks.pop(0)
    chunks.pop()
    
    for chunk in chunks:
        game = chunk[chunk.find(" ")+1:chunk.find("</div>")]
        print game
    print
    
for url in urls:
    getgames(url)




    