import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import os
from dotenv import load_dotenv
import re
import time

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

def is_valid_email(user_email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, user_email) is not None

def send_email(user_name, user_email, user_message):
    try:
        if not is_valid_email(user_email):
            return False, "Invalid email address"
        
        sender_email = user_email
        receiver_email = "anesdzehverovic@gmail.com"
        password = os.getenv("EMAIL_PASSWORD")  

        message = MIMEMultipart("alternative")
        message["Subject"] = "New Message from Portfolio Contact Form"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"""
        You have received a new message from your portfolio contact form.

        Name: {user_name}
        Email: {user_email}
        Message: 
        {user_message}
        """
        part = MIMEText(text, "plain")
        message.attach(part)

        # Send the email
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465) 
            server.login(receiver_email, password)
            server.sendmail(receiver_email, receiver_email, message.as_string())
            server.quit()
            return True, "Email sent!"
        except Exception as e:
            return False, f"Error sending email: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"
    
if __name__ == "__main__":
    user_name = "John Doe"
    user_email = "johndoe@example.com"
    user_message = "Hello, this is a test message"
    success, message = send_email(user_name, user_email, user_message)
    print(success, message)