import gps_provider
from gps3.agps3threaded import AGPS3mechanism


class GpsdProvider(gps_provider.GPSProvider):
    def __init__(self):
        self.agps_thread = AGPS3mechanism()
        self.agps_thread.stream_data()
        self.agps_thread.run_thread()

    def next(self):
        # Check if coordinates are available
        if self.agps_thread.data_stream.lon != 'n/a':
            next_value = {
                'longitude': self.agps_thread.data_stream.lon,
                'latitude': self.agps_thread.data_stream.lat
            }
        else:
            next_value = None

        return next_value

    def __del__(self):
        del self.agps_thread
