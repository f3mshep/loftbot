import smtplib
import ssl
import os


class EmailService:
    PORT = 465  # For SSL
    PASSWORD = os.environ.get('SMTP_PASSWORD')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')

    def __init__(self, ):

        self.context = ssl.create_default_context()

    def send_email(self, post):
        with smtplib.SMTP_SSL("smtp.gmail.com", EmailService.PORT, context=self.context) as server:
            server.ehlo()
            server.login(EmailService.SENDER_EMAIL, EmailService.PASSWORD)
            subject = "New Apartment found!"
            text = ("Description: \n\n" + post["body"] + "\n\n" + "URL: " + post["url"]).encode('ascii', 'ignore')
            message = 'Subject: {}\n\n{}'.format(subject, text)
            for email in self._get_emails():

                server.sendmail(EmailService.SENDER_EMAIL, email, message)

    def _get_emails(self):
        emails = os.environ.get('RECIPIENT_EMAIL')
        if emails is not None:
            return emails.split(',')

