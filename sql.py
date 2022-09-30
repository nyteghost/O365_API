import requests
import msal
import atexit
import os.path
import json
from requests.structures import CaseInsensitiveDict
import pyodbc
import pandas as pd

with open('parameters.json', 'r') as f:
        config = json.load(f)


#print(sca_ascii)

conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server='+(config['Server'])+';'
    'Database=SomeSchoolAssetMGMT;'
    'UID='+(config['UID'])+';'
    'PWD='+(config['PWD'])+';'
)

for i in range (0,100):
    for attempt in range(3):
        try:
            cursor = conn.cursor()
        except pyodbc.ProgrammingError as error:
            print(error)
            input("Not able to connect to Database.\nCheck VPN")
        else:
                break
    else:
        print("failed")




staffTopsquery = f"exec db_denydatawriter.uspYesterdayStaffKits"
staffTops = pd.read_sql(staffTopsquery , conn)


print(staffTops)



