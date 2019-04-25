from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
CREDENTIAL = './credentials/directory/credentials.json'
PORT = 8085
TOKEN = 'directory-token.pickle'

class DirectoryManager:

    def __init__(self):
        self.service = self.get_service()

    def get_service(self):

        creds = None
        if os.path.exists(TOKEN):
            with open(TOKEN, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL, SCOPES)
                creds = flow.run_local_server(port=PORT)
            with open(TOKEN, 'wb') as token:
                pickle.dump(creds, token)

        service = build('admin', 'directory_v1', credentials=creds)
        return service




    def get_users_by_birthday(self, birthday):
        results = self.service.users().list(customer='my_customer',
                                       orderBy='email', projection='full',
                                       query='Outros_dados_pessoais.Data_de_Nascimento:' + birthday).execute()
        users = results.get('users', [])
        return users