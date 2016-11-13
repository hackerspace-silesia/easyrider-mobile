'''
In this file you will find:

- functions definition for functions 

'''

from math import cos, asin, sqrt
import json

file_path = '/home/mik3398/EclipseProjects/EasyRider/MK_backend/json_data/02_track.json'

def distance(lat1, lon1, lat2, lon2):
    from math import cos, asin, sqrt
    p = 0.017453292519943295 #TODO: skąd się wzięła zmienna p, dla innych błąd całościowy trasy jest mniejszy np: 0.017753292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def track_distance(punkty = []):
	total_dist = 0.0
	for x in range(len(punkty)-1):
		lat1 = punkty[x]["latitude"]
		lon1 = punkty[x]["longitude"]
		lat2 = punkty[x+1]["latitude"]
		lon2 = punkty[x+1]["longitude"]
		total_dist += distance(lat1, lon1, lat2, lon2)
	return total_dist

with open(file_path) as data_file:
	data = json.load(data_file)
	
punkty = data["points"]["points"]

i = 20

lat1 = punkty[i]["latitude"]
lon1 = punkty[i]["longitude"]
alt1 = punkty[i]["altitude"]
lat2 = punkty[i+1]["latitude"]
lon2 = punkty[i+1]["longitude"]
alt2 = punkty[i+1]["altitude"]
dis_0_1_en = punkty[i+1]["distance"] - punkty[i]["distance"]
dis_0_1_my = distance(lat1, lon1, lat2, lon2)
error_dist_en_my = abs((dis_0_1_en - dis_0_1_my)/dis_0_1_en)*100

print ("Dis_0-1_en  	= %.10f" % dis_0_1_en)
print ("Dis_0-1_my 	= %.10f" % dis_0_1_my)
print ("Error_dist[%%]    	= %.10f" % error_dist_en_my)

Total_dist_my 			= track_distance(punkty)
Total_dist_en 			= punkty[len(punkty)-1]["distance"]
error_total_en_my		= abs((Total_dist_en - Total_dist_my)/Total_dist_en)*100

print ("_________________")
print ("Total_dist_my	= %.6f" %Total_dist_my)
print ("Total_dist_en	= %.6f" %Total_dist_en)
print ("Error_total[%%]		= %.10f" %error_total_en_my)