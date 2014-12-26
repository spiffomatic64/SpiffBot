import urllib2
import sys

def getsystems():
    system_year=2007
    system_sold=10

    response = urllib2.urlopen('http://en.wikipedia.org/wiki/List_of_million-selling_game_consoles')
    html = response.read()

    tables = html.split("wikitable sortable")
    systems =  tables[1].split("<tr>")
    systems.pop(0)
    systems.pop(0)

    playable=[]
    for system in systems:
        parts = system.split("</td>")
        
        if "data-sort-value" in parts[3]:
            sold = parts[3][parts[3].find("data-sort-value=\"")+17:parts[3].rfind("\">")]
            sold = sold[sold.find("\">")+1:]
        else:
            sold = parts[3][parts[3].find("\">")+1:parts[3].rfind("&#160;")]
            sold = sold[sold.find("\">")+2:]
            if "\xe2\x80\x93" in sold:
                sold = sold[:sold.find("\xe2\x80\x93")]
        
        if float(sold)>system_sold:
            released = parts[2][parts[2].find("title"):parts[2].rfind("</a>")]
            released = released[released.find("\">")+2:]
            if int(released)<system_year:
                
                name = parts[0][parts[0].find("title"):parts[0].find("</a>")]
                name = name[name.find("\">")+2:]
                print("%s\t%s\t%s" % (name, released, sold))
                

    
systems = getsystems()

   




    