from xml.dom import minidom

file_path = '/home/mik3398/Desktop/python/gpx_data/01_track.gpx'

DOMTree = minidom.parse(file_path)

cNodes = DOMTree.childNodes

i = cNodes[0].getElementsByTagName("trkpt")

tab = [[0 for x in range(len(i))] for x in range(2)]
k=0
for i in cNodes[0].getElementsByTagName("trkpt"):
	tab[0][k]= i.getAttribute("lat")
	tab[1][k]= i.getAttribute("lon")
	k=k+1
	
print tab[0][0] + ', ' + tab[1][0]

#print(cNodes[0].getElementsByTagName("trkpt")[0].getAttribute("lat"))