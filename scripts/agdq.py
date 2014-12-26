import urllib2
import BeautifulSoup
import pprint
import json
import requests
import operator

def getTwitch(streamer):
    url = "https://api.twitch.tv/kraken/search/channels?q=%s&limit=5" % streamer
    data = requests.get(url=url)
    binary = data.content
    output = json.loads(binary)
    channels = {}
    try:
        for twitch in output['channels']:
            channels[twitch['name']] = twitch['followers']
        channel = max(channels.iteritems(), key=operator.itemgetter(1))[0]
    except:
        return -1
    return [ channel, channels[channel] ] 
            
def getAgdq():            
    url = "https://gamesdonequick.com/submission/all"
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    data = urllib2.urlopen(req).read()
    soup = BeautifulSoup.BeautifulSoup(data)

    groupedData = []

    for row in soup.findAll("tr", { "class" : ["success", "info", "halfcoordinated"] }):
        data = {}
        allTDs = row.findAll("td")
        for x in range(0, len(allTDs)-1, 2):
            data[allTDs[x].renderContents().strip()] = allTDs[x+1].renderContents().strip()
        groupedData.append(data)

    #pprint.pprint(groupedData)

    streamers = []

    for item in groupedData:
        for name, video in item.iteritems():
            if video[:8] == "<a href=":
                streamers.append(name)
                
    temp = set(streamers)
    streamers = sorted(list(temp))
    return streamers
    
streamers = getAgdq()

for streamer in streamers:
    temp = getTwitch(streamer)
    if temp!=-1:
        print ("%s\t%s" % (temp[0],temp[1]))
    

    
    