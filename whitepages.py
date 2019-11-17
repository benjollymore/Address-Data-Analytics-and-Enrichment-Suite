import json
import urllib
import requests

url = "https://api.ekata.com/3.0/location?api_key=cffb32044ba94e209665f793595abe37"
cityStr = "&city="
countryStr = "&country_code="
postalStr = "&postal_code="
provStr="&state_code="
streetStr = "&street_line_1="
suiteStr = "&street_line_2="

##placeholder data fill in from the other json##
city = "Halifax"
country = "CA"
postal = "B3L 3G9"
prov = "NS"
street = "2529 Sherwood St"
suite = ""

cityStr += city.replace(" ", "+")
countryStr += country
postalStr += postal.replace(" ", "")
provStr += prov
streetStr += street.replace(" ", "+")
suiteStr += suite

query = url + cityStr + countryStr + postalStr + provStr + streetStr + suiteStr
'''
page = requests.get(query)
pageData = page.json()
print(pageData)

'''

with open('addr.json') as f:
    pageData = json.load(f)
    print(pageData)

print("Mailing Status:")
print("\nActive: ",pageData['is_active'])
print("Commericial: ",pageData['is_commercial'])
print("Forwarding Mail: ",pageData['is_forwarder'])
print("Delivery Type: ",pageData['delivery_point'])

print("\nPerson(s) associated with this Address:")
for person in pageData['current_residents']:
	print("\nName: ", person["name"])
	print("Age Range: ", person["age_range"])
	print("Gender: ", person["gender"])
	print("Resident Type: ", person["type"])
	print("Phone Number: ", person["phones"][0]["phone_number"])