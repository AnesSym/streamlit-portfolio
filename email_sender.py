import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

RECEIVER_EMAIL = "anesdzehverovic@gmail.com"


def is_valid_email(user_email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, user_email) is not None


def send_email(user_name, user_email, user_message):
    """Send a contact-form message to my inbox. Returns (ok, detail)."""
    if not is_valid_email(user_email):
        return False, "Invalid email address"

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Portfolio message from {user_name}"
    message["From"] = RECEIVER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Reply-To"] = user_email  # hitting Reply answers the visitor

    text = (
        "You have received a new message from your portfolio contact form.\n\n"
        f"Name: {user_name}\n"
        f"Email: {user_email}\n\n"
        f"{user_message}\n"
    )
    message.attach(MIMEText(text, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(RECEIVER_EMAIL, os.getenv("EMAIL_PASSWORD"))
            server.sendmail(RECEIVER_EMAIL, RECEIVER_EMAIL, message.as_string())
        return True, "sent"
    except Exception as e:
        return False, f"Error sending email: {e}"
