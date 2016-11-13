import json, os
from pprint import pprint

with open('/home/mik3398/Desktop/python/json_data/03_track.json') as data_file:
	data = json.load(data_file)
	
punkty = data["points"]["points"]

#Punkty jest lista slownikow
print punkty[0]

print len(data["points"])

print len(data["points"]["points"])

for punkt in punkty:
	print punkt["time"]
	print punkt["longitude"]
	print punkt["latitude"]





'''
print type(data)
print type(punkty)

print data.has_key("points")
print data.has_key("time")

print "MKMKMK"
print len(data["points"])
'''

