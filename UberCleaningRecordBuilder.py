from Helpers.ExceptionLogging import UberExceptionLogging
from Helpers.FolderFunctions import FolderFunction
from Helpers.DataFrameFunctions import DataFrameFunction
from Helpers.DatabaseFunctions import dbFunction
from Helpers.HTMLFunctions import HTMLFunctions
from Helpers.PDFFunctions import PDFFunctions

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

# Get the Folder Name.
folderName = input("Please Enter the Folder Name: ")

#Create an Instance of FolderFunctions Class
UberFolderFunction = FolderFunction()

#Create the Uber folder Structure and copy the required files in this folder structure
FolderLogString = UberFolderFunction.create_folder_structure(folderName)
UberLogString.append(FolderLogString)

#Create an Instance of DataFrameFunctions Class
UberDataFrameFuntion = DataFrameFunction()

#Get the Final DataFrame with all the data about Cleaning record for the fortnight.
final_df = UberDataFrameFuntion.create_final_df(folderName)
UberLogString.append(UberDataFrameFuntion.get_DataFrameFuntions_LogString())

#Send the records to database
datafunctions = dbFunction()
UberLogString.append(datafunctions.send_DB_records(final_df))

#Rename the Final DataFrame colums to match with CPVV standards
final_df = UberDataFrameFuntion.rename_df_columns()

#Get the HTML templates from the respective files and concatenate them to form one single HTML file.
HTMLfunc = HTMLFunctions()
UberLogString.append(HTMLfunc.HTML_template(final_df, folderName))

#Create the PDF for the final HTML formed in the HTML folder of the User provided Folder Name.
objPDFFunction = PDFFunctions()
UberLogString.append(objPDFFunction.create_PDF(folderName))

#Send the Final Log Uber Log file
objUberExceptionLogging.create_prog_log(UberLogString)