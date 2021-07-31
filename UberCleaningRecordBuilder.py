from IPython.core.display import ProgressBar
from numpy.lib.function_base import append
import pandas as pd
import glob
from datetime import datetime as dt, timedelta
from IPython.display import HTML
import pdfkit
import random
import json
import os, ntpath
from shutil import copyfile
from sqlalchemy import create_engine, orm
import mysql.connector
import traceback

filename = './Logs/UberLog.json'
now = dt.now()
dtLog_string = now.strftime("%d/%m/%Y %H-%M-%S")

UberLogData = {}
dateString = {}

UberLogString = [dtLog_string]

def create_prog_log(logString):
    progLog = logString

    UberLogData["UberDateLog"] = dtLog_string
    UberLogData["UberLogs"] = logString

    with open(filename, "r+") as file:
        data = json.load(file)
        data.append(UberLogData)
        file.seek(0)
        json.dump(data, file, indent=1)
    
# Load the Config JSON file from the config folder and read the respective values
FolderConfigJSON = open('./Config/folder_config.json')
CreateConfigData = json.load(FolderConfigJSON)

# Get The Base Path from the Config File.
CreateBasePath = CreateConfigData["folder_configs"]["BasePath"]
BuildPath = CreateConfigData["folder_configs"]["BuildPath"]
CreateHTMLHeaderTemplate = CreateConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordHeader']
CreateHTMLFooterTemplate = CreateConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordFooter']
CreateHTMLFolder = CreateConfigData["folder_configs"]["HTMLFolder"]
CreateCSVFolder = CreateConfigData["folder_configs"]["CSVFolder"]

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
DataFrameColumnValues = ConfigData["configs"]["DataFrameColumnsValues"]

#Get the fields of the DataFrame from the Config File
DataFrameConf = open('./Config/DataFrameConfig.json')
dataconf = json.load(DataFrameConf)

#Get the fields of the Database Configuration from the Config File
DBConfig = open('./Config/DBConfig.json')
dbconf = json.load(DBConfig)

DBConnector = dbconf["DBConfigs"]["DBConnecter"]
UserName = dbconf["DBConfigs"]["UserName"]
Password = dbconf["DBConfigs"]["Password"]
ServerOrEndPoint = dbconf["DBConfigs"]["ServerOrEndPoint"]
DatabaseName = dbconf["DBConfigs"]["DatabaseName"]

UberLogString.append("Configurations Loaded successfully")
#create_prog_log("Configurations Loaded successfully")

#Set the Upper and Lower Limit for Time Substraction
lower_time_range = 2
upper_time_range = 8 

# Get the Folder Name.
folderName = input("Please Enter the Folder Name: ")

#Create Folder Structure for the New Cleaning Record Fortnight
#Create Folder in "Uber Cleaning Record" directory for the given fortnight in the date format.

dirName = CreateBasePath + folderName
HTMLDirName = dirName + CreateHTMLFolder
CSVDirName = dirName + CreateCSVFolder

UberLogString.append("Creating folder successfully")

# Create target Directory
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory " , dirName ,  " Created ") 
    
    #Create "HTML" directory
    if not os.path.exists(HTMLDirName):
        os.makedirs(HTMLDirName)
        print("Directory " , HTMLDirName ,  " Created ")
    else:
        print("Directory " , HTMLDirName ,  " already exists")  
    
    #Create "CSV" directory
    if not os.path.exists(CSVDirName):
        os.makedirs(CSVDirName)
        print("Directory " , CSVDirName ,  " Created ")
    else:
        print("Directory " , CSVDirName ,  " already exists")      
else:
    print("Directory " , dirName ,  " already exists")   

UberLogString.append("Folder Structure created successfully")

BuildHTMLPath = BuildPath + CreateHTMLFolder
BuildCSVPath = BuildPath + CreateCSVFolder

