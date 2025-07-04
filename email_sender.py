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
            return True, f"Thanks {user_name}! Your message has been sent successfully. I'll get back to you soon!"
        except Exception as e:
            return False, f"Error sending email: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

def create_toast_notification(message, is_success=True):
    """Create a modern toast notification with CSS-only auto-close"""
    toast_type = "success" if is_success else "error"
    icon = "✅" if is_success else "❌"
    
    toast_html = f"""
    <div class="toast-notification toast-{toast_type}">
        <div class="toast-content">
            <div class="toast-icon">{icon}</div>
            <div class="toast-message">{message}</div>
        </div>
        <div class="toast-progress"></div>
    </div>
    
    <style>
    .toast-notification {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 27, 75, 0.95) 100%);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        z-index: 9999;
        min-width: 350px;
        max-width: 500px;
        font-family: 'Inter', sans-serif;
        animation: slideInAndOut 4s ease-out forwards;
    }}
    
    .toast-success {{
        border-left: 4px solid #10B981;
    }}
    
    .toast-error {{
        border-left: 4px solid #EF4444;
    }}
    
    .toast-content {{
        display: flex;
        align-items: center;
        padding: 16px 20px;
        gap: 12px;
    }}
    
    .toast-icon {{
        font-size: 24px;
        flex-shrink: 0;
    }}
    
    .toast-message {{
        color: #E2E8F0;
        font-size: 14px;
        line-height: 1.5;
        font-weight: 500;
        flex-grow: 1;
    }}
    
    .toast-progress {{
        height: 3px;
        background: linear-gradient(90deg, #10B981 0%, #06B6D4 100%);
        border-radius: 0 0 8px 8px;
        animation: progressBar 4s linear forwards;
    }}
    
    .toast-error .toast-progress {{
        background: linear-gradient(90deg, #EF4444 0%, #F59E0B 100%);
    }}
    
    @keyframes slideInAndOut {{
        0% {{
            transform: translateX(100%);
            opacity: 0;
        }}
        15% {{
            transform: translateX(0);
            opacity: 1;
        }}
        85% {{
            transform: translateX(0);
            opacity: 1;
        }}
        100% {{
            transform: translateX(100%);
            opacity: 0;
        }}
    }}
    
    @keyframes progressBar {{
        from {{
            width: 100%;
        }}
        to {{
            width: 0%;
        }}
    }}
    
    @media (max-width: 768px) {{
        .toast-notification {{
            top: 10px;
            right: 10px;
            left: 10px;
            min-width: unset;
            max-width: unset;
        }}
    }}
    </style>
    """
    
    return toast_html

def show_toast_notification(message, is_success=True):
    """Show toast notification and automatically clear it after 4 seconds"""
    # Initialize toast state
    if 'toast_show_time' not in st.session_state:
        st.session_state.toast_show_time = None
    if 'toast_message' not in st.session_state:
        st.session_state.toast_message = None
    if 'toast_success' not in st.session_state:
        st.session_state.toast_success = True
    
    # Set toast data
    st.session_state.toast_show_time = time.time()
    st.session_state.toast_message = message
    st.session_state.toast_success = is_success
    
    # Show the toast
    toast_html = create_toast_notification(message, is_success)
    st.markdown(toast_html, unsafe_allow_html=True)
    
    # Schedule automatic clearing after 4 seconds
    time.sleep(4)
    st.session_state.toast_show_time = None
    st.session_state.toast_message = None
    st.rerun()

if __name__ == "__main__":
    user_name = "John Doe"
    user_email = "johndoe@example.com"
    user_message = "Hello, this is a test message"
    success, message = send_email(user_name, user_email, user_message)
    print(success, message)