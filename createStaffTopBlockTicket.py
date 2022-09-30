import requests
import json
from connectpyse.service import tickets_api, ticket, ticket_notes_api, ticket_note
from connectpyse.schedule import schedule_entries_api,schedule_entry
from requests.structures import CaseInsensitiveDict
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import sqlalchemy as sa
import urllib
import doorKey as dk
config = dk.tangerine()

params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                'Server='+(config['database']['Server'])+';'
                                'Database=GCAAssetMGMT;'
                                'UID='+(config['database']['UID'])+';'
                                'PWD='+(config['database']['PWD'])+';')

conn = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))


### SQL Query
staffTopsBlockquery = f"exec SomeSchoolAssetMGMT_2_0.Rep.uspNewStaffTerms"
staffTopsBlock = pd.read_sql(staffTopsBlockquery , conn)

### Create list of staff members that are being disabled
list_a=[]
for i in staffTopsBlock['UserPrincipalName']:
        list_a.append(i)
list_a= "\n".join(list_a)

### Creation of ticket
company_id = 22482 #the id of the company
board_name = "SomeSchool Service" #the id of the board
board_id = 29
summary = 'This is a test of the API broadcast system'
resources = 'MBrown'  #should match a cw username
url = 'https://api-na.myconnectwise.net/v2021_3/apis/3.0/'
auth = config["cwAUTH"]
newTicket = ticket.Ticket(json_dict={
        "company": {"id": "22482"},
        "board": {"name": "SomeSchool Service"},
        "summary":summary,
                "resources": resources})

ct = tickets_api.TicketsAPI(url=url, auth=auth)
new_ticket = ct.create_ticket(newTicket)
tID = new_ticket.id
print(tID)

### Assigns ticket
itID = int(tID)
assign_ticket = schedule_entries_api.ScheduleEntriesAPI(url=url, auth=auth)
assigned = schedule_entry.ScheduleEntry({"objectId": itID, "member":{"identifier":"APerson"},"type": { "identifier": "S" },"ownerFlag": True})
assign_ticket.create_schedule_entry(assigned)

### Creat a ticket note
ticket_notes = ticket_notes_api.TicketNotesAPI(url=url, auth=auth, ticket_id=tID)
note = ticket_note.TicketNote({"text":"Please see below for the staff members accounts that have been disabled. This is a test and they have not been blocked yet.\n\n{}".format(list_a), "detailDescriptionFlag": True, "internalAnalysisFlag": True ,"externalFlag": False})
ticket_notes.create_ticket_note(note)


################# REQUESTS Version #######################################################################################
# url = "https://api-na.myconnectwise.net/v2021_3/apis/3.0/service/tickets"

# payload = json.dumps({
#   "summary": "This is a test of the API broadcast system",
#   "company": {
#     "id": "22482"
#   },
#   "board": {
#     "name": "SomeSchool Service"
#   },
#   "resources": "MBrown"
# })

# response = requests.request("POST", url, headers=config['ticketHeaders'], data=payload)

# print(response.text)
