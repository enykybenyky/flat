
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_email(subject, body):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
