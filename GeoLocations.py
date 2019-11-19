#get geocoding data from address passed via command line
#has to do some funky stuff instead of just parsing webpage
#as an xml file because google puts api response data in
#a pre tag, which does not play nice with python... :(
#uses googles geocoding api
#ben jollymore and daniel doucett 2019

import json
import urllib
import requests
import sys
import time
import argparse
import cv2
import tensorflow as tf
from PIL import Image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

types = ["accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station", "cafe", "campground", "car_dealer","car_rental","car_repair","car_wash","casino","cemetery","church","city_hall","clothing_store","convenience_store","courthouse","dentist","department_store","doctor","electrician","electronics_store","embassy","fire_station","florist","funeral_home","furniture_store","gas_station","gym","hair_care","hardware_store","hindu_temple","home_goods_store","hospital","insurance_agency","jewelry_store","laundry","lawyer","library","liquor_store","local_government_off", "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office", "real_estate_agency", "restaurant", "roofing_contractor", "rv_park", "school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "supermarket", "synagogue", "taxi_stand", "train_station", "transit_station", "travel_agency", "veterinary_care", "zoo" ]

outputJSON = "{"
output = ""

isInteresting = False
isFlagged = False
isPostOffice = False
isEmbassy = False

parser = argparse.ArgumentParser(
	description="Using an address in natural language find out more detailed"
	" info including nearby businesses")
parser.add_argument('stringname', metavar='address', type=str, nargs='+',
	help="Address for the building")
parser.add_argument('--pld', dest='printLocalData', help="Find the building type",
	action="store_true")
parser.add_argument('--ld', dest='localData', 
	help="Uses places data to find"
		 " what business are close to the location.",
	action="store_true")
parser.add_argument("--pad", dest='printAddressData',
	help="Print only the building info for building with the same "
		 "address as the input. Overrides --pld",
	action="store_true")
parser.add_argument('--wp', dest='whitePages',
	help="Get the data from the white pages server",
	action="store_true")
parser.add_argument('--debug', dest='debug', 
	help="Set JSON from whitepages to use static file for testing (depreciated)",
	action="store_true")
parser.add_argument('--sat', dest='sattelite', 
	help="Retrieve sattelite imagery and send through classification model",
	action="store_true")
parser.add_argument('--st', dest='street', 
	help="Retrieve street level imagery and send through classification model",
	action="store_true")
parser.add_argument('--v', dest='verbose', 
	help="Print verbose output to console",
	action="store_true")
parser.add_argument('--vj', dest='verboseJSON', 
	help="Print json output to console",
	action="store_true")
parser.add_argument('--dj', dest='debugJSON', 
	help="Debug JSON structure",
	action="store_true")


args=parser.parse_args()

def appendJSON(strIn, attrib):
	global outputJSON
	outputJSON += '"'+ strIn + '":"' + str(attrib) + '", '

def terminateJSON():
	global output, outputJSON
	outputJSON = outputJSON[:-2]
	outputJSON += "}"
	if args.debugJSON:
		print(outputJSON)
	else:
		output = json.loads(outputJSON)


#Variables for APIs
url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
urlPlaces = 'https://maps.googleapis.com/maps/api/place/details/json?'
urlWhitePages = "https://api.ekata.com/3.0/location?api_key=cffb32044ba94e209665f793595abe37"
key = '&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'
APIkey = 'AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'

#https://python.gotrained.com/google-places-api-extracting-location-data-reviews/
def search_places_by_coordinate(location, radius):
	endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
	
	places = [] 	#Premake the return array

	#Define the search parameters
	params = {
		'location': location,
		'radius': radius,
		'types': ",".join(types),
		'key': APIkey
	}

	res = requests.get(endpoint_url, params = params)
	results =  json.loads(res.content)
	places.extend(results['results'])
	time.sleep(2)
   
	while "next_page_token" in results:
		params['pagetoken'] = results['next_page_token'],
		res = requests.get(endpoint_url, params = params)
		results = json.loads(res.content)
		places.extend(results['results'])
		time.sleep(2)
	
	return places

#Method to get the data for the location
def get_street_info():
	address = args.stringname[0]
	if args.verbose:
		print("Input: ", address)
		print()
	addressSendable = address.replace(" ", "+")

	query = url + addressSendable + key
	page = requests.get(query)
	geoData = page.json()

	lattitude = geoData['results'][0]['geometry']['location']['lat']
	longitude = geoData['results'][0]['geometry']['location']['lng']
	addressInfo = geoData['results'][0]['address_components']

	if args.verbose:	
		print("Lattitude: ", lattitude)
		print("Longitude: ", longitude)

	appendJSON("lattitude", str(lattitude))
	appendJSON("longitude", str(longitude))

	try:
		place_id = geoData["results"][0]['place_id']
	except KeyError:
		if args.verbose:
			print("Failed")
		place_id = ""

	return {"lat": lattitude, "long": longitude, 
		'id': place_id, 'addressInfo': addressInfo}

#Get the data
def get_nearby_data(info):
	return search_places_by_coordinate(
		",".join([str(addressData['lat']), str(addressData['long'])]), "50")

def print_place_data(data):
	global outputJSON
	count = 0
	
	if len(data) is not 0:
		if args.verbose:
			print("\nNearby business locations:\n")

		outputJSON += '"businesses":[ '
		for x in data:
			outputJSON += "{ "
			count += 1
			try:
				if args.verbose:
					print("%2d: Name     | %s, \n"
						   "    Address  | %s, \n"
						   "    Type     | %s  \n"
						   %(count, x['name'], x['vicinity'], x['types']))
				appendJSON("name", x['name'])
				appendJSON("vicinity", x['vicinity'])
				appendJSON("types", x['types'])

			except KeyError:
				if args.verbose:
					print("%2d: Name     | %s, \n" 
						  "     Address  | No address found, \n"
						  "     Type     | %s  \n"% (count, x['name'],x['types']))
				appendJSON("name", x['name'])
				appendJSON("vicinity", "No address found")
				appendJSON("types", x['types'])
			outputJSON = outputJSON[:-2]
			outputJSON += "}, "

		if args.verbose:	
			print()
		outputJSON = outputJSON[:-2]
		outputJSON += "], "
def switch(argument):
    switcher = {
        "street_number": "number",
        "route": "street",
        "neighborhood": "neighborhood",
        "locality": "locality",
        "administrative_area_level_3": "city",
        "administrative_area_level_2": "muncipality",
        "administrative_area_level_1": "province",
        "country": "country",
        "postal_code": "postal_code",
    }
    return switcher.get(argument, "Invalid entry")

def print_location_data(data, short):
	global outputJSON
	if args.verbose:
		print("\nAddress data for this address is:\n")
	outputJSON += '"address":{ '
	for i in data['addressInfo']:
		#outputJSON += "{ "
		infoStr = switch(i['types'][0])
		if args.verbose:
			print(" %s"%( i['short_name'] if short else i['long_name']))
		if short:
			appendJSON(infoStr, i['short_name'])
		else:
			appendJSON(infoStr, i['long_name'])
		#outputJSON = outputJSON[:-2]
		#outputJSON += "}, "
	outputJSON = outputJSON[:-2]
	outputJSON += "}, "

def get_compare_address(data):
	x = [i['long_name'] for i in data if i['types'][0] == "street_number" or i['types'][0] == "route" or i['types'][0] == "locality"]
	retVal = x[0] + " " + x[1] + ', ' + x[2]
	return retVal

def get_businesses_with_same_address(aData, pData):
	retVal = []
	for i in pData:
		try:
			if i['vicinity'] == aData:
				retVal.append(i)
		except KeyError:
			pass
	return retVal

def check_for_flaggable(data):
	global isFlagged, isPostOffice, isEmbassy
	flaggable = [
		'post_office', 'car_dealer', 'cemetery', 
		'courthouse', 'embassy', 'park', 'storage']

	for i in data:
		for x in i['types']:
			if x in flaggable:
				isFlagged = True
				if x == 'post_office':
					isPostOffice = True
				if x == 'embassy':
					isEmbassy = True

def print_address_data(aData, pData):
	global isInteresting
	data = get_businesses_with_same_address(aData, pData)
	if len(data) > 0: 
		isInteresting = True
		check_for_flaggable(data)

	print_place_data(data)

def format_whitepages_input(data):
	retVal = {}
	x = [i['long_name'] for i in addressData['addressInfo'] if i['types'][0] == 'locality']
	for z in data:
		if 'street_number' in z['types']:
			streetStr= z['short_name']
		elif 'route' in z['types']:
			streetStr+= "+" + z['short_name'].replace(" ", "+")
		elif 'locality' in z['types']:
			cityStr= z['long_name'].replace(" ", "+")
		elif 'country' in z['types']:
			countryStr = z['short_name']
		elif 'postal_code' in z['types']:
			postalStr = z['long_name'].replace(" ", "")
		elif 'administrative_area_level_1' in z['types']:
			provStr = z['short_name']

	retVal['city'] = cityStr
	retVal['country'] = countryStr
	retVal['code'] = postalStr
	retVal['prov'] = provStr
	retVal['street']= streetStr
	retVal['unit']= ""
	return retVal


def get_whitepages_data(data):
	params = {
		'city': data['city'],
		'country_code': data['country'],
		'postal_code': data["code"],
		'state_code': data["prov"],
		'street_line_1': data['street'],
		'street_line_2': data['unit']}
	page = requests.get(urlWhitePages, params=params)
	return page.json()


##placeholder data fill in from the other json##
cityTest = {
	'city': "Halifax",
	'country': "CA",
	'postal': "B3L+3G9",
	'prov': "NS",
	'street': "2529 Sherwood St",
	'unit': ""
}

def print_whitepages_data(pageData):
	global outputJSON
	if args.verbose:
		print("\nMailing Status:")
		print("\nActive: ",pageData['is_active'])
		print("Commericial: ",pageData['is_commercial'])
		print("Forwarding Mail: ",pageData['is_forwarder'])
		print("Delivery Type: ",pageData['delivery_point'])

	appendJSON("active", str(pageData['is_active']))
	appendJSON("commercialMail", str(pageData['is_commercial']))
	appendJSON("forwardsMail", str(pageData['is_forwarder']))
	appendJSON("deliveryType", str(pageData['delivery_point']))

	if args.verbose:
		print("\nPerson(s) associated with this Address:")
	
	if len(pageData['current_residents']) is not 0:
		outputJSON += '"people":[ '
		for person in pageData['current_residents']:
			outputJSON += "{ "
			if args.verbose:
				print("\nName: ", person["name"])
				print("Age Range: ", person["age_range"])
				print("Gender: ", person["gender"])
				print("Resident Type: ", person["type"])
				print("Phone Number: ", person["phones"][0]["phone_number"])
			
			appendJSON("name", person["name"])
			appendJSON("ageRange", person["age_range"])
			appendJSON("gender", person["gender"])
			appendJSON("resType", person["type"])
			appendJSON("phone", person["phones"][0]["phone_number"])
			outputJSON = outputJSON[:-2]
			outputJSON += "}, "

		outputJSON = outputJSON[:-2]
		outputJSON += "], "


def street(lattitude, longitude):
	#####################################streetview model#############################################
	url2 = 'https://maps.googleapis.com/maps/api/streetview?size=400x400&location='
	key2 = '&pitch=10&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'
	query2 = url2 + str(lattitude) + ',' + str(longitude) + key2
	
	urllib.request.urlretrieve(query2, "templates/stView.jpg")
	
	#img2 = Image.open("templates/stView.jpg")
	#img2.show()
	
	CATEGORIES2 = ["apartment", "commercial", "house", "office", "vacant"]
	
	model2 = tf.keras.models.load_model("Models/CNNStreet.model")
	
	img_array2 = cv2.imread("templates/stView.jpg", cv2.IMREAD_COLOR)
	img_array2 = img_array2/255.0
	new_array2 = cv2.resize(img_array2, (400, 400))
	new_array2 = new_array2.reshape(-1, 400, 400, 3)
	
	prediction2 = model2.predict(new_array2)
	prediction2 = list(prediction2[0])
	if args.verbose:
		print("\nBuilding Type Prediction from StreetView: ", CATEGORIES2[prediction2.index(max(prediction2))])
	appendJSON("streetClass", CATEGORIES2[prediction2.index(max(prediction2))])

def sattelite(lattitude, longitude):
	#####################################sattelite model#############################################
	url1 = 'https://maps.googleapis.com/maps/api/staticmap?center='
	key1 = '&zoom=15&size=400x400&maptype=satellite&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8'
	query1 = url1 + str(lattitude) + ',' + str(longitude) + key1
	
	urllib.request.urlretrieve(query1, "templates/satellite.png")
	#img1 = Image.open("templates/satellite.png")
	#img1.show()
	
	CATEGORIES = ["city", "industrial", "rural", "suburban"]
	
	model = tf.keras.models.load_model("Models/CNN.model")
	
	img_array = cv2.imread("templates/satellite.png", cv2.IMREAD_COLOR)
	img_array = img_array/255.0
	new_array = cv2.resize(img_array, (400, 400))
	new_array = new_array.reshape(-1, 400, 400, 3)
	
	prediction = model.predict(new_array)
	prediction = list(prediction[0])
	if args.verbose:
		print("\nTerrain Prediction from Sattelite: ", CATEGORIES[prediction.index(max(prediction))])
	appendJSON("satClass", CATEGORIES[prediction.index(max(prediction))])

#Runtime code
addressData = get_street_info()

print_location_data(addressData, False)	
addressTest = get_compare_address(addressData['addressInfo'])

if args.sattelite:
	sattelite(str(addressData['lat']), str(addressData['long']))
if args.street:
	street(str(addressData['lat']), str(addressData['long']))

'''
with open('addr.json') as f:
	if args.verbose:
	pageData = json.load(f)
	#print(pageData)
'''
if args.whitePages:
	wpInput = format_whitepages_input(addressData['addressInfo'])
	pageData = get_whitepages_data(wpInput)
	print_whitepages_data(pageData)	

if args.localData:
	placeData = get_nearby_data(addressData)
	if args.printLocalData or args.printAddressData:
		if args.printAddressData:
			print_address_data(addressTest, placeData)
		else:
			print_place_data(placeData)
if args.verbose:
	if isFlagged:
		print(
		"     ||====================================================||\n"	
		"     ||         _       _     _                            ||\n"
		"     ||        /_\\   __| | __| | _ _  ___  ___ ___         ||\n"
		"     ||       / _ \\ / _` |/ _` || '_|/ -_)(_-<(_-<         ||\n"
		"     ||      /_/ \\_\\\\__,_|\\__,_||_|  \\___|/__//__/         ||\n"
		"     ||       ___  _                            _          ||\n"
		"     ||      | __|| | __ _  __ _  __ _  ___  __| |         ||\n"
		"     ||      | _| | |/ _` |/ _` |/ _` |/ -_)/ _` |         ||\n"
		"     ||      |_|  |_|\\__,_|\\__, |\\__, |\\___|\\__,_|         ||\n"
		"     ||                    |___/ |___/                     ||\n"
		"     ||====================================================||\n"
		)
		
		if isPostOffice:
			print("\n This address is a post office. Verify not a PO box.\n")
		
		if isEmbassy:
			print("\n This address is registered as an Embassy. Verify it is "
				  "also residential space.")

	elif isInteresting:
		print(
			"==================================================================\n"
			"          Address May Be Mixed Residential and Commercial         \n"
			"==================================================================\n")
outputJSON+='"flags": {'
appendJSON("interesting",str(isInteresting))
appendJSON("flagged",str(isFlagged))
appendJSON("embassy",str(isEmbassy))
appendJSON("postOffice",str(isPostOffice))
outputJSON = outputJSON[:-2]
outputJSON += '}, '
terminateJSON()

if args.verboseJSON:
	print(json.dumps(output, indent=4))

with open('templates/output.json', 'w') as outfile:
    json.dump(output, outfile)