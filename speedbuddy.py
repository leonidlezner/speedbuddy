from seeker import Seeker
import argparse
import logging




def main(arguments):
    seeker = Seeker(db_name=arguments.db)

    res = seeker.find(longitude=11.58731, latitude=50.92689, max_distance=1200)

    if len(res) < 1:
        print('Nothing found!')
    else:
        for point in res:
            print(point['distance'])


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser()

    #parser.add_argument('gps', help='GPS provider (record, gpsd)')
    parser.add_argument('-b', '--db', help='Database name', default='speedcams')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action="store_true")

    main(parser.parse_args())
