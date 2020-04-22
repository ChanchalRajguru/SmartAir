# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:54:07 2020

@author: Chanchal
"""

import numpy as np #Library for mathematical tools
import pandas as pd #Libary to import and manage datasets
# import matplotlib.pyplot as plt
from csvToJSON import avgValue


    
def dataCleaning():
    dataset = pd.read_csv("data\pollution_us_2000_2016.csv")

    mainCsv = dataset.iloc[:,0:9].values
    
    co2 = dataset.iloc[:,25:29].values  #Selecting the CO2 columns 

    # no2 = dataset.iloc[:,10:14].values #Selecting the NO2 columns 
    
    # ozone = dataset.iloc[:,15:19].values
    # so2 = dataset.iloc[:,20:24].values

    from sklearn.preprocessing import Imputer
    imputer = Imputer(missing_values = 'NaN', strategy= "mean", axis=0)

    #Taking care of missing data by using Average
    # from sklearn.impute import SimpleImputer

    # imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

    imputer = imputer.fit(co2[:,:])
    co2[:,:] = imputer.transform(co2[:,:])

    """ imputer = imputer.fit(no2[:,:])
    no2[:,:] = imputer.transform(no2[:,:])



    imputer = imputer.fit(ozone[:,:])
    ozone[:,:] = imputer.transform(ozone[:,:])

    imputer = imputer.fit(so2[:,:])
    so2[:,:] = imputer.transform(so2[:,:]) """
    
    #Creating the Main DataFrame
    mainDataFrame = pd.DataFrame(mainCsv) 
    mainDataFrame.columns = ["SerialNo", "State Code", "County Code", "Site Num", "Address","State","County","City","Date Local"]

    ######################
    ###Carbon-di-oxide####
    ######################

    #Making into a DataFrame for Carbon-di-oxide    
    coDataFrame = pd.DataFrame(co2) 
    coDataFrame.columns = ["CO2 Units","CO2 1st Max Value", "CO2 1st Max Hour", "CO2 AQI" ]

    #Concatenating the Carbon-di-oxide dataFrame 
    carbon = pd.concat([mainDataFrame,coDataFrame], axis=1)

    #Sending the Carbon-di-oxide dataFrame to CSV file
    # carbon.to_csv("data\Carbon.csv", sep='\t',index=False)
    # carbon.to_csv("data\Carbon.csv", sep='\t',index=False)
    
    
    
    avgValue('data\Carbon.csv')

    """ ######################
    ###Nitrogen Oxide####
    ######################

    #Making into a DataFrame for Nitrogen    
    noDataFrame = pd.DataFrame(no2) 
    noDataFrame.columns = ["NO2 Units","NO2 1st Max Value", "NO2 1st Max Hour", "NO2 AQI" ]


    #Concatenating the Nitrogen dataFrame 
    result = pd.concat([mainDataFrame,noDataFrame], axis=1)

    #Sending the Nitrogen dataFrame to CSV file
    result.to_csv("testMain.csv", sep='\t',)


    ######################
    ###     Ozone    ####
    ######################

    #Making into a DataFrame for Carbon-di-oxide    
    ozoneDataFrame = pd.DataFrame(ozone) 
    ozoneDataFrame.columns = ["O3 Units","O3 1st Max Value", "O3 1st Max Hour", "O3 AQI" ]

    #Concatenating the Carbon-di-oxide dataFrame 
    ozone3 = pd.concat([mainDataFrame,ozoneDataFrame], axis=1)

    #Sending the Carbon-di-oxide dataFrame to CSV file
    ozone3.to_csv("Ozone.csv", sep='\t',)


    ######################
    ### Sulfur dioxide ####
    ######################

    #Making into a DataFrame for Sulfur dioxide   
    sulfurDataFrame = pd.DataFrame(so2) 
    sulfurDataFrame.columns = ["SO2 Units","SO2 1st Max Value", "SO2 1st Max Hour", "SO2 AQI" ]

    #Concatenating the Sulfur dioxide dataFrame 
    sulfur = pd.concat([mainDataFrame,sulfurDataFrame], axis=1)

    #Sending the Sulfur dioxide dataFrame to CSV file
    sulfur.to_csv("Sulfur.csv", sep='\t',) """

# dataCleaning()    