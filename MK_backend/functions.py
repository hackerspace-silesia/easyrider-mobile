'''
In this file you will find:

- only definitions of functions

'''

# this function will simply calculate distance between two points
def distance(lat1, lon1, lat2, lon2):
    from math import cos, asin, sqrt
    p = 0.017453292519943295 #TODO: skąd się wzięła zmienna p, dla innych błąd całościowy trasy jest mniejszy np: 0.017753292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))