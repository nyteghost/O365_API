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

# conn = pyodbc.connect(
#     'Driver={ODBC Driver 17 for SQL Server};'
#     'Server='+(config['Server'])+';'
#     'Database=GCAAssetMGMT;'
#     'UID='+(config['UID'])+';'
#     'PWD='+(config['PWD'])+';'
# )

# for i in range (0,100):
#     for attempt in range(3):
#         try:
#             cursor = conn.cursor()
#         except pyodbc.ProgrammingError as error:
#             print(error)
#             input("Not able to connect to Database.\nCheck VPN")
#         else:
#                 break
#     else:
#         print("failed")


# staffTopsquery = f"exec GCAAssetMGMT_2_0.Ship.uspStaffKitDeployPWsToReset"
# staffTops = pd.read_sql(staffTopsquery , conn)

TENANT_ID = config['tenant_id'] 
CLIENT_ID = config['client_id']

AUTHORITY = 'https://login.microsoftonline.com/' + TENANT_ID
ENDPOINT = 'https://graph.microsoft.com/v1.0'

SCOPES = [
    'Files.ReadWrite.All',
    'Sites.ReadWrite.All',
    'User.Read',
    'User.ReadBasic.All'
]

cache = msal.SerializableTokenCache()

if os.path.exists('token_cache.bin'):
    cache.deserialize(open('token_cache.bin', 'r').read())

atexit.register(lambda: open('token_cache.bin', 'w').write(cache.serialize()) if cache.has_state_changed else None)

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

accounts = app.get_accounts()
result = None
if len(accounts) > 0:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if result is None:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if 'user_code' not in flow:
        raise Exception('Failed to create device flow')

    print(flow['message'])

    result = app.acquire_token_by_device_flow(flow)

# for i in staffTops['Org_Secondary_Email']: 
#     user = i
#     print(user)
#     data = """{"passwordProfile": {"forceChangePasswordNextSignIn": 'TRUE'}}"""
#     headers= {'Accept': 'application/json', 'Authorization': 'Bearer '+result['access_token'], 'Content-Type': 'application/json'}
#     resp = requests.patch(f'{ENDPOINT}/users/{user}', headers=headers, data=data)

#     print(resp.status_code)


#user = "sca_resets@georgiacyber.online"
# data = """{"passwordProfile": {"forceChangePasswordNextSignIn": 'TRUE'}}"""
# headers= {'Accept': 'application/json', 'Authorization': 'Bearer '+result['access_token'], 'Content-Type': 'application/json'}
# resp = requests.patch(f'{ENDPOINT}/users/{user}', headers=headers, data=data)
# print(resp.status_code)


#############   DEBUG   ########################################################################################################################




user = "sca_resets@georgiacyber.online"
if 'access_token' in result:
    result = requests.get(f'{ENDPOINT}/users/{user}', headers={'Authorization': 'Bearer ' + result['access_token']})
    result.raise_for_status()
    print(result.json())
else:
    raise Exception('no access token in result')
