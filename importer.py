"""
Camera data importer module
"""

import json
import os
import csv
import pymongo
from pymongo import MongoClient

class Importer(object):
    """
    Camera data importer
    """

    def __init__(self):
        self.points = 0

        mongo = MongoClient()

        database = mongo['speedcams']

        database.points.drop()

        points = database.points

        points.ensure_index([("loc", pymongo.GEOSPHERE)])

        self.db_collection = points


    def load(self, config_file):
        """
        Method for loading the configuration file
        """
        with open(config_file) as json_data:
            data = json.load(json_data)

            files = data['files']

            folder = os.path.dirname(config_file)

            for file_config in files:
                self.load_file_from_config(file_config, folder)

    def insert_db_row(self, row):
        self.points += 1

        if self.db_collection is not None:
            self.db_collection.insert(row)

    def load_file_from_config(self, file_config, folder_name):
        # Construct the complete path
        file_path = os.path.join(folder_name, file_config['source'])
        speed = file_config.get('speed', None)
        mobile_cam = file_config.get('mobile', False)

        print('Loading file: {}'.format(file_path))

        line_counter = 0

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

                self.insert_db_row(row)

        print('Points: ', line_counter)


def main():
    importer = Importer()
    importer.load('./data/speedcams.json')
    print('Total Points: ', importer.points)


if __name__ == '__main__':
    main()
