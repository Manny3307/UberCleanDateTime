from Helpers.ExceptionLogging import UberExceptionLogging
from sqlalchemy import create_engine, orm
import mysql.connector
import json

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

#Perform the database functions to send the data to database.
class dbFunction:
    
    def __init__(self):
        try:
            #Get the fields of the Database Configuration from the Config File
            DBConfig = open('./Config/DBConfig.json')
            dbconf = json.load(DBConfig)

            global DBConnector, UserName, Password, ServerOrEndPoint, DatabaseName
            DBConnector = dbconf["DBConfigs"]["DBConnecter"]
            UserName = dbconf["DBConfigs"]["UserName"]
            Password = dbconf["DBConfigs"]["Password"]
            ServerOrEndPoint = dbconf["DBConfigs"]["ServerOrEndPoint"]
            DatabaseName = dbconf["DBConfigs"]["DatabaseName"]
        except:
            objUberExceptionLogging.UberLogException(ExceptionMessages["Exceptions"]["Database_config"], True, True)

        UberLogString.append(SuccessMessages["Messages"]["database_config"])
        UberLogString.append("Connecting to Database")

    def send_DB_records(self, final_df):
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
            objUberExceptionLogging.UberLogException("ERROR: Cleaning Records could not be sent to UberTempCleaningRecords.", False, False) 
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
                objUberExceptionLogging.UberLogException("ERROR: Something went wrong while executing InsertJSONCleaningRecord. Please Check UberCleaningRecords table in the database", False, False) 
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
        
        return UberLogString