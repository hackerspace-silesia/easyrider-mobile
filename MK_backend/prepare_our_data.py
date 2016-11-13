# -*- coding: utf-8 -*-

import json
import datetime

#Tworzymy nasza liste slownikow	
single = {}
our_data = []


with open('/home/mik3398/Desktop/python/json_data/01_track.json') as data_file:
	data1 = json.load(data_file)
	
with open('/home/mik3398/Desktop/python/json_data/02_track.json') as data_file:
	data2 = json.load(data_file)

with open('/home/mik3398/Desktop/python/json_data/03_track.json') as data_file:
	data3 = json.load(data_file)

with open('/home/mik3398/Desktop/python/json_data/04_track.json') as data_file:
	data4 = json.load(data_file)	

punkty1 = data1["points"]["points"]
punkty2 = data2["points"]["points"]
punkty3 = data3["points"]["points"]
punkty4 = data4["points"]["points"]

#przygotuj nasze dane:
# jest to tablica z słowników
# pojedyńczy słownik reprezentuje jeden punkt i zawiera pola:
# uuid - identyfikator urządzenia
# lat - latitude
# lon - longitude
# time - czas pomiaru

for punkt in punkty1:
	#time conversion from UTC to seconds since 1970.1.1
	czas_sec = (datetime.datetime.strptime(punkt["time"], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.datetime(1970,1,1)).total_seconds()
	our_data.append({"lat":punkt["latitude"], "lon":punkt["longitude"], "time":int(czas_sec), "uuid":10000})
for punkt in punkty2:
	czas_sec = (datetime.datetime.strptime(punkt["time"], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.datetime(1970,1,1)).total_seconds()
	our_data.append({"lat":punkt["latitude"], "lon":punkt["longitude"], "time":int(czas_sec), "uuid":10000})
for punkt in punkty3:
	czas_sec = (datetime.datetime.strptime(punkt["time"], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.datetime(1970,1,1)).total_seconds()
	our_data.append({"lat":punkt["latitude"], "lon":punkt["longitude"], "time":int(czas_sec), "uuid":10000})
for punkt in punkty4:
	czas_sec = (datetime.datetime.strptime(punkt["time"], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.datetime(1970,1,1)).total_seconds()
	our_data.append({"lat":punkt["latitude"], "lon":punkt["longitude"], "time":int(czas_sec), "uuid":10000})

print len(our_data)

print our_data[123]
	
#Our Data is ready for processing 
#(it corresponds to server response for one UUID)
#print our_data