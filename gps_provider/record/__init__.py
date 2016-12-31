import gps_provider


class RecordProvider(gps_provider.GPSProvider):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def next(self):
        return {'longitude': 23.58728, 'latitude': 46.77467}
