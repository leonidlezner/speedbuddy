from seeker import Seeker
from mainrunner import MainRunner

import argparse
import logging
import time

from gps_provider.record import RecordProvider
from gps_provider.gpsd import GpsdProvider

from notificator.console import ConsoleNotificator
from notificator.rgbled import RgbLedNotificator

class SpeedBuddy(MainRunner):
    def __init__(self, db_name):
        MainRunner.__init__(self)
        self.seeker = Seeker(db_name=db_name)
        self.gps_provider = None
        self.notificators = []
        self.distance = 200

        self.gps_provider_list = {
            'gpsd': GpsdProvider,
            'record': RecordProvider
        }

        self.notificator_list = {
            'console': ConsoleNotificator,
            'rgbled': RgbLedNotificator
        }

    def loop(self):
        current_position = self.gps_provider.next()

        if current_position is not None:
            cameras = self.seeker.find(current_position['longitude'], current_position['latitude'], self.distance)

            if len(cameras) > 0:
                for notificator in self.notificators:
                    notificator.notify(cameras)

        time.sleep(1)

    def set_gps_provider(self, provider_name):
        if provider_name not in self.gps_provider_list:
            raise RuntimeError('Provider {} not found!'.format(provider_name))

        logging.debug('GPS provider set to "{}".'.format(provider_name))

        self.gps_provider = self.gps_provider_list[provider_name]()

    def add_notificator(self, notificator_name):
        if notificator_name not in self.notificator_list:
            raise RuntimeError('Notificator {} not found!'.format(notificator_name))

        self.notificators.append(self.notificator_list[notificator_name]())

        logging.debug('Added notificator "{}".'.format(notificator_name))

    def cleanup(self):
        if self.gps_provider is not None:
            del self.gps_provider

        for notificator in self.notificators:
            del notificator


def main(arguments):
    speedbuddy = SpeedBuddy(db_name=arguments.db)

    speedbuddy.set_gps_provider(provider_name=arguments.gps)

    speedbuddy.add_notificator('console')
    speedbuddy.add_notificator('rgbled')

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
