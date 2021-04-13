import requests
import json
from datetime import datetime
from yattag import Doc

# config section. Personalize here
line = '212'
url_north = 'https://api.metro.net/agencies/lametro/stops/05200/predictions/'
url_south = 'https://api.metro.net/agencies/lametro/stops/13651/predictions/'
list_north = []
list_south = []
html_path = '/var/www/html/'

# Get JSON data
data_north = json.loads(requests.get(url_north).text)
data_south = json.loads(requests.get(url_south).text)
time = str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

# loop through data and append to a list
for item in data_north['items']:
    nprint = item['minutes']
    list_north.append(item['minutes'])

for item in data_south['items']:
    nprint = item['minutes']
    list_south.append(item['minutes'])

# Output prediction to terminal
print('The next northbound bus will arrive in: ', min(list_north))
print('The next southbound bus will arrive in: ', min(list_south))
print('last fetched: '+ time)

# Create contents of html file
doc, tag, text = Doc().tagtext()
doc.asis('<META HTTP-EQUIV="refresh" CONTENT="30">')
with tag('title'):
    text('Metro Line '+ line)
with tag('center'):
    text('The next northbound bus will arrive in: ')
    with tag('h1'):
        text(min(list_north))
    text('The next southbound bus will arrive in: ')
    with tag('h1'):
        text(min(list_south))
    with tag('small'):
        text('last fetched: ',str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))

# create the html file
file = open(html_path+'index.html', 'w')
file.write(doc.getvalue())
file.close()