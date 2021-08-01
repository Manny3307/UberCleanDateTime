
from numpy.lib.function_base import append
import pandas as pd
import glob
from datetime import datetime as dt, timedelta
from IPython.display import HTML
import pdfkit
import random
import json
import os, ntpath, sys, traceback
from shutil import copyfile
from sqlalchemy import create_engine, orm
import mysql.connector
import traceback, logging

filename = './Logs/UberLog.json'
now = dt.now()
dtLog_string = now.strftime("%d/%m/%Y %I-%M-%S %p")

UberLogData = {}
UberLogString = []

#Logs the Uber Program Exceptions
def UberLogException(UberExceptionString, UberProgExit, UberSystemExit):
     
    print(UberExceptionString)
    print(traceback.format_exc())
    if UberProgExit == True: print("Exiting the Program")

    UberLogString.append(UberExceptionString)
    UberLogString.append(traceback.format_exc())
    UberLogString.append("Exiting the Program")

    create_prog_log(UberLogString) # Send the exception to the UberLog.json Log File.

    if UberSystemExit == True: sys.exit()

#Create Logs in the program
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
try:
    FolderConfigJSON = open('./Config/folder_config.json')
    CreateConfigData = json.load(FolderConfigJSON)

    # Get The Base Path from the Config File.
    CreateBasePath = CreateConfigData["folder_configs"]["BasePath"]
    BuildPath = CreateConfigData["folder_configs"]["BuildPath"]
    CreateHTMLHeaderTemplate = CreateConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordHeader']
    CreateHTMLFooterTemplate = CreateConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordFooter']
    CreateHTMLFolder = CreateConfigData["folder_configs"]["HTMLFolder"]
    CreateCSVFolder = CreateConfigData["folder_configs"]["CSVFolder"]
except:
    UberLogException("ERROR: Cannot load the folder settings from folder_config.json!!!", True, True)

UberLogString.append("Folder settings from folder_config.json Loaded successfully.")

try:
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
    DataFrameColumnsNames = ConfigData["configs"]["DataFrameColumnsNames"]
except:
    UberLogException("ERROR: Cannot load the settings from config.json", True, True)

UberLogString.append("Config settings from config.json Loaded successfully.")

try:
    #Get the fields of the Database Configuration from the Config File
    DBConfig = open('./Config/DBConfig.json')
    dbconf = json.load(DBConfig)

    DBConnector = dbconf["DBConfigs"]["DBConnecter"]
    UserName = dbconf["DBConfigs"]["UserName"]
    Password = dbconf["DBConfigs"]["Password"]
    ServerOrEndPoint = dbconf["DBConfigs"]["ServerOrEndPoint"]
    DatabaseName = dbconf["DBConfigs"]["DatabaseName"]
except:
    UberLogException("ERROR: Cannot load the Database settings from DBconfig.json", True, True)

UberLogString.append("Database credentials from DBconfig.json Loaded successfully.")

try:
    #Get the fields of the DataFrame from the Config File
    DataFrameConf = open('./Config/DataFrameConfig.json')
    dataconf = json.load(DataFrameConf)
except:
    UberLogException("ERROR: Cannot load the Dataframe configurations from DataFrameConfig.json", True, True)

UberLogString.append("DataFrame configurations from DataFrameConfig.json Loaded successfully.")

UberLogString.append("All required configurations Loaded successfully.")

#Set the Upper and Lower Limit for Time Substraction
lower_time_range = 2
upper_time_range = 8 

# Get the Folder Name.
folderName = input("Please Enter the Folder Name: ")

#Create Folder Structure for the New Cleaning Record Fortnight
#Create Folder in "Uber Cleaning Record" directory for the given fortnight in the date format.

