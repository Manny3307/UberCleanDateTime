from Helpers.ExceptionLogging import UberExceptionLogging
import json
import os, ntpath, sys, traceback
from shutil import copyfile
import glob

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

HTMLDirName = ""
CSVDirName = ""


class FolderFunction:

    def __init__(self):
        # Load the Config JSON file from the config folder and read the respective values
        try:
            FolderConfigJSON = open('./Config/folder_config.json')
            CreateConfigData = json.load(FolderConfigJSON)

            # Get The Base Path from the Config File.
            global CreateBasePath, BuildPath, CreateHTMLHeaderTemplate, CreateHTMLFooterTemplate, CreateHTMLFolder, CreateCSVFolder
            CreateBasePath = CreateConfigData["folder_configs"]["BasePath"]
            BuildPath = CreateConfigData["folder_configs"]["BuildPath"]
            CreateHTMLHeaderTemplate = CreateConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordHeader']
            CreateHTMLFooterTemplate = CreateConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordFooter']
            CreateHTMLFolder = CreateConfigData["folder_configs"]["HTMLFolder"]
            CreateCSVFolder = CreateConfigData["folder_configs"]["CSVFolder"]
        except:
            objUberExceptionLogging.UberLogException(ExceptionMessages["Exceptions"]["folder_config"], True, True)

        UberLogString.append(SuccessMessages["Messages"]["folder_config"])    

    #Create Folder Structure for the New Cleaning Record Fortnight
    #Create Folder in "Uber Cleaning Record" directory for the given fortnight in the date format.
    def walk(self,folderDict, path):
        paths = []

        # we only continue if the value is not None
        if folderDict:
            for folder, subDict in folderDict.items():

                # making sure the path will have forward slashes
                # especially necessary on windows
                pathTemp = os.path.normpath(os.path.join(path, folder))
                pathTemp = pathTemp.replace("\\", "/")

                #add the current found path to the list
                paths.append(pathTemp)

                # we call the the function again to go deeper
                # in the dictionary
                paths.extend(self.walk(subDict, pathTemp))


        return paths

    #Check if all the folders are created properly or not.
    def checkFolderStructure(self, folderPaths):
        foldernotcreated = []
        
        for folder in folderPaths:
            if os.path.exists(folder) == False:
                foldernotcreated.append(folder) 
        
        return foldernotcreated

    #Create Folder Structure for the New Cleaning Record Fortnight
    #Create Folder in "Uber Cleaning Record" directory for the given fortnight in the date format.
    def create_folder_structure(self, folderName):
        check_for_error = False
        try:
            path = "./Config/FolderStructure.json"
            folders = {}
            replaced_folder = {}
            with open(path, 'r') as f:
                folders = json.load(f)

            replaced_folder[folderName] = folders["folder_name"]
            folderPaths = self.walk(replaced_folder, CreateBasePath)
            
            for folder_name in folderPaths:
                if not (os.path.exists(folder_name)):
                    os.makedirs(folder_name)
                    print(f"Folder {ntpath.basename(folder_name)} created successfully!!!")
                else:
                    print(f"Folder {ntpath.basename(folder_name)} already exists!!!")

            folderlist = self.checkFolderStructure(folderPaths)
            

            if not folderlist:
                print("Folder Structure Created Successfully!!!")
            else:
                check_for_error = True
                print("Folder Structure failed the configuration!!!")
                print("Following Folder(s) not present in the folder structure!!!")
                print("==========================================================")
                print(folderlist)
                print("ERROR: Folder structure cannot be created.")
                print("Exiting the Program!!!")
                UberLogString.append("Folder Structure failed the configuration!!!")
                sys.exit()

        except:
            check_for_error = True
            objUberExceptionLogging.UberLogException("ERROR: Folder structure cannot be created.", True, True)

        if check_for_error == False:
            try:
                #Build the Path for HTML and CSV Folders.
                BuildHTMLPath = os.path.join(BuildPath, CreateHTMLFolder)
                BuildCSVPath = os.path.join(BuildPath, CreateCSVFolder)

                #Copy the Required files to the created folders
                # Read a single HTML file or multiple HTML files from the Given Folder.
                HTMLTemplatefiles_src = glob.glob(f"{BuildHTMLPath}/*.html")
                CSVTemplatefiles_src = glob.glob(f"{BuildCSVPath}/*.csv")
                global HTMLDirName, CSVDirName
                dirName = os.path.join(CreateBasePath, folderName)
                HTMLDirName = os.path.join(dirName, CreateHTMLFolder)
                CSVDirName = os.path.join(dirName, CreateCSVFolder)

                #Copy the HTML Template Files 
                self.copy_files_to_dest_folder(HTMLTemplatefiles_src, HTMLDirName)
                #Copy the CSV Files 
                self.copy_files_to_dest_folder(CSVTemplatefiles_src, CSVDirName)
            except:
                objUberExceptionLogging.UberLogException("ERROR: Required HTML and CSV file(s) cannot be copied in designated folders.", True, True)

        UberLogString.append("CSV and HTML files copied successfully to the newly created designated folders.")
        UberLogString.append("Folder Structure created successfully.")
        
        return UberLogString

    #Funtion to copy the template files in the respective folders
    def copy_files_to_dest_folder(self, Templatefiles_src, DirName):
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
            objUberExceptionLogging.UberLogException("ERROR: File(s) cannot be copied in required folders.", True, True)