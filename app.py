import datetime

from gmail.gmail import GmailManager
from directory.directory import DirectoryManager


print(datetime.date(2019, 4, 12) == datetime.datetime.today().date())
current_date = str(datetime.datetime.today().day) + '-' + str(datetime.datetime.today().month)
print(current_date)




directory_manager = DirectoryManager()
users = directory_manager.get_users_by_birthday('25-01')

if not users:
    print('No users in the domain.')
else:
    print('Users:')
    for user in users:
        print(u'{0} ({1}) {2}'.format(user['primaryEmail'], user['name']['fullName'], user['customSchemas']['Outros_dados_pessoais']['Data_de_Nascimento']))





gmail_manager = GmailManager()
message = gmail_manager.create_message('me', 'hitalo.emanoel@gmail.com', 'Test Gmail Api', 'This is just a test\n' + current_date)
gmail_manager.send_message('me', message)