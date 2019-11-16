#generate sattelite image data for training/testing purposes
#ben jollymore 2019

import csv

with open('cpairs.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		lat = {row[0]}
		lng = {row[1]}
		name = "pics/" + {row[2]}
		exec('python retrieveImage.py ' + lat + " " + lng + " " + name)