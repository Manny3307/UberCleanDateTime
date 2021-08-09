import traceback, logging
import json
from datetime import datetime as dt, timedelta, time
import sys, os.path

UberLogData = {}
UberLogString = []
filename = ""
now = dt.now()
dtLog_string = now.strftime("%d/%m/%Y %I-%M-%S %p")


class UberExceptionLogging:

    def __init__(self):
        self.create_check_new_log_file()


    #Load the KnownException.json and SuccessMessages.json to a dictionary
    def load_exception_success(self, exception_or_success):
        if(exception_or_success == "Exception"):
            ExceptionOrSuccessJSON = open('./Config/KnownExceptions.json')
        else:
            ExceptionOrSuccessJSON = open('./Config/SuccessMessages.json')
            
        CreateConfigData = json.load(ExceptionOrSuccessJSON)

        return CreateConfigData


    #Create new Log file for every day
    def create_check_new_log_file(self):
        global filename
        Logfile = f"./Logs/UberLog_{now.strftime('%d_%m_%Y')}.json"
        if not (os.path.exists(Logfile)):
            with open(Logfile,'w') as fp:
                fp.write("[]")
                filename = Logfile
        else:
            filename = Logfile

    #Create Logs in the program
    def create_prog_log(self, logString):
        progLog = logString

        UberLogData["UberDateLog"] = dtLog_string
        UberLogData["UberLogs"] = logString

        with open(filename, "r+") as file:
            data = json.load(file)
            data.append(UberLogData)
            file.seek(0)
            json.dump(data, file, indent=1)

    
    #Logs the Uber Program Exceptions
    def UberLogException(self, UberExceptionString, UberProgExit, UberSystemExit):
     
        print(UberExceptionString)
        print(traceback.format_exc())
        if UberProgExit == True: print("Exiting the Program")

        UberLogString.append(UberExceptionString)
        UberLogString.append(traceback.format_exc())
        UberLogString.append("Exiting the Program")

        self.create_prog_log(UberLogString) # Send the exception to the UberLog.json Log File.

        if UberSystemExit == True: sys.exit()