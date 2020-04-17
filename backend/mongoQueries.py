import pymongo
import json
from pymongo import MongoClient, GEO2D, GEOSPHERE 
import pprint
from bson.son import SON

db = MongoClient().carbonPollution
database = db.carbonFeatureJson

# print(database["coordinates"])

database.create_index([("coordinates", GEOSPHERE)])
database.create_index([("coordinates", GEO2D)])
database.create_index([("geometry", GEOSPHERE)])
database.create_index([("geometry", GEO2D)])

query = {"geometry": {"$within": {"$box": [[ -87.359296, 35.00118], [-131.602021, 55.117982]]}}}
for doc in database.find(query).sort('_id'):
    pprint.pprint(doc)






############# Documentation ################

# db = MongoClient().geo_example
# index = db.places.create_index([("loc", GEO2D)])
# print(db)


# result = db.places.insert_many([{"loc": [2, 5]},{"loc": [30, 5]},{"loc": [1, 2]},{"loc": [4, 4]}])  
# print(result.inserted_ids)

# for doc in db.places.find({"loc": {"$near": [3, 6]}}).limit(3):
#     pprint.pprint(doc)



