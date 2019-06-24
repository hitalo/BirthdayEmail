import datetime
import json

from gmail.gmail import GmailManager
from directory.directory import DirectoryManager


#print(datetime.date(2019, 4, 12) == datetime.datetime.today().date())
month = "{:02d}".format(datetime.datetime.today().month)
day =  "{:02d}".format(datetime.datetime.today().day)
current_date = day + '-' + month




directory_manager = DirectoryManager()
users = directory_manager.get_users_by_birthday(current_date)

if not users:
    print('No users in the domain.')
else:

    with open('email-config.json') as email_config:
        email = json.load(email_config)

        #To add vars
        #email['content'] = email['content'].replace('##DATE##', current_date)

    #users = ['@gmail.com', '@uern.br']

    gmail_manager = GmailManager()
    for user in users:
        if("alu.uern.br" in user['primaryEmail']): #TODO check in query
            continue

        #print(u'{0} ({1}) {2}'.format(user['primaryEmail'], user['name']['fullName'], user['customSchemas']['Outros_dados_pessoais']['Data_de_Nascimento']))
        message = gmail_manager.create_message('me', user['primaryEmail'], email['subject'], email['content'])
        gmail_manager.send_message('me', message)