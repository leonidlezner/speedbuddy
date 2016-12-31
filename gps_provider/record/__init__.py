import gps_provider


class RecordProvider(gps_provider.GPSProvider):
    def __init__(self):
        print('Loading data...')

    def __del__(self):
        pass

    def next(self):
        next_value = {'longitude': 23.58728, 'latitude': 46.77467}

        return next_value
