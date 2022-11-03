import string
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from datetime import datetime
import json
import enum

import Core.StorageManager.StorageManager as storage

class PageNames(enum.Enum):

    uniqueMessages = "УникальныеСообщения"
    onboarding = "Онбординг"

pages = PageNames


CREDENTIALS_FILE = 'creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
)
httpAuth = credentials.authorize(httplib2.Http())

service = build('sheets', 'v4', http = httpAuth)
service_drive = build('drive', 'v3', http = httpAuth)

spreadsheet_id = '1ZJ6VzQOQJlZvVtJ2UNhb8Uj4El2TV8lG7wMfMwMiJaM'

def getTableModifiedTime():
    response = service_drive.files().get(fileId=spreadsheet_id,fields="modifiedTime").execute()
    modified_time_str = response['modifiedTime']
    date = datetime.fromisoformat(modified_time_str[:-1])
    return date

def getContent(page: PageNames, range: string):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{page.value}!{range}',
        majorDimension='ROWS'
    ).execute()

    values = values['values']
    return values

def updateUniqueMessages():

    values = getContent(pages.uniqueMessages, "A1:B200")
    if len(values) > 0:
        del values[0]

    content = {}
    for line in values:
        if line[0] not in content and line[0] != "":
            content[line[0]] = line[1]

    storage.writeJsonData(
        storage.path.botContentUniqueMessages, 
        content
    )
    
def updateOnboarding():

    values = getContent(pages.onboarding, "A1:B100")
    if len(values) > 0:
        del values[0]

    content = []
    for line in values:
        content.append({
            "message": line[0],
            "buttonText": line[1]
        })

    storage.writeJsonData(
        storage.path.botContentOnboarding, 
        content
    )