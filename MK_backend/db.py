from pymongo import MongoClient
from datetime import datetime

'''
schema_track = {
    'uuid4': {
        'type': 'string',
        'required': True,
    },
    'point': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'lat': {'type': 'string'},
                'lon': {'type': 'string'},
                'time': {'type': 'integer'}
            }
        }
    },
    'distance': {'type': 'integer'},
    'name': {'type': 'string'},
    'timestart': {'type': 'integer'},
    'timestop': {'type': 'integer'}
}
'''


class WorkerMongo(object):

    def __init__(self, worker_id='wk1', mongo_host='localhost', mongo_port=27017, mongo_dbname='apitest'):
        self.client = MongoClient(mongo_host, mongo_port)
        self.db = self.client[mongo_dbname]
        self.worker_id = worker_id

    def validate_date(self, datestring):
        try:
            # YYYY-MM-DDTHH:mm:ss.sssZ
            tmp = datetime.strptime(datestring[0:20], '%Y-%m-%dT%H:%M:%S.')
            return tmp.timestamp()
        except ValueError:
            return datestring

    def get_point(self, uuid4=None):
        query = {}
        point_collection = self.db.point
        if uuid4:
            query = {'uuid4': uuid4}
        result = []
        for point in point_collection.find(query).sort([('time', 1)]):
            # print(point)
            result.append({
                'time': int(self.validate_date(point['time'])),
                'uuid4': point['uuid4'],
                'lat': point['point']['lat'],
                'lon': point['point']['lon']})
            point_collection.update_one({'_id': point['_id']}, {'$set': {'worker_id': self.worker_id}})
        return result

    def del_worker_point(self, worker_id=None):
        if worker_id:
            res = self.db.point.delete_many({'worker_id': worker_id})
            return res.deleted_counts
        return 0

    def get_tracks(self, uuid4=None, track_id=None, oldest_one=False):
        '''
        zwraca sciezke po uuid4, _id lub najnowsza
        '''
        track_collection = self.db.track
        query = {}
        if uuid4:
            query = {'uuid4': uuid4}
        if track_id:
            query = {'_id': track_id}
        tracks = []
        for track in track_collection.find(query).sort([('timestop', -1)]):
            tracks.append(track)
        return tracks

    def check_track(self, uuid4, timestamp, margin=60):
        '''
        sprawdza czy dla podanego timestampi marginesu jest jakas sciezka, jesli jest to zwraca
        '''
        track_collection = self.db.track
        timelimit = timestamp - margin
        return track_collection.find_one({'uuid4': uuid4, "timestop": {"$gt": timelimit}})

    def save_track(self, track):
        '''
        jesli ma '_id' to robi replace
        '''
        track_collection = self.db.track
        if '_id' in track:
            track_collection.delete_one({'_id': track['_id']})
        new_track = {k: track[k] for k in track.keys() if not k.startswith('_')}
        res = track_collection.insert_one(new_track)
        return res.inserted_id


if __name__ == '__main__':
    wrk = WorkerMongo(mongo_host='192.168.1.185', worker_id='wk2')
    # print(wrk.get_point(uuid4='9daea379-9e52-4611-bf61-60d4cd305b16'))
    # print(wrk.check_track(uuid4='9daea379-9e52-4611-bf61-60d4cd305b16', timestamp=1455810100))
    track = wrk.get_tracks(uuid4='9daea379-9e52-4611-bf61-60d4cd305b16')
    print(track)
    track[0]['point'].append({'lat': '40.7127841', 'lon': '-74.005960', 'time': 1455810100})
    print(wrk.save_track(track[0]))
    print(wrk.get_tracks(uuid4='9daea379-9e52-4611-bf61-60d4cd305b16'))
