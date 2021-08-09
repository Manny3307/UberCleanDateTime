from Helpers.ExceptionLogging import UberExceptionLogging
import json
import os, ntpath, sys, traceback
from shutil import copyfile
import glob
import pandas as pd
from datetime import datetime as dt, timedelta, time

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

class HTMLFunctions:
    
    def __init__(self):
        try:
            # Load the Config JSON file from the config folder and read the respective values
            ConfigJSON = open('./Config/config.json')
            ConfigData = json.load(ConfigJSON)

            # Get The Base Path from the Config File.
            global BasePath, HTMLHeaderTemplate, HTMLFooterTemplate, FinalHTMLResult, HTMLFolder, CSVFolder
            BasePath = ConfigData["configs"]["BasePath"]
            HTMLHeaderTemplate = ConfigData["configs"]["HTMLHeaderTemplate"]
            HTMLFooterTemplate = ConfigData["configs"]["HTMLFooterTemplate"]
            FinalHTMLResult = ConfigData["configs"]["FinalHTMLResult"]
            HTMLFolder = ConfigData["configs"]["HTMLFolder"]
            CSVFolder = ConfigData["configs"]["CSVFolder"]
        except:
            objUberExceptionLogging.UberLogException(ExceptionMessages["Exceptions"]["general_config"], True, True)

        UberLogString.append(SuccessMessages["Messages"]["general_config"])

    #Load HTML Templates and concatenate them into one single HTML file
    def HTML_template(self, final_df, folderName):
        try:
            #Convert data frame into a HTML table.
            BodyTemplate = final_df.to_html(classes='mystyle',index=False)
            global TemplatePath
            TemplatePath = os.path.join(BasePath, folderName, HTMLFolder)
            #Load the header HTML Template
            HeaderTemplate = open(f"{TemplatePath}/{HTMLHeaderTemplate}").read()
            
            #Load the Footer HTML Template
            FooterTemplate = open(f"{TemplatePath}/{HTMLFooterTemplate}").read()

            #Concatenate all the templates into End Result to form one complete HTML
            global EndResult
            EndResult = str(HeaderTemplate) + str(BodyTemplate) + str(FooterTemplate)
        except:
            objUberExceptionLogging.UberLogException("ERROR: Final HTML cannot be loaded and concatenated!!!", True, True) 

        UberLogString.append("Concatenating the final HTML!!!")
        
        self.save_HTML_file()

        return UberLogString

    #Save the End Result HTML created
    def save_HTML_file(self):
        try:
            #Assign EndResult to UberCleanTimeHTML.html file.
            UberDateTimeHTML = open(f"{TemplatePath}/{FinalHTMLResult}","w")
            UberDateTimeHTML.write(EndResult)
            UberDateTimeHTML.close()
        except:
            objUberExceptionLogging.UberLogException("ERROR: Final HTML cannot be loaded and concatednated!!!", True, True) 
        finally:
            UberDateTimeHTML.close()

        UberLogString.append("Saving the final HTML to HTML file in HTML Folder!!!")