from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
from GoogleSheetAPI import SpreadsheetSnippets as ss
import json



class GoogleAPITest():

    def __init__(self):
        pass

    def main(self):
        # Initialize
        # If modifying these scopes, delete the file token.json.
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        store = file.Storage('token.json')
        workdir = os.getcwd()
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)

        # Initialize Service
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        ssAPI = ss(service)

        # Set spread sheet param
        SPREADSHEET_ID = '1XW8pwJuDs5SdisHkpsq7m5peU826mfpkZmSyRppUyCQ'
        RANGE_NAME = 'A:C'
        UPDATE_RANGE = 'D1:E4'
        Value_input_option = 'USER_ENTERED'
        value = [
            ['Value', 'Comment'],
            ['11', 'test'],
            ['13', 'test'],
            ['15', 'test']
        ]

        # read data from spreadsheet
        ssAPI.get_values(SPREADSHEET_ID, RANGE_NAME)

        # write data into spreadsheet
        ssAPI.update_values(SPREADSHEET_ID, UPDATE_RANGE, Value_input_option, value)


if __name__ == '__main__':
    spreadsheet = GoogleAPITest()
    spreadsheet.main()
