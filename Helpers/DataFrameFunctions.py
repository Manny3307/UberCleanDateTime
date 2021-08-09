from Helpers.ExceptionLogging import UberExceptionLogging
import json
import os, ntpath, sys, traceback
from shutil import copyfile
import glob
import pandas as pd
from datetime import datetime as dt, timedelta, time
import random

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

#Set the Upper and Lower Limit for Time Substraction
lower_time_range = 2
upper_time_range = 8 

class DataFrameFunction:

    def __init__(self) -> None:
        try:
            #Get the fields of the DataFrame from the Config File
            DataFrameConf = open('./Config/DataFrameConfig.json')
            global dataconf
            dataconf = json.load(DataFrameConf)
        except:
            objUberExceptionLogging.UberLogException(ExceptionMessages["Exceptions"]["Dataframe_config"], True, True)
    
        UberLogString.append(SuccessMessages["Messages"]["dataframe_config"])
    
        try:
            # Load the Config JSON file from the config folder and read the respective values
            ConfigJSON = open('./Config/config.json')
            ConfigData = json.load(ConfigJSON)

            # Get The Base Path from the Config File.
            global BasePath, HTMLHeaderTemplate, HTMLFooterTemplate, FinalHTMLResult, HTMLFolder, CSVFolder, DataFrameColumnsNames
            BasePath = ConfigData["configs"]["BasePath"]
            HTMLHeaderTemplate = ConfigData["configs"]["HTMLHeaderTemplate"]
            HTMLFooterTemplate = ConfigData["configs"]["HTMLFooterTemplate"]
            FinalHTMLResult = ConfigData["configs"]["FinalHTMLResult"]
            HTMLFolder = ConfigData["configs"]["HTMLFolder"]
            CSVFolder = ConfigData["configs"]["CSVFolder"]
            DataFrameColumnsNames = ConfigData["configs"]["DataFrameColumnsNames"]
        except:
            objUberExceptionLogging.UberLogException(ExceptionMessages["Exceptions"]["general_config"], True, True)

        UberLogString.append(SuccessMessages["Messages"]["general_config"])
    
    #Load the Date and Time Data from Uber Build folder to cleaning record destination CSV folder.
    def load_date_time_data(self, folderName):
        try:
            global cleaningfolderName
            cleaningfolderName = folderName
            UberCSVFiles = os.path.join(BasePath, cleaningfolderName, CSVFolder)
            # Read a single CSV file or multiple CSV files from the Given Folder.
            myfiles = glob.glob(f"{UberCSVFiles}/*.csv")

            # Get a DataFrame and assign the CSV to this DataFrame
            global UberTripData
            UberTripData = pd.DataFrame()
            TempUberTripData = pd.DataFrame()
            TempUberTripDataList = []

            # Read the CSV file(s) in the UberTripData DataFrame
            if myfiles != None:
                for myfile in myfiles:
                    csvfile = open(myfile) 
                    TempUberTripData = pd.read_csv(csvfile)
                    TempUberTripDataList.append(TempUberTripData)
                    
            # Get the Dump of Uber Date and Time data 
            UberTripData = pd.concat(TempUberTripDataList, axis=0, ignore_index=True)
        except:
            objUberExceptionLogging.UberLogException("ERROR: Date and Time Data cannot be loaded in the dataframe.", True, True)

        UberLogString.append("Date and Time Data successfully loaded in the dataframe.")

    #Calculate the clean time for Uber Trips
    def UberSplitDateTime(self, UberDateTime, TimeInMinutes):
        try:
            x = UberDateTime.split()
            UberTime = x[3]
            UberTime = dt.strptime(UberTime, '%H:%M')
            CleanTime = UberTime - timedelta(minutes = TimeInMinutes)
            FinalDateandCleanTime = x[0] + " " + x[1] + " " + x[2] + " " + CleanTime.strftime("%H:%M") + " " + x[4]
            return FinalDateandCleanTime 
        except:
            objUberExceptionLogging.UberLogException("ERROR: Date and Time are not in correct format.", True, True)

    #Create the final dataframe 
    def create_final_df(self, foldername):
        try:
            self.load_date_time_data(foldername)
            #Create a new DataFrame
            global final_df
            final_df = pd.DataFrame()
            
            #Apply UberSplitDateTime to Date and Time of Trip column.
            #Date and time of trip
            for (k, v) in dataconf.items():
                if v["IsEval"] == True:
                    if not v["IsDict"] == "false":
                        final_df[v["dfColumn"]] = eval(v["Value"],{'self':self, 'UberTripData':UberTripData, 'random':random, 'lower_time_range': lower_time_range, 'upper_time_range': upper_time_range})
                    else:
                        final_df[v["dfColumn"]] = eval(v["Value"])    
                else:
                    final_df[v["dfColumn"]] = v["Value"]
        except:
            objUberExceptionLogging.UberLogException("ERROR: Final DataFrame holding the Cleaning Records cannot be created.", True, True)
        
        return final_df

    UberLogString.append("Creating the final dataframe having all the required columns")
    
    #Rename the final dataframe columns 
    def rename_df_columns(self):
        try:
            #Update Column Names of the main Dataframe
            final_df.rename(columns=eval(DataFrameColumnsNames), inplace = True)  
        except:
            objUberExceptionLogging.UberLogException("ERROR: Column names in the Final Dataframe could not be updated, Please check DataFrameColumnsNames in config.json!!!", True, True) 

        UberLogString.append("Renaming the dataframe columns to one provided in the CPVV Template !!!")
        UberLogString.append("Rendering the dataframe to HTML!!!")

        return final_df

    #Return the DataFrameFunctions Log String for creating the log purposes.
    def get_DataFrameFuntions_LogString(self):
        return UberLogString