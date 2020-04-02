import csv
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pickle
import time
import statistics
import re
import pymongo


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
    csvList = [] #Stores all csv data in form of List of Dicts
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
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["State"] in addressDict.keys():
                address = row["Address"].replace(","," ")
                if address not in addressDict[row["State"]]:
                    addressDict[row["State"]].append(address)
    # pickle.dump(addressDict, open("Data/AddressFiles/AddressInState.dat", "wb"))

# fileCheck('Data\Carbon.csv')

def avgValue(fileName):
    pollutantDict= {'Arizona': [], 'California': [], 'Colorado': [], 'Florida': [], 'Illinois': [], 'Kansas': [], 'Kentucky': [], 'Louisiana': [], 'Michigan': [], 'Missouri': [], 'New Jersey': [], 'New York': [], 'North Carolina': [], 'Pennsylvania': [], 'Texas': [], 'Virginia': [], 'Massachusetts': [], 'Nevada': [], 'New Hampshire': [], 'Tennessee': [], 'South Carolina': [], 'Connecticut': [], 'Iowa': [], 'Maryland': [], 'Oklahoma': [], 'Wisconsin': [], 'Arkansas': [], 'Oregon': [], 'Wyoming': [], 'North Dakota': [], 'Ohio': []}
    avgDict = {}
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["State"] in pollutantDict.keys():
                maxHour = int(row["SO2 1st Max Hour"])
                if maxHour != 0:
                    pollutantDict[row["State"]].append(maxHour)
        for key in pollutantDict:
            avgDict[key] = statistics.mean(pollutantDict[key])
    print(avgDict)

# avgValue('Data/Sulfur.csv')
