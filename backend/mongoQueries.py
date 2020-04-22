import pymongo
import json
from pymongo import MongoClient, GEO2D, GEOSPHERE
import pprint
from bson.son import SON

# db = MongoClient().carbonPollution
# database = db.carbonCounties

# print(database["coordinates"])

# database.create_index([("geometry", GEOSPHERE)])

# Geo intersects & within requires another document as a value i.e. $geometry
# Polygon uses 5 points with the end point being the first point.


db = MongoClient().averageCarbonPollution
database = db.carbonFeatureJsonList

database.create_index([("geometry", GEOSPHERE)])
# database.create_index([("coordinates", GEOSPHERE)])


newlist = []
# query = {'geometry': {'$geoIntersects': {'$geometry': {'type' : "Polygon" , 'coordinates': [ [ [ -88, 32], [-79, 32], [ -79, 24], [ -88, 24], [-88,32] ] ]}}}}
# query = {'geometry': {'$within': {'$geometry': {'type' : "Polygon" , 'coordinates': [ [ [ -88, 32], [-79, 32], [ -79, 24], [ -88, 24], [-88,32] ] ]}}}}
# query = {'geometry': {'$center':  [ [ -119.234617 ,47.732885],6 ]}}


# query = {'geometry': {'$within': {'$centerSphere': [[-121.217742, 45.670259], 1]}}}
query = {'geometry': {'$within': {'$centerSphere': {'type' : "Point" , 'coordinates': [[-121.217742, 45.670259], 1]}}}}

# query = {'coordinates': {'$within': {'$centerSphere': [[-121.217742, 45.670259], 1]}}}

# data.features.geometry.coordinates


for doc in database.find(query):
    newlist.append(doc)
    pprint.pprint(doc)

print("newlist-length", len(newlist))