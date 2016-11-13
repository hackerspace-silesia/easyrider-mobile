# -*- coding: utf-8 -*-

from math import cos, asin, sqrt
import json, datetime

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

print "\n\n"	
print "Total len of our_data container is %d" %len(our_data)
print "\n"
print "Example container (point) data is:"
print our_data[123]
	
#Our Data is ready for processing 
#(it corresponds to server response for one UUID)
#print our_data


def calc_single_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def calc_distance_on_track(track):
	total_dist = 0.0
	for x in range(len(track)-1):
		lat1 = track[x]["lat"]
		lon1 = track[x]["lon"]
		lat2 = track[x+1]["lat"]
		lon2 = track[x+1]["lon"]
		total_dist += calc_single_distance(lat1, lon1, lat2, lon2)
	return total_dist
		

def calc_speed(distance,time):
	#[km, s]
	if time != 0:
		return 3600*distance/time
	return 0	
	#[km, h]


print "___________________"
print "LOADED DATA FROM MONGO DB"
print "___________________"
print "for one user (UUID)"


#zacznij dzielic dane na trasy

#my_tracks będzie listą list słowników
# od góry: 	pierwsza lista to numer jednolitej trasy
# 			druga lista to lista słowników (punktów) trasy
#			trzeci element to słownik (punkt) okreslajacy wspolrzedne i czas
my_tracks = []

#last_record to ostatni element (słownik) ostatniej trasy z listy tras
#należy sprawdzić czy kolejna paczka danych jest kontynuacją starej trasy
#czy ma być traktowana jako nowa trasa
last_record = {}
#last_record = my_tracks[len(my_tracks)-1][len(my_tracks[len(my_tracks)-1])-1]
#or in case its' first track last_record is 0 or not needed


#warunki na łączenie trasy tutaj:
def is_track_continous(last_record,new_record):
	
	answer = 0 #default answer = no
	
	# [s]
	my_time = new_record["time"] - last_record["time"]
	#0: czas mniejszy niż 15minut:
	if my_time < 900:
		#1: czy odleglosci nie sa wieksze niż 500m
		# [km]
		my_dist = calc_single_distance (last_record["lat"], last_record["lon"],\
					   new_record["lat"], new_record["lon"])
		if my_dist < 0.5:
			#2: prędkość mniejsza niż 50km/h:
			# [km/h]
			my_speed = calc_speed(my_dist,my_time)
			if my_speed < 50:
				answer = 1 #change answer to yes
	return answer


def divide_into_tracks(our_data):
	
	my_tracks = []
	current_track = []
	
	#last_record = get_last_record(our_data[0]["time"],900)
	#TODO: stubbed !!!
	last_record = our_data[0]
	is_continous = is_track_continous(last_record,our_data[0])
	
	for x in range(len(our_data)-1):
		
		if 1 == is_continous:
			#print "MK1"
			current_track.append(our_data[x])
		elif 0 == is_continous:
			print "MK0 %d" %x
			my_tracks.append(current_track)
			current_track = []
			current_track.append(our_data[x])
		is_continous = is_track_continous(our_data[x],our_data[x+1])
	
	#put last track to variable my_tracks
	my_tracks.append(current_track)
	current_track = []
	
	return my_tracks
			
def calc_tracks_info(my_tracks):
	
	time_start = 0
	time_end = 0
	time_total = 0
	distance_total = 0
	avg_speed = 0
	
	tracks_info = []
	
	for track in my_tracks:
		time_start = track[0]["time"]
		time_end = track[len(track)-1]["time"]
		time_total = time_end - time_start
		distance_total = calc_distance_on_track(track)
		avg_speed = calc_speed(distance_total,time_total)
		
		tracks_info.append([time_start, time_end, time_total, distance_total, avg_speed])
	
	return tracks_info
		
		
		
	


new_record = our_data[1]
last_record = our_data[0]



my_time = new_record["time"] - last_record["time"]
my_dist = calc_single_distance (last_record["lat"], last_record["lon"],\
					   new_record["lat"], new_record["lon"])
my_speed = calc_speed(my_dist,my_time)

print "my..."
print my_time
print my_dist
print my_speed

new_record = our_data[2]
last_record = our_data[1]

print "is... %d" % is_track_continous(last_record,new_record)
		
check_tab = []

last_record = our_data[0]


for x in range(len(our_data)):
	
	if 0 == is_track_continous(last_record,our_data[x]):
		check_tab.append(x)
	last_record = our_data[x]
	
print check_tab

my_tracks_full_data = divide_into_tracks(our_data)

print "Data divided into %d tracks" % len(my_tracks_full_data)
print "track no 1"
#print my_tracks_full_data

tracks_info = calc_tracks_info (my_tracks_full_data)

print "Printing total tracks info: "
print "____Track 1"
print "total time: %d sec" %tracks_info[0][2]
print "total dist: %f km" %tracks_info[0][3]
print "avg  speed: %f km/h" %tracks_info[0][4]
print "____Track 2"
print "total time: %d sec" %tracks_info[1][2]
print "total dist: %f km" %tracks_info[1][3]
print "avg  speed: %f km/h" %tracks_info[1][4]
print "____Track 3"
print "total time: %d sec" %tracks_info[2][2]
print "total dist: %f km" %tracks_info[2][3]
print "avg  speed: %f km/h" %tracks_info[2][4]
print "____Track 4"
print "total time: %d sec" %tracks_info[3][2]
print "total dist: %f km" %tracks_info[3][3]
print "avg  speed: %f km/h" %tracks_info[3][4]