import pymongo
import json
from pymongo import MongoClient, GEO2D, GEOSPHERE 
import pprint
from bson.son import SON

# db = MongoClient().carbonPollution
# database = db.carbonCounties

# print(database["coordinates"])

#database.create_index([("geometry", GEOSPHERE)])

# Geo intersects & within requires another document as a value i.e. $geometry
# Polygon uses 5 points with the end point being the first point.


db = MongoClient().averageCarbonPollution
database = db.carbonFeatureJsonList

query = {'geometry': {'$geoIntersects': {'$geometry': {'type' : "Polygon" , 'coordinates': [ [ [ -88, 32], [-79, 32], [ -79, 24], [ -88, 24], [-88,32] ] ]}}}}
# query = {'geometry': {'$within': {'$geometry': {'type' : "Polygon" , 'coordinates': [ [ [ -88, 32], [-79, 32], [ -79, 24], [ -88, 24], [-88,32] ] ]}}}}
# for doc in database.find(query):
#     pprint.pprint(doc)

query_maxDistance = {'geometry': {'$near': {'$geometry': {'type' : "Polygon" , 'coordinates': [ [ [ -88, 32], [-79, 32], [ -79, 24], [ -88, 24], [-88,32] ] ], }},("$maxDistance", 100) }}
for doc in database.find(query_maxDistance):
    pprint.pprint(doc)


