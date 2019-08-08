import smtplib
from email.message import EmailMessage

def main():
    send_message('test','testteeee')

def send_message(subject,message):
    from_email = 'farrukh_london@hotmail.com'
    to_email = 'farrukh.tamimi@gmail.com'


    msg = EmailMessage()

    msg['Subject'] = subject
    msg.set_content(message)
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP('smtp-mail.outlook.com',587)
    server.starttls()
    server.login('farrukh_london@hotmail.com','W0nd3r4ul!')

    server.send_message(msg,from_email,to_email)
    server.close()


if __name__ == '__main__':
    main()
