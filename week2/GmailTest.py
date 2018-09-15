from __future__ import print_function

# Importing required libraries
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

from GmailAPIHelper import GmailSnippets as gm

# Creating a storage.JSON file with authentication details
# SCOPES = 'https://www.googleapis.com/auth/gmail.compose'  # we are using modify and not readonly, as we will be marking the messages Read
SCOPES = "https://mail.google.com/"


class GmailTest():

    def __init__(self):
        store = file.Storage('token_gmail.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials_gmail.json', SCOPES)
            creds = tools.run_flow(flow, store)
        # Initialize Service
        GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
        self.gmAPI = gm(GMAIL)

    def ParseUnreadEmailData(self):
        finalList = self.gmAPI.getUnreadEmail()
        print(finalList)

        print(finalList[0]['Snippet'])
        return finalList[0]['Snippet']

    def CreateAndSendParsedData(self, data):
        response = self.gmAPI.create_message("lydiacm1123@gmail.com", "E0146244@U.NUS.EDU", "Profitable Company", data)
        self.gmAPI.SendMessage("lydiacm1123@gmail.com", response)


if __name__ == '__main__':
    gm = GmailTest()
    data = gm.ParseUnreadEmailData()
    gm.CreateAndSendParsedData(data)
