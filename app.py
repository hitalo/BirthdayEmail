from gmail.gmail import GmailManager

gmail_manager = GmailManager()
message = gmail_manager.create_message('me', 'hitalo.emanoel@gmail.com', 'Test Gmail Api', 'This is just a test')
gmail_manager.send_message('me', message)