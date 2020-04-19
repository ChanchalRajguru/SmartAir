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




# query = {'geometry': {'$geoIntersects': {'$geometry': {'type' : "Polygon" , 'coordinates': [ [ [ -88, 32], [-79, 32], [ -79, 24], [ -88, 24], [-88,32] ] ]}}}}
query = {'geometry': {'$within': {'$geometry': {'type' : "Polygon" , 'coordinates': [ [ [ -88, 32], [-79, 32], [ -79, 24], [ -88, 24], [-88,32] ] ]}}}}


for doc in database.find(query):
    pprint.pprint(doc)

############# Documentation ################

# db = MongoClient().geo_example
# index = db.places.create_index([("loc", GEO2D)])
# print(db)


# result = db.places.insert_many([{"loc": [2, 5]},{"loc": [30, 5]},{"loc": [1, 2]},{"loc": [4, 4]}])  
# print(result.inserted_ids)

# for doc in db.places.find({"loc": {"$near": [3, 6]}}).limit(3):
#     pprint.pprint(doc)