try:
    dirName = os.path.join(CreateBasePath, folderName)

    # Create target Directory
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created. ") 
        
        HTMLDirName = os.path.join(dirName, CreateHTMLFolder)
        #Create "HTML" directory
        if not os.path.exists(HTMLDirName):
            os.makedirs(HTMLDirName)
            print("Directory " , HTMLDirName ,  " Created. ")
        else:
            print("Directory " , HTMLDirName ,  " already exists.")  
        
        CSVDirName = os.path.join(dirName, CreateCSVFolder)
        #Create "CSV" directory
        if not os.path.exists(CSVDirName):
            os.makedirs(CSVDirName)
            print("Directory " , CSVDirName ,  " Created. ")
        else:
            print("Directory " , CSVDirName ,  " already exists.")      
    else:
        print("Directory " , dirName ,  " already exists.")  
except:
    UberLogException("ERROR: Folder structure cannot be created.", True, True)

UberLogString.append("Folder Structure created successfully.")

HTMLDirName = os.path.join(dirName, CreateHTMLFolder)
CSVDirName = os.path.join(dirName, CreateCSVFolder)

#Funtion to copy the template files in the respective folders
def copy_files_to_dest_folder(Templatefiles_src, DirName):
    try:
        if Templatefiles_src != None:
            for temp_files in Templatefiles_src:
                src_files = temp_files
                dest_files = os.path.join(DirName, ntpath.basename(temp_files))
                if not os.path.exists(dest_files):
                    copyfile(src_files, dest_files)
                    print("File " , dest_files ,  " copied successfully!!!")
                else:
                    print("File " , dest_files ,  " already exists")
    except:
        UberLogException("ERROR: File(s) cannot be copied in required folders.", True, True)

try:
    #Build the Path for HTML and CSV Folders.
    BuildHTMLPath = os.path.join(BuildPath, CreateHTMLFolder)
    BuildCSVPath = os.path.join(BuildPath, CreateCSVFolder)
    print(BuildHTMLPath)
    print(BuildCSVPath)

    #Copy the Required files to the created folders
    # Read a single HTML file or multiple HTML files from the Given Folder.
    HTMLTemplatefiles_src = glob.glob(f"{BuildHTMLPath}/*.html")
    CSVTemplatefiles_src = glob.glob(f"{BuildCSVPath}/*.csv")

    #Copy the HTML Template Files 
    copy_files_to_dest_folder(HTMLTemplatefiles_src, HTMLDirName)
    #Copy the CSV Files 
    copy_files_to_dest_folder(CSVTemplatefiles_src, CSVDirName)
except:
    UberLogException("ERROR: Required HTML and CSV file(s) cannot be copied in designated folders.", True, True)

UberLogString.append("CSV and HTML files copied successfully to the newly created designated folders.")

try:
    UberCSVFiles = os.path.join(BasePath, folderName, CSVFolder)
    # Read a single CSV file or multiple CSV files from the Given Folder.
    myfiles = glob.glob(f"{UberCSVFiles}/*.csv")

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
except:
    UberLogException("ERROR: Date and Time Data cannot be loaded in the dataframe.", True, True)

UberLogString.append("Date and Time Data successfully loaded in the dataframe.")

#Calculate the clean time for Uber Trips
def UberSplitDateTime(UberDateTime, TimeInMinutes):
    try:
        x = UberDateTime.split()
        UberTime = x[3]
        UberTime = dt.strptime(UberTime, '%H:%M')
        CleanTime = UberTime - timedelta(minutes = TimeInMinutes)
        FinalDateandCleanTime = x[0] + " " + x[1] + " " + x[2] + " " + CleanTime.strftime("%H:%M") + " " + x[4]
        return FinalDateandCleanTime 
    except:
        UberLogException("ERROR: Date and Time are not in correct format.", True, True)

#Get the Current path name to Name the PDF
def GetCurrentPathName():
    try:
        UberPDFCleaningRecord = os.path.join(BasePath, folderName)
        #CurrentUberCleaningRecordFolder = f"D:\\Uber Cleaning Record\\{folderName}"
        CompleteFileName = f"{UberPDFCleaningRecord}/Cleaning-record-{folderName}.pdf"
        return CompleteFileName
    except:
        UberLogException("ERROR: Cleaning record PDF file name cannot be correctly formed.", True, True)

try:
    #Create a new DataFrame
    final_df = pd.DataFrame()

    #Apply UberSplitDateTime to Date and Time of Trip column.
    #Date and time of trip
    for (k, v) in dataconf.items():
        if v["IsEval"] == True:
            final_df[v["dfColumn"]] = eval(v["Value"])
        else:
            final_df[v["dfColumn"]] = v["Value"]
