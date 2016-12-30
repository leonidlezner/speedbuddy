from seeker import Seeker
from mainrunner import MainRunner

import argparse
import logging
import time

from gps_provider.record import RecordProvider
from gps_provider.gpsd import GpsdProvider


class SpeedBuddy(MainRunner):
    def __init__(self, db_name):
        MainRunner.__init__(self)
        self.seeker = Seeker(db_name=db_name)
        self.gps_provider = None

        self.gps_providers = {
            'gpsd': GpsdProvider,
            'record': RecordProvider
        }

    def loop(self):
        current_position = self.gps_provider.next()
        print(current_position)
        time.sleep(1)

    def load_gps_provider(self, provider_name):
        if not self.gps_providers.has_key(provider_name):
            raise RuntimeError('Provider {} not found!'.format(provider_name))

        logging.debug('Loading GPS provider "{}"!'.format(provider_name))

        self.gps_provider = self.gps_providers[provider_name]()

    def cleanup(self):
        if self.gps_provider is not None:
            del self.gps_provider


def main(arguments):
    speedbuddy = SpeedBuddy(db_name=arguments.db)

    speedbuddy.load_gps_provider(provider_name=arguments.gps)

    speedbuddy.start()

    speedbuddy.lock()

    '''
    seeker = Seeker()

    res = seeker.find(longitude=11.58731, latitude=50.92689, max_distance=1200)

    if len(res) < 1:
        print('Nothing found!')
    else:
        for point in res:
            print(point['distance'])
    '''


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create the argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('gps', help='GPS provider (record, gpsd)')
    parser.add_argument('-b', '--db', help='Database name', default='speedcams')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action="store_true")

    main(parser.parse_args())
