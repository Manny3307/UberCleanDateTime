import pandas as pd
import glob
from datetime import datetime as dt, timedelta
from IPython.display import HTML
import pdfkit
import random
import json

# Load the Config JSON file from the config folder and read the respective values
ConfigJSON = open('./Config/config.json')
ConfigData = json.load(ConfigJSON)

# Get The Base Path from the Config File.
BasePath = ConfigData["configs"]["BasePath"]
HTMLHeaderTemplate = ConfigData["configs"]["HTMLHeaderTemplate"]
HTMLFooterTemplate = ConfigData["configs"]["HTMLFooterTemplate"]
FinalHTMLResult = ConfigData["configs"]["FinalHTMLResult"]
HTMLFolder = ConfigData["configs"]["HTMLFolder"]
CSVFolder = ConfigData["configs"]["CSVFolder"]

#Set the Upper and Lower Limit for Time Substraction
lower_time_range = 2
upper_time_range = 8 

# Get the Folder Name.
folderName = input("Please Enter the Folder Name: ")

# Read a single CSV file or multiple CSV files from the Given Folder.
myfiles = glob.glob(f"{BasePath}{folderName}{CSVFolder}*.csv")

# Get a DataFrame and assign the CSV to this DataFrame
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

#Calculate the clean time for Uber Trips
def UberSplitDateTime(UberDateTime, TimeInMinutes):
    x = UberDateTime.split()
    UberTime = x[3]
    UberTime = dt.strptime(UberTime, '%H:%M')
    CleanTime = UberTime - timedelta(minutes = TimeInMinutes)
    FinalDateandCleanTime = x[0] + " " + x[1] + " " + x[2] + " " + CleanTime.strftime("%H:%M") + " " + x[4]
    return FinalDateandCleanTime 

#Get the Current path name to Name the PDF
def GetCurrentPathName():
    
    #CurrentUberCleaningRecordFolder = f"D:\\Uber Cleaning Record\\{folderName}"
    CompleteFileName = f"{BasePath}{folderName}\\Cleaning-record-{folderName}.pdf"
    return CompleteFileName

#Create a new DataFrame
final_df = pd.DataFrame()

#Apply UberSplitDateTime to Date and Time of Trip column.
#Date and time of trip
final_df["Date and time of trip"] = UberTripData["DateTimeTrip"]
final_df["Date and Time of clean"] = UberTripData["DateTimeTrip"].apply(lambda x: UberSplitDateTime(x, random.randint(lower_time_range,upper_time_range)))
final_df["Driver name"] = "Manmeet"
final_df["Driver certificate number"] = "DC631236" 
final_df["Passenger high-touch surfaces cleaned? (Y/N)"] = "Y"
final_df["Driver high-touch surfaces cleaned? (Y/N)"] = "Y"

#Convert data frame into a HTML table.
BodyTemplate = final_df.to_html(classes='mystyle',index=False)

#Load the header HTML Template
HeaderTemplate=open(f"{BasePath}{folderName}{HTMLFolder}{HTMLHeaderTemplate}").read()

#Load the Footer HTML Template
FooterTemplate=open(f"{BasePath}{folderName}{HTMLFolder}{HTMLFooterTemplate}").read()

#Concatenate all the templates into End Result to form one complete HTML
EndResult = str(HeaderTemplate) + str(BodyTemplate) + str(FooterTemplate)

#Assign EndResult to UberCleanTimeHTML.html file.
UberDateTimeHTML = open(f"{BasePath}{folderName}{HTMLFolder}{FinalHTMLResult}","w")
UberDateTimeHTML.write(EndResult)
UberDateTimeHTML.close()

#Create PDF from UberCleanTimeHTML.html to upload into Uber Portal.
pdfkit.from_file(f"{BasePath}{folderName}{HTMLFolder}{FinalHTMLResult}", GetCurrentPathName())