#Copy the Required files to the created folders
# Read a single HTML file or multiple HTML files from the Given Folder.
HTMLTemplatefiles_src = glob.glob(f"{BuildHTMLPath}*.html")
CSVTemplatefiles_src = glob.glob(f"{BuildCSVPath}*.csv")

#Funtion to copy the template files in the respective folders
def copy_files_to_dest_folder(Templatefiles_src, DirName):
    if Templatefiles_src != None:
        for temp_files in Templatefiles_src:
            src_files = temp_files
            dest_files = DirName + ntpath.basename(temp_files)
            if not os.path.exists(dest_files):
                copyfile(src_files, dest_files)
                print("File " , dest_files ,  " copied successfully!!!")
            else:
                print("File " , dest_files ,  " already exists")
    
#Copy the HTML Template Files 
copy_files_to_dest_folder(HTMLTemplatefiles_src, HTMLDirName)
#Copy the CSV Files 
copy_files_to_dest_folder(CSVTemplatefiles_src, CSVDirName)

UberLogString.append("CSV and HTML files copied successfully to the newly created folders")

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

UberLogString.append("Date and Time Data successfully loaded in the dataframe")

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
for (k, v) in dataconf.items():
    if v["IsEval"] == True:
        final_df[v["dfColumn"]] = eval(v["Value"])
    else:
        final_df[v["dfColumn"]] = v["Value"]

UberLogString.append("Creating the final dataframe having all the required columns")

UberLogString.append("Connecting to Database")
# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}", encoding='utf8')

UberLogString.append("Sending Records to UberTempCleaningRecords table in database....")
print("Sending Records to database....")

# Convert dataframe to sql table                                   
final_df.to_sql('UberTempCleaningRecords', engine, if_exists='append', index=False)

UberLogString.append("Sending Records to UberCleaningRecords table through InsertJSONCleaningRecord stored procedure")
connection = engine.raw_connection()
# define parameters to be passed in and out
parameterIn = None
parameterOut = "@parameterOut"
try:
    cursor = connection.cursor()
    results = cursor.callproc("InsertJSONCleaningRecord", [parameterOut])
    # fetch result parameters
    cursor.close()
    connection.commit()
finally:
    connection.close() 

#Print the message returned from the Stored Procedure
print(results[0])
UberLogString.append(results[0])

print("Records successfully sent to database !!!")
UberLogString.append("Records successfully sent to UberCleaningRecords in database !!!")


#Update Column Names of the main Dataframe
final_df.rename(columns=eval(DataFrameColumnValues), inplace = True)  

UberLogString.append("Renaming the dataframe columns to one provided in the CPVV Template !!!")

UberLogString.append("Rendering the dataframe to HTML!!!")

#Convert data frame into a HTML table.
BodyTemplate = final_df.to_html(classes='mystyle',index=False)

#Load the header HTML Template
HeaderTemplate=open(f"{BasePath}{folderName}{HTMLFolder}{HTMLHeaderTemplate}").read()

#Load the Footer HTML Template
FooterTemplate=open(f"{BasePath}{folderName}{HTMLFolder}{HTMLFooterTemplate}").read()

#Concatenate all the templates into End Result to form one complete HTML
EndResult = str(HeaderTemplate) + str(BodyTemplate) + str(FooterTemplate)

UberLogString.append("Concatenating the final HTML!!!")

#Assign EndResult to UberCleanTimeHTML.html file.
UberDateTimeHTML = open(f"{BasePath}{folderName}{HTMLFolder}{FinalHTMLResult}","w")
UberDateTimeHTML.write(EndResult)
UberDateTimeHTML.close()

UberLogString.append("Saving the final HTML to HTML file in HTML Folder!!!")

UberLogString.append("Begin to write the PDF file from the resultant HTML!!!")

#Create PDF from UberCleanTimeHTML.html to upload into Uber Portal.
pdfkit.from_file(f"{BasePath}{folderName}{HTMLFolder}{FinalHTMLResult}", GetCurrentPathName())

UberLogString.append("PDF written successfully from the resultant HTML file!!!")
create_prog_log(UberLogString)
