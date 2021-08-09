#The file to Create the folder Structure of the new Cleaning Record Folder for Uber
import pandas as pd
import glob
from datetime import datetime as dt, timedelta
import json
import os, ntpath
from shutil import copyfile

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

# Get the Folder Name.
folderName = input("Please Enter the Folder Name: ")

#Create Folder Structure for the New Cleaning Record Fortnight
#Create Folder in "Uber Cleaning Record" directory for the given fortnight in the date format.

dirName = CreateBasePath + folderName
HTMLDirName = dirName + CreateHTMLFolder
CSVDirName = dirName + CreateCSVFolder


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

BuildHTMLPath = BuildPath + CreateHTMLFolder
BuildCSVPath = BuildPath + CreateCSVFolder

#Copy the Required files to the created folders
# Read a single HTML file or multiple HTML files from the Given Folder.
HTMLTemplatefiles_src = glob.glob(f"{BuildHTMLPath}*.html")
CSVTemplatefiles_src = glob.glob(f"{BuildCSVPath}*.csv")

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