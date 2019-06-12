import datetime
import json

from gmail.gmail import GmailManager
from directory.directory import DirectoryManager


print(datetime.date(2019, 4, 12) == datetime.datetime.today().date())
month = "{:02d}".format(datetime.datetime.today().month)
day =  "{:02d}".format(datetime.datetime.today().day)
current_date = day + '-' + month
print(current_date)




directory_manager = DirectoryManager()
users = directory_manager.get_users_by_birthday(current_date)

if not users:
    print('No users in the domain.')
else:

    with open('email-config.json') as email_config:
        email = json.load(email_config)
        email['content'] = email['content'].replace('current_date', current_date)
        print(email['content'])

    gmail_manager = GmailManager()
    print('Users:')
    for user in users:
        print(u'{0} ({1}) {2}'.format(user['primaryEmail'], user['name']['fullName'], user['customSchemas']['Outros_dados_pessoais']['Data_de_Nascimento']))
        #message = gmail_manager.create_message('me', 'hitalo.emanoel@gmail.com', 'Test Gmail Api', email['content'])
        #gmail_manager.send_message('me', message)