except:
    UberLogException("ERROR: Final DataFrame holding the Cleaning Records cannot be created.", True, True)

UberLogString.append("Creating the final dataframe having all the required columns")

UberLogString.append("Connecting to Database")

TempTableCheck = True
try:
    # Create SQLAlchemy engine to connect to MySQL Database
    engine = create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}", encoding='utf8')

    UberLogString.append("Sending Records to UberTempCleaningRecords table in database....")
    print("Sending Records to database....")

    # Convert dataframe to sql table                                   
    final_df.to_sql('UberTempCleaningRecords', engine, if_exists='append', index=False)
except:
    TempTableCheck = False
    UberLogException("ERROR: Cleaning Records could not be sent to UberTempCleaningRecords.", False, False) 
finally:
    engine = None

if TempTableCheck == True:    
    UberLogString.append("Sending Records to UberCleaningRecords table through InsertJSONCleaningRecord stored procedure")

    # Create SQLAlchemy engine to connect to MySQL Database
    engine = create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}", encoding='utf8')

    sp_Check = True
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
    except:
        UberLogException("ERROR: Something went wrong while executing InsertJSONCleaningRecord. Please Check UberCleaningRecords table in the database", False, False) 
        sp_Check = False
    finally:
        connection.close() 

    #Print the message returned from the Stored Procedure
    print(results[0])
    UberLogString.append(results[0])

    if sp_Check == True: 
        print("Cleaning Records successfully sent to database !!!")
        UberLogString.append("Records successfully sent to UberCleaningRecords in database !!!")
    else:
        print("Failed to send Cleaning Records to database !!!")
        UberLogString.append("Failed to send Cleaning Records to database !!!")    

try:
    #Update Column Names of the main Dataframe
    final_df.rename(columns=eval(DataFrameColumnsNames), inplace = True)  
except:
    UberLogException("ERROR: Column names in the Final Dataframe could not be updated, Please check DataFrameColumnsNames in config.json!!!", True, True) 

UberLogString.append("Renaming the dataframe columns to one provided in the CPVV Template !!!")
UberLogString.append("Rendering the dataframe to HTML!!!")
try:
    #Convert data frame into a HTML table.
    BodyTemplate = final_df.to_html(classes='mystyle',index=False)

    TemplatePath = os.path.join(BasePath, folderName, HTMLFolder)
    #Load the header HTML Template
    HeaderTemplate = open(f"{TemplatePath}/{HTMLHeaderTemplate}").read()
    
    #Load the Footer HTML Template
    FooterTemplate = open(f"{TemplatePath}/{HTMLFooterTemplate}").read()

    #Concatenate all the templates into End Result to form one complete HTML
    EndResult = str(HeaderTemplate) + str(BodyTemplate) + str(FooterTemplate)
except:
    UberLogException("ERROR: Final HTML cannot be loaded and concatednated!!!", True, True) 

UberLogString.append("Concatenating the final HTML!!!")

try:
    #Assign EndResult to UberCleanTimeHTML.html file.
    UberDateTimeHTML = open(f"{TemplatePath}/{FinalHTMLResult}","w")
    UberDateTimeHTML.write(EndResult)
    UberDateTimeHTML.close()
except:
    UberLogException("ERROR: Final HTML cannot be loaded and concatednated!!!", True, True) 
finally:
    UberDateTimeHTML.close()

UberLogString.append("Saving the final HTML to HTML file in HTML Folder!!!")

UberLogString.append("Begin to write the PDF file from the resultant HTML!!!")

try:
    #Create PDF from UberCleanTimeHTML.html to upload into Uber Portal.
    pdfkit.from_file(f"{TemplatePath}/{FinalHTMLResult}", GetCurrentPathName())
except:
    UberLogException("ERROR: PDF file cannot be created, please check if the PDF file is already open!!!", True, True)

UberLogString.append("PDF written successfully from the resultant HTML file!!!")
create_prog_log(UberLogString)