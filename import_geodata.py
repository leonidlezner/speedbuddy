import csv
from bson.son import SON
import pymongo
from pymongo import MongoClient


class GeoFormatException(Exception):
    pass

class GeodataImporter:
    def __init__(self, db_collection=None):
        self.points = []
        self.total_points = 0
        self.db_collection = db_collection

    def import_row(self, row):
        #self.points.append(row)
        #return

        if self.db_collection is not None:
          self.db_collection.insert({
            'name': row[2],
            'speed': row[3],
            'mobile': row[4],
            'loc': {
              'type': 'Point',
              'coordinates': [row[0], row[1]],
            }
          })

    def load(self, filename, speed=0, mobile=False):
        print('Loading file {}'.format(filename))

        # Open the csv file and iterate through the lines
        with open(filename, 'r', encoding="ISO-8859-1") as csvfile:
            row_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in row_reader:
                # Check the number of columns
                if len(row) != 3:
                    raise GeoFormatException("Wrong geo data format: {}".format(', '.join(row)))

                # Create a tuple with geo coordinates
                geo_point = (float(row[0]), float(row[1]), row[2], speed, mobile)

                # Count up the point counter
                self.total_points += 1

                # Process the row
                self.import_row(geo_point)





def import_demo():
    mongo = MongoClient()
    database = mongo['speedcams']
    
    database.points.drop()
    
    points = database.points
    
    points.ensure_index([("loc", pymongo.GEOSPHERE)])
    
    
    importer = GeodataImporter(db_collection=points)

    importer.load('./garmin-mobil/Blitzer_mobil.csv', speed=0, mobile=True)

    for speed in range(10, 140, 10):
        importer.load('./garmin-mobil/Blitzer_mobil_{}.csv'.format(speed), speed=speed, mobile=True)

    importer.load('./garmin-mobil/Blitzer_mobil_Abstand.csv', speed=0, mobile=True)
    
    #print(importer.points)


if __name__ == '__main__':
    import_demo()

