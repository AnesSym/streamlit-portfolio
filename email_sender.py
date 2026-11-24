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


def get_email_password():
    """Gmail app password from the environment (.env locally) or Streamlit secrets (Streamlit Cloud).

    Google shows app passwords in groups of four ("abcd efgh ijkl mnop"); the spaces are dropped.
    """
    password = os.getenv("EMAIL_PASSWORD")
    if not password:
        try:
            import streamlit as st
            password = st.secrets.get("EMAIL_PASSWORD")
        except Exception:  # no secrets file configured
            password = None
    return password.replace(" ", "").strip() if password else None


def send_email(user_name, user_email, user_message):
    """Send a contact-form message to my inbox. Returns (ok, detail); detail explains a failure for the logs."""
    if not is_valid_email(user_email):
        return False, "Invalid email address"

    password = get_email_password()
    if not password:
        return False, "EMAIL_PASSWORD is not set. Add it as a top-level secret in the app's Secrets settings."

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
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as server:
            server.login(RECEIVER_EMAIL, password)
            server.sendmail(RECEIVER_EMAIL, RECEIVER_EMAIL, message.as_string())
        return True, "sent"
    except smtplib.SMTPAuthenticationError as e:
        return False, (f"Gmail rejected the login ({e.smtp_code}). EMAIL_PASSWORD must be a 16-character Gmail "
                       f"app password, not the account password: {e.smtp_error!r}")
    except (OSError, smtplib.SMTPException) as e:
        return False, f"Could not send through smtp.gmail.com:465: {e!r}"
