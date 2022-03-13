import smtplib
import ssl
import os


class EmailService:
    PORT = 465  # For SSL
    PASSWORD = os.environ.get('SMTP_PASSWORD')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
    RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

    def __init__(self, ):

        self.context = ssl.create_default_context()

    def send_email(self, post):
        with smtplib.SMTP_SSL("smtp.gmail.com", EmailService.PORT, context=self.context) as server:
            server.ehlo()
            server.login(EmailService.SENDER_EMAIL, EmailService.PASSWORD)
            subject = "New Apartment found!"
            text = ("Description: \n\n" + post["body"] + "\n\n" + "URL: " + post["url"]).encode('ascii', 'ignore')
            message = 'Subject: {}\n\n{}'.format(subject, text)
            server.sendmail(EmailService.SENDER_EMAIL, EmailService.RECIPIENT_EMAIL, message)
