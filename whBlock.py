import requests
import msal
import atexit
import os.path
import json
from requests.structures import CaseInsensitiveDict
import pyodbc
import pandas as pd
from connectpyse.service import ticket_notes_api, ticket_note,ticket,tickets_api
from connectpyse.schedule import schedule_entries_api,schedule_entry
from sqlalchemy import create_engine
import sqlalchemy as sa
import urllib
import doorKey as dk
config = dk.tangerine()

class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict()   
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 

params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                'Server='+(config['database']['Server'])+';'
                                'Database=SomeSchoolAssetMGMT;'
                                'UID='+(config['database']['UID'])+';'
                                'PWD='+(config['database']['PWD'])+';')

conn = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))


### SQL Query
staffTopsBlockquery = f"exec SomeSchoolAssetMGMT_2_0.Rep.uspNewStaffTerms"
staffTopsBlock = pd.read_sql(staffTopsBlockquery , conn)

### Create list of staff members that are being disabled
# list_a=[]
dict_a=my_dictionary()

# for i in staffTopsBlock['UserPrincipalName']:
#         list_a.append(i)

for u,d in zip(staffTopsBlock.UserPrincipalName,staffTopsBlock.EndDate):
        d = str(d)
        dict_a.add(u,d)



# list_a_joined= "\n".join(list_a)
dict_a_joined = '\n'.join(' TERMED '.join((key,val)) for (key,val) in dict_a.items())

print("Please see below for the staff members accounts that have been disabled.\n\n{}".format(dict_a_joined))




### Variables ###
TENANT_ID = config['tenant_id'] 
CLIENT_ID = config['client_id']
cwURL = 'https://api-na.myconnectwise.net/v2021_2/apis/3.0/'
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

budata = """{"accountEnabled": 'False'}}"""
buheaders= {'Accept': 'application/json', 'Authorization': 'Bearer '+result['access_token'], 'Content-Type': 'application/json'}
for u,d in dict_a.items(): 
    user = u
    print(user)
    # blockl = requests.patch(f'{ENDPOINT}/users/{user}', headers=buheaders, data=budata)
    # ubresult = requests.get(f'{ENDPOINT}/users/{user}?$select=accountEnabled', headers={'Authorization': 'Bearer ' + result['access_token']})
    # ubresult.raise_for_status()
    # print(blockl.text)
    # print(ubresult.text)


# ### Creation of ticket
# company_id = 22482 #the id of the company
# board_name = "SomeSchool Service" #the id of the board
# board_id = 29
# summary = 'GCA termed Staff Block List'
# resources = 'APerson'  #should match a cw username
# url = 'https://api-na.myconnectwise.net/v2021_3/apis/3.0/'
# auth = config["cwAUTH"]
# newTicket = ticket.Ticket(json_dict={
#         "company": {"id": "22482"},
#         "board": {"name": "SomeSchool Service"},
#         "summary":summary,
#                 "resources": resources})

# ct = tickets_api.TicketsAPI(url=url, auth=auth)
# new_ticket = ct.create_ticket(newTicket)
# tID = new_ticket.id
# print(tID)

# ### Assigns ticket
# itID = int(tID)
# assign_ticket = schedule_entries_api.ScheduleEntriesAPI(url=url, auth=auth)
# assigned = schedule_entry.ScheduleEntry({"objectId": itID, "member":{"identifier":"APerson"},"type": { "identifier": "S" },"ownerFlag": True})
# assign_ticket.create_schedule_entry(assigned)

# ### Creat a ticket note
# ticket_notes = ticket_notes_api.TicketNotesAPI(url=url, auth=auth, ticket_id=tID)
# note = ticket_note.TicketNote({"text":"Please see below for the staff members accounts that have been disabled.\n\n{}".format(list_a_joined), "detailDescriptionFlag": True, "internalAnalysisFlag": True ,"externalFlag": False})
# ticket_notes.create_ticket_note(note)







#############   DEBUG   ########################################################################################################################
# print(type(data))
# user = ""
# if 'access_token' in result:
#     print(user)
#     data = """{"accountEnabled": 'False'}}"""
#     headers= {'Accept': 'application/json', 'Authorization': 'Bearer '+result['access_token'], 'Content-Type': 'application/json'}
#     blockl = requests.patch(f'{ENDPOINT}/users/{user}', headers=headers, data=data)
#     result = requests.get(f'{ENDPOINT}/users/{user}?$select=accountEnabled', headers={'Authorization': 'Bearer ' + result['access_token']})
#     result.raise_for_status()
#     print(blockl.text)
#     print(result.text)
# else:
#     raise Exception('no access token in result')



