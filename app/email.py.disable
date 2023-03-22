import smtplib
import email
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Set up the email addresses and password
    my_address = "iotburner28@gmail.com" # Replace with your own Gmail address
    my_password = "uefa acwp roct hnuc" # Replace with your Gmail password
    recipient_address = "ilikefortniteseason4@gmail.com" # Replace with the recipient's email address

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = my_address
    msg['To'] = recipient_address
    msg['Subject'] = "IoT Fan"

    # Add the body to the email
    body = "The current temperature is ***. Would you like to turn on the fan?"
    msg.attach(MIMEText(body, 'plain'))

    # Log in to the Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_address, my_password)

    # Send the email
    text = msg.as_string()
    server.sendmail(my_address, recipient_address, text)

    # Log out of the server
    print('sent to ' + recipient_address)
    server.quit()

def receive_email():
    EMAIL = 'ilikefortniteseason4@gmail.com'
    PASSWORD = 'khui ncfj kdan ocyv'
    SERVER = "imap.gmail.com"

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)

    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''

                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                if mail_subject == 'IoT Fan' or 'IoT Fan' in mail_subject.lower() or any('IoT Fan' in recipient.lower() for recipient in message.get_all('to', [])):
                    print(f'From: {mail_from}')
                    print(f'Subject: {mail_subject}')
                    print(f'Content: {mail_content}')

def receive_reply():
    EMAIL = "iotburner28@gmail.com" # Replace with your own Gmail address
    PASSWORD = "uefa acwp roct hnuc" # Replace with your Gmail password
    SERVER = "imap.gmail.com"

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)

    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''

                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                if mail_content == 'yes' or 'yes' in mail_subject.lower() or any('yes' in recipient.lower() for recipient in message.get_all('to', [])) or 'yes' in mail_content.lower():
                    print(f'From: {mail_from}')
                    print(f'Subject: {mail_subject}')
                    print(f'Content: {mail_content}')
#send_email()
#receive_email()
receive_reply()

