import datetime

from gmail.gmail import GmailManager


print(datetime.date(2019, 4, 12) == datetime.datetime.today().date())
current_date = str(datetime.datetime.today().day) + '/' + str(datetime.datetime.today().month) + '/' + str(datetime.datetime.today().year)
print(current_date)

gmail_manager = GmailManager()
message = gmail_manager.create_message('me', 'hitalo.emanoel@gmail.com', 'Test Gmail Api', 'This is just a test\n' + current_date)
gmail_manager.send_message('me', message)