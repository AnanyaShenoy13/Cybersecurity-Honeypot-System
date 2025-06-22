from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Config

def send_email(subject, message, from_email, to_email):
    try:
        # Setup the SMTP server
        server = SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        server.starttls()
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)

        # Construct email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send email
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {str(e)}')

if __name__ == '__main__':
    send_email("Test Subject", "Test Message", "sender@example.com", "recipient@example.com")
