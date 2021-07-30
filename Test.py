import json
import os,sys
import pandas as pd
from datetime import datetime as dt, timedelta
import random
import ast
from sqlalchemy import create_engine


f = open('./Config/config.json')
data = json.load(f)

#print(data["configs"]["BasePath"])
#print(data["configs"]["HTMLHeaderTemplate"])

f.close()
#print(os.name)
#print(sys.platform)

FolderConfigJSON = open('./Config/folder_config.json')
ConfigData = json.load(FolderConfigJSON)

#HTMLFilestoCopy = ConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordHeader']
#print(f"Uber Cleaning Header Template = {HTMLFilestoCopy}")

#Set the Upper and Lower Limit for Time Substraction
lower_time_range = 2
upper_time_range = 8 

#Calculate the clean time for Uber Trips
def UberSplitDateTime(UberDateTime, TimeInMinutes):
    x = UberDateTime.split()
    UberTime = x[3]
    UberTime = dt.strptime(UberTime, '%H:%M')
    CleanTime = UberTime - timedelta(minutes = TimeInMinutes)
    FinalDateandCleanTime = x[0] + " " + x[1] + " " + x[2] + " " + CleanTime.strftime("%H:%M") + " " + x[4]
    return FinalDateandCleanTime 

#print(UberSplitDateTime("July 9, 2021 05:10 PM",5))

#df = pd.read_csv("./CSV/UberTripData.csv")
#print(df.head(5))

#df1 = pd.DataFrame()


DataFrameConf = open('./Config/DataFrameConfig.json')
dataconf = json.load(DataFrameConf)

#for (k, v) in dataconf.items():
#    if v["IsEval"] == True:
#        df1[v["dfColumn"]] = eval(v["Value"])
#    else:
#        df1[v["dfColumn"]] = v["Value"]


#print(df1)
#df1.to_csv("test.csv",index=False)
   
import mysql.connector
   

# Usefull Code 
# Credentials to database connection
hostname="manny-uber-records.cwl0oxqn3sec.us-east-2.rds.amazonaws.com"
dbname="manny_uber_records_2021"
uname="admin"
pwd="pikolo486"

# Create dataframe
df = pd.DataFrame(data=[[111,'Thomas','35','United Kingdom'],
		[222,'Ben',42,'Australia'],
		[333,'Harry',28,'India']],
		columns=['id','name','age','country'])

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+mysqlconnector://admin:pikolo486@manny-uber-records.cwl0oxqn3sec.us-east-2.rds.amazonaws.com/manny_uber_records_2021")

# Convert dataframe to sql table                                   
df.to_sql('users', engine, index=False)

import pandas as pd
from sqlalchemy import create_engine
 
# set your parameters for the database
user = "user"
password = "password"
host = "abc.efg.hij.rds.amazonaws.com"
port = 3306
schema = "db_schema"
 
# Connect to the database
conn_str = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4'.format(
    user, password, host, port, schema)
db = create_engine(conn_str, encoding='utf8')
connection = db.raw_connection()
 
# define parameters to be passed in and out
parameterIn = 1
parameterOut = "@parameterOut"
try:
    cursor = connection.cursor()
    cursor.callproc("storedProcedure", [parameterIn, parameterOut])
    # fetch result parameters
    results = list(cursor.fetchall())
    cursor.close()
    connection.commit()
finally:
    connection.close() 