import csv
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pickle
import time
import statistics
import re
import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["carbonPollution"]

#Creates a dict of list for all states in USA
#Output {"statename1":[], "statename2":[],.....}
def usStatesList(fileName):
    statesList = []
    statesDict = {}
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t') # Reading the Carbon.csv file
        for row in reader:
            if row["State"] not in statesList: #Checking if state is already present in the list, if not add.
                statesList.append(row["State"])
        for each in statesList: # Creating the dict of lists for states 
            if each not in statesDict:
                statesDict[each] = []
        return statesDict  

#Take the mean value for all the occurance for each state from Carbon.csv file for the given pollutant.
#Output {"statename1":[12.827382728], "statename2":[17.436762099],.....}
def avgValue(fileName):
    pollutantDict = usStatesList('data\Carbon.csv') #calling usStatesList function returns {"statename1":[], "statename2":[],.....}
    avgDict = {}
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t') # Reading the Carbon.csv file
        for row in reader:
            if row["State"] in pollutantDict.keys(): 
                maxHour = float(row["CO2 1st Max Hour"]) # taking into consideration the CO2 1st Max Hour
                if maxHour != 0:
                    pollutantDict[row["State"]].append(maxHour) # appending it to the dictionary
        for key in pollutantDict:
            if len(pollutantDict[key]) !=0:
                avgDict[key] = statistics.mean(pollutantDict[key]) # taking the average of all available states 
    return avgDict


#Creates a JSON FeatureCollection and inserts it into MongoDB
def carbonJson():
    avgDict = avgValue('data\Carbon.csv') #returns {"statename1":[12.827382728], "statename2":[17.436762099],.....}
    with open('data/us-states.json', newline='') as json_file: # using an exiting json file which has the Polygon Co-ordinates
        data = json.load(json_file)
        for state in avgDict:
            for key in data["features"]:
                if state == key["properties"]["name"]:
                    key["properties"]["carbon"] = avgDict[state] #adding the carbon mean data to the JOSN file. 
        mycol = mydb["carbonFeatureJson"]
        
        #Inserting it into MongoDB
        # jsondata = mycol.insert_many([data]) #[ObjectId('5e8726922a655e3947524340')] 
        
        #print list of the _id values of the inserted documents:
        # print(jsondata.inserted_ids) 
        
        # f = open("data/carbon.json", "a")
        # f.write(json.dumps(data))
        # f.close()            

# carbonJson()





#Generates the Lat and Long for address which start from county and uses the UsAllAddress.dat file to fetch the addresses
def getLatLong():
    nom = Nominatim(user_agent="APSolution", timeout=63)
    allAddresses = pickle.load(open("Data/UsAllAddress.dat", "rb"))
    listOfAdress = []
    for each in allAddresses:
        addressDict = {}
        if "Not in a city" in each:
            each = each.replace(", Not in a city","")
        location = nom.geocode(each)
        if location!= None:
            addressDict[each] = {"latitude":location.latitude,"longitude":location.longitude}
            listOfAdress.append(addressDict)
    pickle.dump(listOfAdress, open("Data/LatLongOfCounty.dat", "wb"))

# getLatLong()

def fileOpen(fileName):
    featureCollection = {"type": "FeatureCollection", "features": []}
    allCountys = []
    with open(fileName, newline='') as csvfile:
        num = 0
        reader = csv.DictReader(csvfile)
        listOfAddress = pickle.load(open("Data/LatLongOfCounty.dat","rb"))
        allAddresses = pickle.load(open("Data/UsAllAddress.dat","rb"))
        for row in reader:
            # Do not delete the code below
            #     if int(row["SerialNo"]) < 4046:#stores address of County, City, State, United States Of America"
            # address = row["County"] + ", " + row["City"] + ", " + row["State"] + ", " + "United States Of America"
            # if address not in allAddresses:
            #     num+=1
            #     print(num," ", address)
            #     allAddresses.append(address)
        # pickle.dump(allAddresses, open("UsAllAddress.dat", "wb"))
            serialnum = row["SerialNo"]
            address = row["County"] + ", " + row["City"] + ", " + row["State"] + ", " + "United States Of America"
            # if "Not in a city" in address: #striping out Not in a city
            #     address = address.replace(", Not in a city", "")
            for eachAdd in listOfAddress: #checking if address is present in the LatLong List
                if address in eachAdd:
                    if row["CO2 Mean"]:
                        featureDict = {"type": "Feature",
                                          "properties": {
                                              "county": row["County"],
                                              "city":row["City"],
                                              "state":row["State"],
                                              "country":"United States Of America",
                                              "co2Mean": row["CO2 Mean"],
                                              "date":row["Date Local"]
                                          },
                                          "geometry": {
                                            "type": "Point",
                                            "coordinates": [
                                             eachAdd[address]["longitude"],eachAdd[address]["latitude"]
                                            ]}}
                        if featureDict not in featureCollection["features"]:
                            if address not in allCountys:
                                featureCollection["features"].append(featureDict)
                                allCountys.append(address)
                                print("Added!!")
                                print(num, " ",featureDict)
                        num+=1
                        print("serialnum  ", serialnum)
                        # time.sleep(5)
                    else:
                        num+=1
                        print("not present!!")
                        print(num, " ", row)
                        time.sleep(3)
    print("featureCollection: ", featureCollection["features"])
    print("Length of featureCollection: ", len(featureCollection["features"]))
    pickle.dump(featureCollection["features"], open("Data/datFiles/carbonMean.dat", "wb"))
    featureCollection["features"] = pickle.load(open("Data/datFiles/carbonMean.dat","rb"))

# fileOpen('Data\Carbon.csv')

#Creates Feature collection for the given pollution type  
def createFeatureCollec():
    featureCollection = {"type": "FeatureCollection", "features": []}
    featureCollection["features"] = pickle.load(open("Data/datFiles/carbonMean.dat", "rb"))
    print(featureCollection)
    file = open("Data\\JsFiles\\CurrentPollution\\carbonMeanCollection.js", "a")
    file.write(str(featureCollection))
    file.close()

# createFeatureCollec()


#Get the names of countys, cities, address in a state
def fileCheck(fileName): 
    addressDict= {'Arizona': [], 'California': [], 'Colorado': [], 'Florida': [], 'Illinois': [], 'Kansas': [], 'Kentucky': [], 'Louisiana': [], 'Michigan': [], 'Missouri': [], 'New Jersey': [], 'New York': [], 'North Carolina': [], 'Pennsylvania': [], 'Texas': [], 'Virginia': [], 'Massachusetts': [], 'Nevada': [], 'New Hampshire': [], 'Tennessee': [], 'South Carolina': [], 'Connecticut': [], 'Iowa': [], 'Maryland': [], 'Oklahoma': [], 'Wisconsin': [], 'Arkansas': [], 'Oregon': [], 'Wyoming': [], 'North Dakota': [], 'Ohio': []}
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile) # Reading the Carbon.csv file
        for row in reader:
            if row["State"] in addressDict.keys(): #Considering only 'State' from the complete address 
                address = row["Address"].replace(","," ") #Removing the comma from adresss replacing it with space
                if address not in addressDict[row["State"]]:
                    addressDict[row["State"]].append(address)
    # pickle.dump(addressDict, open("Data/AddressFiles/AddressInState.dat", "wb"))

# fileCheck('Data\Carbon.csv')