import smtplib

port = 465
service_email = 'flatchat.service0@gmail.com'
# noinspection HardcodedPassword
with open('database/password.txt', 'r') as file:
    password = file.read()


def send_verification_email(email: str, auth_link: str, url: str):
    server = smtplib.SMTP_SSL('smtp.gmail.com', port)

    server.ehlo()
    server.login(service_email, password)

    # todo: create an email body and subject. It should be dynamicly generated
    message = f'''Subject: Flatchat verification


Hi, you have been registered to Flatchat.
Please click on the following link to verify your account:
{url}/authenticate/{auth_link}
Greetings your flatchat-team
'''
    print('Sending email to: ' + email)
    server.sendmail(service_email, email, message)
    print('Email sent')

