#get 400x400 sattelite image from a coordinate pair
#uses googles static map api
#ben jollymore 2019

import urllib.request
import sys
from PIL import Image

lattitude = sys.argv[1]
longitude = sys.argv[2]
name = sys.argv[3]

url = 'https://maps.googleapis.com/maps/api/staticmap?center='
key = '&zoom=15&size=400x400&maptype=satellite&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'
query = url + lattitude + ',' + longitude + key

urllib.request.urlretrieve(query, name)

#img = Image.open(name)
#img.show()
