import json, requests, pprint
url = 'https://api.twitch.tv/kraken/streams?'

params = dict( offset='0', limit='100' )

stop = False
total = 0

while stop == False:
    data = requests.get(url=url, params=params)
    binary = data.content
    output = json.loads(binary)

    if 'streams' not in output:
        stop = True
    else:
        for stream in output['streams']:
            if stream['viewers']==0:
                stop = True
            total = total+stream['viewers']
            print "%s:%s" % (stream['channel']['display_name'], stream['viewers'])
    params['offset']=int(params['offset'])+100;

print total