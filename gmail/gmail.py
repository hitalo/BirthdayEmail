from __future__ import print_function

from googleapiclient import errors
from googleapiclient.discovery import build

from google.oauth2 import service_account

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import base64
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/gmail.send']

SERVICE_ACCOUNT_FILE = './credentials/service.json'

class GmailManager:


    def __init__(self):
        self.service = self.get_service()


    def get_service(self):

        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        with open('email-sender.json') as email_sender:
            email = json.load(email_sender)
        delegated_credentials = creds.with_subject(email['sender'])

        service = build('gmail', 'v1', credentials=delegated_credentials)
        return service



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
        message = MIMEText(message_text, 'html')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        body = {'raw': raw}
        return body



    def create_message_with_img(self, sender, to, subject, message_text, image_file):
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = to

        message.attach(MIMEText('<p><img src="cid:image1" /></p>' + message_text, 'html'))

        with open(image_file, 'rb') as image:
            image.seek(0)
            img = MIMEImage(image.read(), 'png')

        img.add_header('Content-Id', '<image1>')
        img.add_header("Content-Disposition", "inline", filename="image1")
        message.attach(img)

        raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
        raw_message_no_attachment = raw_message_no_attachment.decode()
        body = {'raw': raw_message_no_attachment}
        return body




    def send_message(self, user_id, message):
        """Send an email message.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.

        Returns:
          Sent Message.
        """
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: ', error)




    def main(self):
        message = self.create_message('me', '@gmail.com', 'Test Gmail Api', 'This is just a test')
        self.send_message('me', message)

if __name__ == '__main__':
    gmail_manager = GmailManager()
    gmail_manager.main()
