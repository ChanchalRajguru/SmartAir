import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["averageCarbonPollution"]

def insertForest():
    file = open("data\ForestJson.json", "r")
    forestData = json.load(file) 
    data = []
    for each in forestData["features"]:
        newCoordinates = each["geometry"]["coordinates"][0]
        each["geometry"]["coordinates"] = newCoordinates
        data.append(each)

    ## DB name
    mycol = mydb["forestListRefined"]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

    ### Inserting it into MongoDB
    # jsondata = mycol.insert_many(data)

    # print("Inserting into Mongo!!")

    # ### print list of the _id values of the inserted documents:
    # print(jsondata.inserted_ids) 


insertForest()