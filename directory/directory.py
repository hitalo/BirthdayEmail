from __future__ import print_function

from googleapiclient.discovery import build
from google.oauth2 import service_account

import json

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
SERVICE_ACCOUNT_FILE = './credentials/service.json'

class DirectoryManager:

    def __init__(self):
        self.service = self.get_service()

    def get_service(self):

        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        with open('email-sender.json') as email_sender:
            email = json.load(email_sender)
        delegated_credentials = creds.with_subject(email['sender'])

        service = build('admin', 'directory_v1', credentials=delegated_credentials)
        return service




    def get_users_by_birthday(self, birthday):
        results = self.service.users().list(customer='my_customer',
                                       orderBy='email', projection='full',
                                       query='Outros_dados_pessoais.Data_de_Nascimento:' + birthday).execute()
        users = results.get('users', [])
        return users