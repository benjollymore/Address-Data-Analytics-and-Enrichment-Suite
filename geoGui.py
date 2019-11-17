#get geocoding data from address passed via command line
#has to do some funky stuff instead of just parsing webpage
#as an xml file because google puts api response data in
#a pre tag, which does not play nice with python... :(
#uses googles geocoding api
#once gets lat/long info from parsed address, 
#grabs 400x400px sattelite image from this location.
#then passes this image through a convolutional 
#neural network to classify terrain type as
#city/industrial/suburban/rural
#todo: classify building type from streetview capture
#images using another CNN to process
#ben jollymore 2019

import json
import urllib
import requests
import sys
import cv2
import tensorflow as t
from PIL import Image
from tkinter import *

window = Tk()
window.title("Window")
lbl = Label(window, text="Thing to make data stuff from address stuff")
lbl.grid(column=0, row=0)
window.geometry('640x480')

btn = Button(window, text="Query")
btn.grid(column=1, row=1)

entry = Entry(window,width=60)
entry.grid(column=0, row=1)

def clicked():
	address = entry.get()

window.mainloop()


url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
key = '&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'

address = sys.argv[1]
addressSendable = address.replace(" ", "+")

query = url + addressSendable + key
page = requests.get(query)
geoData = page.json()

lattitude = geoData['results'][0]['geometry']['location']['lat']
longitude = geoData['results'][0]['geometry']['location']['lng']
addressInfo = []

for i in geoData['results'][0]['address_components']:
	if (i['types'][0] != "route" and i['types'][0] != "street_number"):
		if i['long_name'] not in addressInfo:
			addressInfo.append(i['long_name'])

print("Lattitude: ", lattitude)
print("Longitude: ", longitude)
for i in addressInfo:
	print(i)

url = 'https://maps.googleapis.com/maps/api/staticmap?center='
key = '&zoom=15&size=400x400&maptype=satellite&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'
query = url + str(lattitude) + ',' + str(longitude) + key

urllib.request.urlretrieve(query, "satellite.png")
img = Image.open("satellite.png")
img.show()

CATEGORIES = ["city", "industrial", "rural", "suburban"]

model = tf.keras.models.load_model("CNN.model")

img_array = cv2.imread("satellite.png", cv2.IMREAD_COLOR)
new_array = cv2.resize(img_array, (400, 400))
new_array = new_array.reshape(-1, 400, 400, 3)

prediction = model.predict(new_array)
prediction = list(prediction[0])
print(CATEGORIES[prediction.index(max(prediction))])

#next up -- do same thing but grab street view image
#build a building type classifier
#house apt warehouse empty lot etc

url2 = 'https://maps.googleapis.com/maps/api/streetview?size=400x400&location='
key2 = '&pitch=10&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'
query2 = url2 + str(lattitude) + ',' + str(longitude) + key2

urllib.request.urlretrieve(query2, "streetview.png")

img2 = Image.open("streetview.png")
img2.show()

CATEGORIES2 = ["apartment", "commercial", "house", "office", "vacant"]

model2 = tf.keras.models.load_model("CNNStreet.model")

img_array2 = cv2.imread("streetview.png", cv2.IMREAD_COLOR)
new_array2 = cv2.resize(img_array2, (400, 400))
new_array2 = new_array2.reshape(-1, 400, 400, 3)

prediction2 = model.predict(new_array2)
prediction2 = list(prediction2[0])
print(CATEGORIES2[prediction2.index(max(prediction2))])
