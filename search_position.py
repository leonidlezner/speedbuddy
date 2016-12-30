from bson.son import SON
import pymongo
from pymongo import MongoClient
import math

# Source http://www.johndcook.com/blog/python_longitude_latitude/
def distance_on_unit_sphere(lat1, long1, lat2, long2):
  # Convert latitude and longitude to
  # spherical coordinates in radians.
  degrees_to_radians = math.pi/180.0
 
  # phi = 90 - latitude
  phi1 = (90.0 - lat1)*degrees_to_radians
  phi2 = (90.0 - lat2)*degrees_to_radians
 
  # theta = longitude
  theta1 = long1*degrees_to_radians
  theta2 = long2*degrees_to_radians
 
  # Compute spherical distance from spherical coordinates.
 
  # For two locations in spherical coordinates
  # (1, theta, phi) and (1, theta', phi')
  # cosine( arc length ) =
  # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
  # distance = rho * arc length
 
  cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
  math.cos(phi1)*math.cos(phi2))
  arc = math.acos( cos )
 
  # Remember to multiply arc by the radius of the earth
  # in your favorite set of units to get length.
  return arc * 6371 * 1000

def main():
  mongo = MongoClient()
  database = mongo['speedcams']
    
  points = database.points
  
  while True:
    
    coordinates = input('C>')#[47.532554, 8.709355]
    
    coordinates = [float(c) for c in coordinates.split(',')]
  
    coordinates.reverse()
  
    max_distance = 200

    query = {
      'loc':
        {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', coordinates)])), ('$maxDistance', max_distance)])
      }
    }
  
    print('Searching...')
  
    for point in points.find(query):
      print(point['loc']['coordinates'], distance_on_unit_sphere(point['loc']['coordinates'][1], point['loc']['coordinates'][0], coordinates[1], coordinates[0]))
  
      
if __name__ == '__main__':
  main()
