'''
Reading GMAIL using Python
	- Abhishek Chhibber
'''

'''
This script does the following:
- Go to Gmal inbox
- Find and read all the unread messages
- Extract details (Date, Sender, Subject, Snippet, Body) and export them to a .csv file / DB
- Mark the messages as Read - so that they are not read again 
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret.json should be saved in the same directory as this file
'''

import base64
from email import MIMEText
from email.mime.text import MIMEText

import dateutil.parser as parser
# Importing required libraries
from bs4 import BeautifulSoup


class GmailSnippets(object):

    def __init__(self, service):
        self.service = service

    def getUnreadEmail(self):

        user_id = 'me'
        label_id_one = 'INBOX'
        label_id_two = 'UNREAD'

        # Getting all the unread messages from Inbox
        # labelIds can be changed accordingly
        unread_msgs = self.service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

        # We get a dictonary. Now reading values for the key 'messages'
        mssg_list = unread_msgs['messages']

        print ("Total unread messages in inbox: ", str(len(mssg_list)))

        final_list = []

        for mssg in mssg_list:
            temp_dict = {}
            m_id = mssg['id']  # get id of individual message
            message = self.service.users().messages().get(userId=user_id,
                                                          id=m_id).execute()  # fetch the message using API
            payld = message['payload']  # get payload of the message
            headr = payld['headers']  # get header of the payload

            for one in headr:  # getting the Subject
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['Subject'] = msg_subject
                else:
                    pass

            for two in headr:  # getting the date
                if two['name'] == 'Date':
                    msg_date = two['value']
                    date_parse = (parser.parse(msg_date))
                    m_date = (date_parse.date())
                    temp_dict['Date'] = str(m_date)
                else:
                    pass

            for three in headr:  # getting the Sender
                if three['name'] == 'From':
                    msg_from = three['value']
                    temp_dict['Sender'] = msg_from
                else:
                    pass

            temp_dict['Snippet'] = message['snippet']  # fetching message snippet

            try:

                # Fetching message body
                mssg_parts = payld['parts']  # fetching the message parts
                part_one = mssg_parts[0]  # fetching first element of the part
                part_body = part_one['body']  # fetching body of the message
                part_data = part_body['data']  # fetching data from the body
                clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
                clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean_two, "lxml")
                mssg_body = soup.body()
                # mssg_body is a readible form of message body
                # depending on the end user's requirements, it can be further cleaned
                # using regex, beautiful soup, or any other method
                temp_dict['Message_body'] = mssg_body

            except:
                pass

            print (temp_dict)
            final_list.append(temp_dict)  # This will create a dictonary item in the final list
            return final_list

            # This will mark the messagea as read
            # GMAIL.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def SendMessage(self, user_id, message):
        """Send an email message.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.

        Returns:
          Sent Message.
        """

        message = (self.service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print 'Message Id: %s' % message['id']
