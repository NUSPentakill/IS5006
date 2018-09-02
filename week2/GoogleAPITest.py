from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
from GoogleSheetAPI import SpreadsheetSnippets as ss
import json



class GoogleAPITest():

    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        # Set spread sheet param
        self.SPREADSHEET_ID = '1XW8pwJuDs5SdisHkpsq7m5peU826mfpkZmSyRppUyCQ'
        self.store = file.Storage('token.json')
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            self.creds = tools.run_flow(flow, self.store)
        # Initialize Service
        service = build('sheets', 'v4', http=self.creds.authorize(Http()))
        self.ssAPI = ss(service)

    def readWriteGoogleSheet(self, updateRange, value=None):
        Value_input_option = 'USER_ENTERED'
        #read data from spreadsheet
        if value is None:
            result = self.ssAPI.get_values(self.SPREADSHEET_ID, updateRange)
            print(result)
        # write data into spreadsheet
        if value is not None:
            self.ssAPI.update_values(self.SPREADSHEET_ID, updateRange, Value_input_option, value)

    def appendGoogleSheet(self, value):
        Value_input_option = 'USER_ENTERED'
        updateRange = 'Sheet1'


        # read data from spreadsheet
        # ssAPI.get_values(SPREADSHEET_ID, RANGE_NAME)

        # write data into spreadsheet
        self.ssAPI.append_values(self.SPREADSHEET_ID, updateRange, Value_input_option, value)


if __name__ == '__main__':
    spreadsheet = GoogleAPITest()
    spreadsheet.readWriteGoogleSheet('D7')
