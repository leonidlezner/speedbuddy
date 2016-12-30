"""
Camera data importer module
"""

import json
import os
import csv
import pymongo
from pymongo import MongoClient
import argparse
import logging


class Importer(object):
    """
    Camera data importer
    """

    def __init__(self, db_name='speedcams'):
        self.points = 0
        # Creating the client
        mongo = MongoClient()

        # Getting the database
        database = mongo[db_name]

        # Clearing the 'points' data base table
        database.points.drop()

        points = database.points

        points.ensure_index([("loc", pymongo.GEOSPHERE)])

        self.db_collection = points

    def load(self, config_file):
        """
        Method for loading the configuration file
        :param config_file: Path to the config JSON file
        """
        with open(config_file) as json_data:
            data = json.load(json_data)

            files = data['files']

            folder = os.path.dirname(config_file)

            for file_config in files:
                self.load_file_from_config(file_config, folder)

    def load_file_from_config(self, file_config, folder_name):
        """
        Method for loading the gps data and importing it to the DB

        :param file_config: Dictionary with file configuration info
        :param folder_name: Path to the folder containing the speed cameras
        :return:
        """

        # Construct the complete path
        file_path = os.path.join(folder_name, file_config['source'])

        speed = file_config.get('speed', None)

        mobile_cam = file_config.get('mobile', False)

        logging.debug('Loading file: {}'.format(file_path))

        line_counter = 0
        rows = []

        # Open the csv file and iterate through the lines
        with open(file_path, 'r', encoding="ISO-8859-1") as csvfile:
            row_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            # Iterating through rows
            for row in row_reader:
                line_counter += 1

                # Latitude
                latitude = float(row[1])

                # Longitude
                longitude = float(row[0])

                # Description
                description = row[2]

                row = {
                    'name': description,
                    'speed': speed,
                    'mobile': mobile_cam,
                    'loc': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude],
                    }
                }

                rows.append(row)

        logging.debug('Points: {}'.format(line_counter))

        self.points += line_counter

        # Insert the file content into the database
        self.db_collection.insert_many(rows)


def main(arguments):
    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)

    importer = Importer(db_name=arguments.db)

    importer.load(config_file=arguments.config)

    logging.debug('Total Points: {}'.format(importer.points))


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('config', help='JSON configuration file')
    parser.add_argument('-b', '--db', help='Database name', default='speedcams')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action="store_true")

    main(parser.parse_args())
