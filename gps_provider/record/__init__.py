import gps_provider
import gpxpy
import gpxpy.gpx
import os

class RecordProvider(gps_provider.GPSProvider):
    def __init__(self):
        print('Loading data...')

        dir_path = os.path.dirname(os.path.realpath(__file__))

        gpx_file = open(os.path.join(dir_path, 'data', 'demo1.gpx'), 'r')

        self.gpx = gpxpy.parse(gpx_file)

        self.points = self.gpx.tracks[0].segments[0].points

        self.current_point = 0
        self.max_points = len(self.points)

    def __del__(self):
        pass

    def next(self):
        next_point = self.points[self.current_point]
    
        next_value = {'longitude': next_point.longitude, 'latitude': next_point.latitude}

        self.current_point += 1

        if self.current_point >= self.max_points:
            self.current_point = 0

        return next_value

