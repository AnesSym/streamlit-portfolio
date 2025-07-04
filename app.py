from pathlib import Path
import streamlit as st
from PIL import Image
import base64
import os
from dotenv import load_dotenv
import time
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from streamlit_option_menu import option_menu
from email_sender import send_email, create_toast_notification, show_toast_notification
from streamlit_lottie import st_lottie
import json

# --- PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(page_title="Portfolio | Anes", page_icon=":wave:")

# Import configuration AFTER page config
from config import (
    PAGE_TITLE, PAGE_ICON, NAME, DESCRIPTION, EMAIL, SOCIAL_MEDIA,
    nav_options, PROJECTS, GROQ_MODEL, MAX_TOKENS, CONVERSATIONAL_MEMORY_LENGTH,
    get_system_prompt, ABOUT_ME_TEXT, EXPERIENCE_QUALIFICATIONS, HARD_SKILLS,
    CHAT_INTRO_MESSAGE, CONTACT_FORM_MESSAGE
)
from experience import EXPERIENCE

# Initialize session state for welcome flow
if 'welcome_form_completed' not in st.session_state:
    st.session_state['welcome_form_completed'] = False
if 'splash_shown' not in st.session_state:
    st.session_state['splash_shown'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None

# Step 1: Show welcome form if not completed
if not st.session_state['welcome_form_completed']:
    # Add modern styling
    st.markdown("""
    <style>
    /* Hide Streamlit elements */
    .stApp > header {visibility: hidden;}
    .stApp > footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Reset default margins */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Custom form styling */
    .stForm {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 16px !important;
        color: #E2E8F0 !important;
        padding: 16px 20px !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
        background: rgba(59, 130, 246, 0.15) !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        height: 56px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background: rgba(251, 191, 36, 0.1) !important;
        color: #FCD34D !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin: 16px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Narrower centered layout
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col2:
        st.markdown("""
        <div style="
            background: rgba(30, 27, 75, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 24px;
            padding: 40px 32px;
            box-shadow: 0 32px 64px rgba(0, 0, 0, 0.4);
            margin-top: 12vh;
            text-align: center;
            max-width: 480px;
            margin-left: auto;
            margin-right: auto;
        ">
            <h1 style="
                font-family: 'Inter', sans-serif;
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #C084FC 0%, #6366F1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 16px;
                letter-spacing: -0.02em;
            ">
                Welcome to my Portfolio
            </h1>
            <p style="
                color: #E2E8F0;
                font-size: 1.1rem;
                line-height: 1.6;
                margin-bottom: 32px;
                font-weight: 400;
            ">
                Hi there! I'm Anes Džehverović, and I'm excited to share my work with you.
            </p>
        """, unsafe_allow_html=True)
        
        with st.form("welcome_form"):
            st.markdown("""
            <div style="
                color: #C084FC;
                font-size: 1rem;
                font-weight: 600;
                margin-bottom: 16px;
                text-align: left;
            ">
                What should I call you?
            </div>
            """, unsafe_allow_html=True)
            
            user_name = st.text_input(
                "Your name (optional)", 
                placeholder="Enter your name...",
                label_visibility="collapsed",
                key="user_name_input"
            )
            
            st.markdown('<div style="margin-bottom: 16px;"></div>', unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit_with_name = st.form_submit_button(
                    "Continue with name", 
                    use_container_width=True,
                    type="primary"
                )
            with col_b:
                submit_anonymous = st.form_submit_button(
                    "Continue anonymously", 
                    use_container_width=True
                )
            
            if submit_with_name and user_name:
                st.session_state['user_name'] = user_name.strip()
                st.session_state['welcome_form_completed'] = True
                st.rerun()
            elif submit_with_name and not user_name:
                st.warning("Please enter your name or choose 'Continue anonymously'")
            elif submit_anonymous:
                st.session_state['user_name'] = None
                st.session_state['welcome_form_completed'] = True
                st.rerun()
        
        st.markdown("""
            <div style="
                margin-top: 24px;
                padding-top: 20px;
                border-top: 1px solid rgba(99, 102, 241, 0.2);
                color: #94A3B8;
                font-size: 0.875rem;
                line-height: 1.5;
                text-align: center;
            ">
                Your information stays private and is only used to personalize your experience.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Stop execution here if welcome form not completed
    st.stop()

# Step 2: Show splash screen after form completion
if st.session_state['welcome_form_completed'] and not st.session_state['splash_shown']:
    # Get user name for personalization
    user_name = st.session_state.get('user_name')
    welcome_text = f"Welcome, {user_name}!" if user_name else "Welcome!"
    
    # Full-screen splash screen
    st.markdown(f"""
    <style>
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    .splash-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(-45deg, #1E1B4B, #312E81, #4C1D95, #6366F1);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        backdrop-filter: blur(10px);
    }}
    
    .welcome-text {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        animation: fadeIn 2s ease-out;
        text-shadow: 0 0 40px rgba(192, 132, 252, 0.3);
        letter-spacing: -0.02em;
    }}
    
    .loading-dots {{
        display: flex;
        justify-content: center;
        margin-top: 30px;
        animation: fadeIn 2s ease-out 1s both;
    }}
    
    .dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1, #C084FC);
        margin: 0 4px;
        animation: pulse 1.5s infinite;
    }}
    
    .dot:nth-child(1) {{ animation-delay: 0s; }}
    .dot:nth-child(2) {{ animation-delay: 0.5s; }}
    .dot:nth-child(3) {{ animation-delay: 1s; }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.2); opacity: 0.7; }}
    }}
    </style>
    
    <div class="splash-container">
        <div>
            <div class="welcome-text">{welcome_text}</div>
            <div class="loading-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-advance after 3 seconds
    time.sleep(3)
    st.session_state['splash_shown'] = True
    st.rerun()

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "resume_anes-dzehverovic.pdf"
profile_pic_path = current_dir / "assets" / "Untitled.png"
profile_pic_hover_path = current_dir / "assets" / "Untitled4.png"

# --- CUSTOM CSS ---
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    /* Apply Inter font globally */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    .project {
        display: block;
        width: fit-content;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .description {
        display: none;
        max-height: 0;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .project.open .description {
        display: block;
        max-height: 500px;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# --- LOAD ASSETS ---
with open("assets/Animation3.json") as f:
    animation_data = json.load(f)

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()

# --- UTILITY FUNCTIONS ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def create_assistant_svg_icon():
    """Create a custom SVG icon for the AI assistant with theme colors"""
    return """
    <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="40" height="40" viewBox="0 0 32 32">
    <defs>
        <linearGradient id="modernGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#6366F1;stop-opacity:1" />
            <stop offset="30%" style="stop-color:#8B5CF6;stop-opacity:1" />
            <stop offset="60%" style="stop-color:#A855F7;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#C084FC;stop-opacity:1" />
        </linearGradient>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Main sparkle -->
    <path fill="url(#modernGradient)" filter="url(#glow)" d="M15.304,21.177l-1.203,2.756c-0.463,1.06-1.929,1.06-2.391,0l-1.203-2.756	c-1.071-2.453-2.999-4.406-5.403-5.473l-3.313-1.47c-1.053-0.467-1.053-2,0-2.467l3.209-1.424c2.466-1.095,4.429-3.12,5.481-5.656	L11.7,1.748c0.452-1.09,1.959-1.09,2.411,0l1.219,2.938c1.053,2.537,3.015,4.562,5.481,5.656l3.209,1.424	c1.053,0.467,1.053,2,0,2.467l-3.313,1.47C18.303,16.771,16.375,18.724,15.304,21.177z"/>
    
    <!-- Secondary sparkle -->
    <path fill="url(#modernGradient)" filter="url(#glow)" d="M26.488,29.868l-0.338,0.776	c-0.248,0.568-1.034,0.568-1.282,0l-0.338-0.776c-0.603-1.383-1.69-2.484-3.046-3.087l-1.043-0.463c-0.564-0.25-0.564-1.07,0-1.321	l0.984-0.437c1.391-0.618,2.497-1.76,3.09-3.19l0.348-0.838c0.242-0.584,1.05-0.584,1.292,0l0.348,0.838	c0.593,1.43,1.699,2.572,3.09,3.19l0.984,0.437c0.564,0.251,0.564,1.07,0,1.321l-1.043,0.463	C28.178,27.384,27.092,28.485,26.488,29.868z"/>
    </svg>
    """

def svg_to_data_uri(svg_string):
    """Convert SVG string to data URI for use in Streamlit"""
    import base64
    svg_bytes = svg_string.encode('utf-8')
    svg_base64 = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{svg_base64}"

def create_user_avatar(name=None):
    """Create a circular avatar with the user's initial"""
    # Use the stored user name if available
    if name is None:
        name = st.session_state.get('user_name', 'User')
    
    if name is None:
        name = "User"
        
    initial = name[0].upper() if name else "U"
    avatar_html = f"""
    <div style="
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        margin-right: 8px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    ">
        {initial}
    </div>
    """
    return avatar_html

def display_user_message(message):
    """Display user message on the right with modern styling"""
    user_name = st.session_state.get('user_name', 'User')
    col1, col2 = st.columns([0.92, 0.08])
    with col1:
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            margin-bottom: 16px;
            margin-left: 20px;
        ">
            <div style="
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
                border: 1px solid rgba(99, 102, 241, 0.3);
                padding: 12px 16px;
                border-radius: 16px;
                font-family: 'Inter', sans-serif;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
                word-wrap: break-word;
                overflow-wrap: break-word;
                word-break: break-word;
                white-space: normal;
                max-width: 70%;
                width: fit-content;
                min-width: 50px;
                text-align: right;
                color: #E2E8F0;
            ">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(create_user_avatar(user_name), unsafe_allow_html=True)

def stream_response_smooth(placeholder, text, delay=0.02):
    """Display text with character-by-character smooth animation using consistent markdown"""
    import time
    
    if not text:
        return
    
    displayed_text = ""
    
    # Add custom CSS for cursor animation
    st.markdown("""
    <style>
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    .typing-cursor {
        color: #6366F1;
        animation: blink 1s infinite;
        font-weight: 400;
    }
    </style>
    """, unsafe_allow_html=True)
    
    for i, char in enumerate(text):
        displayed_text += char
        
        # Use markdown but add cursor as simple text
        cursor_text = displayed_text + "│"  # Using a simple cursor character
        placeholder.markdown(cursor_text)
        
        # Shorter delay for spaces and punctuation
        if char in [' ', '.', ',', '!', '?', '\n']:
            time.sleep(delay * 0.5)
        else:
            time.sleep(delay)
    
    # Final state - pure markdown, no cursor
    placeholder.markdown(text)

def print_letter_by_letter(message, is_assistant=True, delay=0.025):
    if is_assistant:
        avatar_svg = svg_to_data_uri(create_assistant_svg_icon())
        chat_placeholder = st.chat_message("ai", avatar=avatar_svg)
        message_placeholder = chat_placeholder.empty()
        
        # Use the smooth streaming function with animation
        stream_response_smooth(message_placeholder, message, delay=0.015)
    else:
        # For user messages, use the custom display function
        display_user_message(message)

def manage_chat_history(max_messages=20):
    """Keep only the last max_messages in chat history and sync with LangChain memory"""
    if len(st.session_state['chat_history']) > max_messages:
        # Keep only the last max_messages in session state
        st.session_state['chat_history'] = st.session_state['chat_history'][-max_messages:]
        
        # Clear and rebuild LangChain memory to stay in sync
        memory.clear()
        
        # Re-add recent messages to LangChain memory in the correct order
        for msg in st.session_state['chat_history']:
            if msg['role'] == 'user':
                memory.chat_memory.add_user_message(msg['content'])
            elif msg['role'] == 'assistant':
                memory.chat_memory.add_ai_message(msg['content'])

# --- HERO SECTION ---
profile_pic_base64 = get_base64_of_bin_file(profile_pic_path)
profile_pic_hover_base64 = get_base64_of_bin_file(profile_pic_hover_path)

col1, col2 = st.columns(2, gap="small")
with col1:
    st.markdown(
        f"""
        <div class="profile-pic-container">
            <img class="profile-pic" src="data:image/png;base64,{profile_pic_base64}" alt="Profile Picture">
            <img class="profile-pic-hover" src="data:image/png;base64,{profile_pic_hover_base64}" alt="Profile Picture Hover">
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.title(NAME)
    
    st.write(DESCRIPTION)
    st.write("**E-mail:**", EMAIL)
    st.download_button(
        label="[Download Resume](#)",
        data=PDFbyte,
        file_name=resume_file.name,
        mime="application/octet-stream",
        key="download_resume_button"
    )

# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA) + 1)  # Add one more column for the info icon
for index, (platform, details) in enumerate(SOCIAL_MEDIA.items()):
    with cols[index]:
        if platform == "GitHub":
            icon_svg = """<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>"""
        else:  # LinkedIn
            icon_svg = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#0077B5">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>"""
        
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                {icon_svg}
                <a href="{details['url']}" target="_blank" style="text-decoration: none; color: #faf3e1; font-weight: 500;">{platform}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# Add info icon in the last column
with cols[-1]:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <div class="info-icon-container" style="
                position: relative;
                display: inline-block;
                cursor: pointer;
            ">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="
                    color: #6366F1;
                    transition: all 0.3s ease;
                " onmouseover="this.style.color='#C084FC'" onmouseout="this.style.color='#6366F1'">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 16v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M12 8h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <div class="info-tooltip" style="
                    visibility: hidden;
                    opacity: 0;
                    position: absolute;
                    top: -10px;
                    right: 100%;
                    margin-right: 10px;
                    width: 280px;
                    background: linear-gradient(135deg, rgba(30, 27, 75, 0.95) 0%, rgba(17, 24, 39, 0.95) 100%);
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 12px;
                    padding: 16px;
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
                    backdrop-filter: blur(10px);
                    z-index: 1000;
                    transition: all 0.3s ease;
                ">
                    <div style="
                        color: #C084FC;
                        font-size: 0.9rem;
                        font-weight: 600;
                        margin-bottom: 12px;
                        text-align: center;
                    ">AI Assistant Technology Stack</div>
                    <div style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 8px;
                        font-size: 0.8rem;
                        color: #E2E8F0;
                        font-family: 'Inter', sans-serif;
                        flex-wrap: wrap;
                    ">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L8 6H16L12 2Z" fill="url(#infoGradient)"/>
                            <path d="M12 22L8 18H16L12 22Z" fill="url(#infoGradient)"/>
                            <path d="M2 12L6 8V16L2 12Z" fill="url(#infoGradient)"/>
                            <path d="M22 12L18 8V16L22 12Z" fill="url(#infoGradient)"/>
                            <circle cx="12" cy="12" r="3" fill="url(#infoGradient)"/>
                            <defs>
                                <linearGradient id="infoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" style="stop-color:#6366F1"/>
                                    <stop offset="100%" style="stop-color:#C084FC"/>
                                </linearGradient>
                            </defs>
                        </svg>
                        <span style="font-weight: 500;">Powered by</span>
                        <span style="
                            background: rgba(99, 102, 241, 0.2);
                            border: 1px solid rgba(99, 102, 241, 0.4);
                            border-radius: 8px;
                            padding: 2px 6px;
                            color: #C084FC;
                            font-weight: 600;
                        ">Groq</span>
                        <span style="color: #64748B;">+</span>
                        <span style="
                            background: rgba(99, 102, 241, 0.2);
                            border: 1px solid rgba(99, 102, 241, 0.4);
                            border-radius: 8px;
                            padding: 2px 6px;
                            color: #C084FC;
                            font-weight: 600;
                        ">LangChain</span>
                        <span style="color: #64748B;">+</span>
                        <span style="
                            background: rgba(99, 102, 241, 0.2);
                            border: 1px solid rgba(99, 102, 241, 0.4);
                            border-radius: 8px;
                            padding: 2px 6px;
                            color: #C084FC;
                            font-weight: 600;
                        ">Meta Llama 3.1</span>
                    </div>
                </div>
            </div>
            <span style="color: #faf3e1; font-weight: 500;">Tech Stack</span>
        </div>
        
        <style>
        .info-icon-container:hover .info-tooltip {
            visibility: visible !important;
            opacity: 1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- NAVIGATION ---
with st.sidebar:
    # --- USER STATUS HEADER ---
    # Get user info
    user_name = st.session_state.get('user_name')
    
    if user_name:
        # Single line with restart button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style="
                padding: 12px 0;
                display: flex;
                align-items: center;
                gap: 8px;
            ">
                <span style="
                    width: 6px;
                    height: 6px;
                    background: #10B981;
                    border-radius: 50%;
                    display: inline-block;
                "></span>
                <span style="
                    color: #10B981;
                    font-size: 12px;
                    font-weight: 500;
                    font-family: 'Inter', sans-serif;
                    text-transform: lowercase;
                ">active</span>
                <span style="
                    color: #64748B;
                    font-size: 12px;
                    font-family: 'Inter', sans-serif;
                ">|</span>
                <span style="
                    color: #E2E8F0;
                    font-size: 12px;
                    font-weight: 400;
                    font-family: 'Inter', sans-serif;
                ">{user_name}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Small restart button
            if st.button("↻", key="restart_session", help="Restart session", use_container_width=True):
                st.session_state.clear()
                st.rerun()
    else:
        # Anonymous user - single line
        st.markdown(f"""
        <div style="
            padding: 12px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="
                width: 6px;
                height: 6px;
                background: #64748B;
                border-radius: 50%;
                display: inline-block;
            "></span>
            <span style="
                color: #64748B;
                font-size: 12px;
                font-weight: 500;
                font-family: 'Inter', sans-serif;
                text-transform: lowercase;
            ">guest</span>
            <span style="
                color: #64748B;
                font-size: 12px;
                font-family: 'Inter', sans-serif;
            ">|</span>
            <span style="
                color: #64748B;
                font-size: 12px;
                font-weight: 400;
                font-family: 'Inter', sans-serif;
            ">anonymous</span>
        </div>
        """, unsafe_allow_html=True)
    
   
    
    # Navigation menu
    selection = option_menu(
        "Navigation",
        options=list(nav_options.keys()),
        icons=list(nav_options.values()),
        menu_icon=None,
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#1E1B4B"},
            "icon": {"color": "#6366F1", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "#312E81", 
                "color": "#E2E8F0",
                "transition": "all 0.3s ease"
            },
            "nav-link-selected": {
                "background-color": "#312E81", 
                "color": "#C084FC", 
                "font-weight": "bold",
                "border-left": "3px solid #6366F1"
            },
            "icon-selected": {"color": "#C084FC"}, 
        },
    )
    


# --- AI SETUP ---
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

groq_api_key = os.environ['GROQ_API_KEY']
groq_chat = ChatGroq(
    groq_api_key=groq_api_key,
    model_name=GROQ_MODEL,
    max_tokens=MAX_TOKENS
)

user_name = st.session_state.get('user_name')
system_prompt = get_system_prompt(EMAIL, SOCIAL_MEDIA, EXPERIENCE, user_name)
memory = ConversationBufferWindowMemory(
    k=CONVERSATIONAL_MEMORY_LENGTH, 
    memory_key="chat_history", 
    return_messages=True
)

# Sync memory with existing session state on startup
def sync_memory_on_startup():
    """Sync LangChain memory with session state on app startup"""
    if st.session_state.get('chat_history'):
        # Clear memory first
        memory.clear()
        
        # Rebuild memory from session state
        for msg in st.session_state['chat_history']:
            if msg['role'] == 'user':
                memory.chat_memory.add_user_message(msg['content'])
            elif msg['role'] == 'assistant':
                memory.chat_memory.add_ai_message(msg['content'])

sync_memory_on_startup()

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}"),
])

conversation = LLMChain(
    llm=groq_chat,
    prompt=prompt,
    verbose=False,
    memory=memory,
)

# --- MAIN CONTENT ---
if selection == "Ask Me Anything":
    st.write("---")
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'intro_shown' not in st.session_state:
        st.session_state['intro_shown'] = False
    
    # Display introduction message only once (but don't add it to chat history)
    if not st.session_state['intro_shown']:
        avatar_svg = svg_to_data_uri(create_assistant_svg_icon())
        with st.chat_message("ai", avatar=avatar_svg):
            from config import get_personalized_intro_message
            intro_message = get_personalized_intro_message()
            st.markdown(intro_message)
        st.session_state['intro_shown'] = True
    
    # Display chat history with consistent styling
    if st.session_state['chat_history']:
        for msg in st.session_state['chat_history']:
            if msg['role'] == 'user':
                display_user_message(msg['content'])
            elif msg['role'] == 'assistant':
                # Display assistant message with proper markdown rendering
                avatar_svg = svg_to_data_uri(create_assistant_svg_icon())
                with st.chat_message("ai", avatar=avatar_svg):
                    st.markdown(msg['content'])

    # User input
    question = st.chat_input("Ask me anything...")
    
    if question:
        # Add user message to session state history
        st.session_state['chat_history'].append({
            "role": "user", 
            "content": question
        })
        
        # IMPORTANT: Also add to LangChain memory
        memory.chat_memory.add_user_message(question)
        
        # Display user message
        display_user_message(question)

        # Show classic spinner while processing
        with st.spinner("Thinking..."):
            try:
                response = conversation.predict(human_input=question)
            except Exception as e:
                response = f"I apologize, but I encountered an error: {str(e)}"

        # Display assistant response with animation
        print_letter_by_letter(response, is_assistant=True)

        # Add assistant response to session state history
        st.session_state['chat_history'].append({
            "role": "assistant", 
            "content": response
        })
        
        # Manage history length to prevent memory issues
        manage_chat_history(max_messages=20)
        
        # Single rerun to refresh the page and show updated history
        st.rerun()

elif selection == "About Me":
    st.markdown("""
    <style>
    .about-hero {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 32px;
        margin: 24px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .about-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #06B6D4, #8B5CF6, #C084FC);
    }
    
    .about-title {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 16px;
        letter-spacing: -0.01em;
    }
    
    .about-subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 24px;
        line-height: 1.6;
    }
    
    .about-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        margin-top: 32px;
    }
    
    .about-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 27, 75, 0.4) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .about-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    .about-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #06B6D4, #8B5CF6, #C084FC);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .about-card:hover::before {
        opacity: 1;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .card-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .about-card:hover .card-icon {
        transform: scale(1.1);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
    }
    
    .card-title {
        color: #C084FC;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0;
    }
    
    .card-content {
        color: #E2E8F0;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .text-description-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 27, 75, 0.4) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 32px;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        margin-top: 24px;
    }
    
    .text-description-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #06B6D4, #8B5CF6, #C084FC);
    }
    
    .text-description-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 32px rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .description-content {
        color: #E2E8F0;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: center;
        margin: 0;
    }
    
    .personal-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 16px;
        margin: 24px 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 16px;
        background: rgba(6, 182, 212, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(6, 182, 212, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stat-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.2);
        background: rgba(6, 182, 212, 0.15);
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06B6D4, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #94A3B8;
        font-size: 0.85rem;
        margin-top: 4px;
        font-weight: 500;
    }
    
    .interests-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 16px;
    }
    
    .interest-tag {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .interest-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%);
    }
    
    .interest-tag .text {
        color: #E2E8F0;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .timeline-item {
        position: relative;
        padding-left: 24px;
        margin-bottom: 20px;
        border-left: 2px solid rgba(99, 102, 241, 0.3);
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -5px;
        top: 0;
        width: 8px;
        height: 8px;
        background: linear-gradient(135deg, #06B6D4, #8B5CF6);
        border-radius: 50%;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
    }
    
    .timeline-year {
        color: #06B6D4;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .timeline-event {
        color: #E2E8F0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .quote-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 24px 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .quote-card::before {
        content: '"';
        position: absolute;
        top: -10px;
        left: 20px;
        font-size: 4rem;
        color: rgba(99, 102, 241, 0.2);
        font-family: Georgia, serif;
    }
    
    .quote-text {
        color: #E2E8F0;
        font-size: 1.1rem;
        font-style: italic;
        line-height: 1.6;
        margin-bottom: 16px;
    }
    
    .quote-author {
        color: #06B6D4;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    @media (max-width: 768px) {
        .about-grid {
            grid-template-columns: 1fr;
        }
        
        .personal-stats {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .interests-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="about-hero">
        <div class="about-title">About Me</div>
        <div class="about-subtitle">
            AI Engineer & Physics Graduate passionate about building intelligent systems that make a difference
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Stats
    st.markdown("""
    <div class="personal-stats">
        <div class="stat-item">
            <div class="stat-number">2+</div>
            <div class="stat-label">Years in AI/ML</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">5+</div>
            <div class="stat-label">Companies Worked</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">10+</div>
            <div class="stat-label">Projects Completed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">∞</div>
            <div class="stat-label">Lines of Code</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Content Cards - Fixed 3-column layout
    
    # Text Description Card
    st.markdown("""
    <div class="text-description-card">
        <div class="description-content">
            I'm a passionate AI Engineer with a Master's in Applied Physics, combining scientific rigor with cutting-edge technology. 
            My journey from physics to AI has given me a unique perspective on problem-solving and system design. I love building 
            intelligent systems that solve real-world problems and push the boundaries of what's possible. Whether it's developing 
            semantic search engines, creating data pipelines, or mentoring fellow developers, I'm always excited about the next 
            challenge that combines innovation with practical impact.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Interests
    st.markdown("""
    <div class="about-card" style="margin-top: 32px;">
        <div class="card-header">
            <div class="card-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20.84 4.61C20.3292 4.099 19.7228 3.69364 19.0554 3.41708C18.3879 3.14052 17.6725 2.99817 16.95 2.99817C16.2275 2.99817 15.5121 3.14052 14.8446 3.41708C14.1772 3.69364 13.5708 4.099 13.06 4.61L12 5.67L10.94 4.61C9.9083 3.5783 8.50903 2.9987 7.05 2.9987C5.59096 2.9987 4.19169 3.5783 3.16 4.61C2.1283 5.6417 1.5487 7.04097 1.5487 8.5C1.5487 9.95903 2.1283 11.3583 3.16 12.39L12 21.23L20.84 12.39C21.351 11.8792 21.7563 11.2728 22.0329 10.6053C22.3095 9.93789 22.4518 9.22248 22.4518 8.5C22.4518 7.77752 22.3095 7.06211 22.0329 6.39467C21.7563 5.72723 21.351 5.1208 20.84 4.61V4.61Z" fill="url(#beyondGradient)"/>
                    <defs>
                        <linearGradient id="beyondGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#8B5CF6"/>
                            <stop offset="100%" style="stop-color:#C084FC"/>
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            <h3 class="card-title">Beyond Code</h3>
        </div>
        <div class="card-content">
            <div class="interests-grid">
                <div class="interest-tag">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 12L11 14L15 10" stroke="url(#targetGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="url(#targetGradient)" stroke-width="2"/>
                        <defs>
                            <linearGradient id="targetGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#06B6D4"/>
                                <stop offset="100%" style="stop-color:#8B5CF6"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <span class="text">Problem Solving</span>
                </div>
                <div class="interest-tag">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4 19.5C4 18.837 4.26339 18.2011 4.73223 17.7322C5.20107 17.2634 5.83696 17 6.5 17H20" stroke="url(#bookGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M6.5 2H20V22H6.5C5.83696 22 5.20107 21.7366 4.73223 21.2678C4.26339 20.7989 4 20.163 4 19.5V4.5C4 3.83696 4.26339 3.20107 4.73223 2.73223C5.20107 2.26339 5.83696 2 6.5 2Z" stroke="url(#bookGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <defs>
                            <linearGradient id="bookGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#8B5CF6"/>
                                <stop offset="100%" style="stop-color:#C084FC"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <span class="text">Continuous Learning</span>
                </div>
                <div class="interest-tag">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L8 6H16L12 2Z" fill="url(#scienceGradient)"/>
                        <path d="M12 22L8 18H16L12 22Z" fill="url(#scienceGradient)"/>
                        <path d="M2 12L6 8V16L2 12Z" fill="url(#scienceGradient)"/>
                        <path d="M22 12L18 8V16L22 12Z" fill="url(#scienceGradient)"/>
                        <circle cx="12" cy="12" r="3" fill="url(#scienceGradient)"/>
                        <defs>
                            <linearGradient id="scienceGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#06B6D4"/>
                                <stop offset="100%" style="stop-color:#6366F1"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <span class="text">Physics & Research</span>
                </div>
                <div class="interest-tag">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="url(#mentorGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="9" cy="7" r="4" stroke="url(#mentorGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M23 21V19C23 18.1645 22.7155 17.3541 22.2094 16.6977C21.7033 16.0414 20.9983 15.5757 20.2 15.3657" stroke="url(#mentorGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke="url(#mentorGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <defs>
                            <linearGradient id="mentorGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#8B5CF6"/>
                                <stop offset="100%" style="stop-color:#C084FC"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <span class="text">Mentoring</span>
                </div>
                <div class="interest-tag">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.663 17H4.5C3.11929 17 2 15.8807 2 14.5C2 13.1193 3.11929 12 4.5 12H9.663C10.5837 12 11.337 11.2467 11.337 10.326V9.674C11.337 8.75329 10.5837 8 9.663 8H2" stroke="url(#innovationGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14.337 7H19.5C20.8807 7 22 8.11929 22 9.5C22 10.8807 20.8807 12 19.5 12H14.337C13.4163 12 12.663 12.7533 12.663 13.674V14.326C12.663 15.2467 13.4163 16 14.337 16H22" stroke="url(#innovationGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <defs>
                            <linearGradient id="innovationGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#06B6D4"/>
                                <stop offset="100%" style="stop-color:#8B5CF6"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <span class="text">Innovation</span>
                </div>
                <div class="interest-tag">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 3L1 9L12 15L21 10.09V17H23V9L12 3Z" fill="url(#teachingGradient)"/>
                        <path d="M5 13.18V17.18C5 19.54 8.58 21 12 21C15.42 21 19 19.54 19 17.18V13.18L12 17L5 13.18Z" fill="url(#teachingGradient)"/>
                        <defs>
                            <linearGradient id="teachingGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#8B5CF6"/>
                                <stop offset="100%" style="stop-color:#C084FC"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <span class="text">Teaching</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Journey Timeline
    st.markdown("""
    <div class="about-card" style="margin-top: 24px;">
        <div class="card-header">
            <div class="card-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="url(#timelineGradient)" stroke-width="2"/>
                    <polyline points="12,6 12,12 16,14" stroke="url(#timelineGradient)" stroke-width="2" stroke-linecap="round"/>
                    <defs>
                        <linearGradient id="timelineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#06B6D4"/>
                            <stop offset="100%" style="stop-color:#6366F1"/>
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            <h3 class="card-title">My Journey</h3>
        </div>
        <div class="card-content">
            <div class="timeline-item">
                <div class="timeline-year">2024 - Present</div>
                <div class="timeline-event">AI Engineer at Social Explorer, building semantic search systems</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">2023 - 2024</div>
                <div class="timeline-event">Physics Teacher & Data Science Engineer roles</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">2018 - 2023</div>
                <div class="timeline-event">Bachelor's in Applied Physics, University of Sarajevo</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">2022 - 2023</div>
                <div class="timeline-event">Started professional journey with internships</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Quote
    st.markdown("""
    <div class="quote-card">
        <div class="quote-text">
            The best way to predict the future is to create it through intelligent systems that understand and adapt to human needs.
        </div>
        <div class="quote-author">— My personal philosophy</div>
    </div>
    """, unsafe_allow_html=True)

elif selection == "Experience & Qualifications":
    st.markdown("""
    <style>
    .qual-container {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 32px;
        margin: 24px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    
    .qual-title {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.01em;
    }
    
    .highlight-stat {
    text-align: center;
    padding: 16px;
    background: rgba(6, 182, 212, 0.1);
    border-radius: 12px;
    margin: 8px 0 16px 0;
    border: 1px solid rgba(6, 182, 212, 0.2);
    transition: all 0.3s ease;
    position: relative;
    cursor: pointer;
    }
    
    .highlight-stat:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.2);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06B6D4, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-top: 4px;
    }
    
    /* Stats row container */
    .stats-row {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .stats-row .st-emotion-cache-1r6slb0 {
        flex: 1;
        min-width: 0;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 280px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 27, 75, 0.95) 100%);
        color: #E2E8F0;
        text-align: left;
        border-radius: 12px;
        padding: 16px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -140px;
        opacity: 0;
        transition: opacity 0.3s ease;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(15, 23, 42, 0.95) transparent transparent transparent;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .tooltip-title {
        color: #C084FC;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    
    .tooltip-item {
        color: #94A3B8;
        font-size: 0.8rem;
        margin-bottom: 4px;
    }
    
    .tooltip-item:before {
        content: "• ";
        color: #6366F1;
        font-weight: bold;
    }
    
    .qual-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 8px;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .qual-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 15px 35px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    .qual-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #06B6D4, #8B5CF6, #C084FC);
    }
    
    .qual-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .qual-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    
    .qual-card-title {
        color: #C084FC;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    .qual-card-content {
        position: relative;
        padding-bottom: 40px;
        min-height: 100px;
    }
    
    .experience-badge {
        position: absolute;
        bottom: 0;
        right: 0;
        display: inline-block;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(6, 182, 212, 0.4);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #06B6D4;
        transition: all 0.3s ease;
    }
    
    .experience-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
    }
    
    .qual-card-text {
        color: #E2E8F0;
        line-height: 1.6;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container with all content inside
    st.markdown("""
    <div class="qual-container">
        <div class="qual-title">Experience & Qualifications</div>
    """, unsafe_allow_html=True)
    
    # Stats section - inside the container with better spacing
    st.markdown('<div class="stats-row">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="highlight-stat">
            <div class="stat-number">2+</div>
            <div class="stat-label">Years in AI/ML</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-stat tooltip">
            <div class="stat-number">5+</div>
            <div class="stat-label">Programming Languages</div>
            <span class="tooltiptext">
                <div class="tooltip-title">Programming Languages</div>
                <div class="tooltip-item">Python (Expert)</div>
                <div class="tooltip-item">JavaScript (Intermediate)</div>
                <div class="tooltip-item">SQL (Advanced)</div>
                <div class="tooltip-item">Shell Scripting (Advanced)</div>
                <div class="tooltip-item">HTML/CSS (Intermediate)</div>
                <div class="tooltip-item">C++ (Basic)</div>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="highlight-stat tooltip">
            <div class="stat-number">10+</div>
            <div class="stat-label">Technologies Mastered</div>
            <span class="tooltiptext">
                <div class="tooltip-title">Technologies & Tools</div>
                <div class="tooltip-item">FastAPI & REST APIs</div>
                <div class="tooltip-item">Docker & Containerization</div>
                <div class="tooltip-item">Git & Version Control</div>
                <div class="tooltip-item">PostgreSQL & MongoDB</div>
                <div class="tooltip-item">OpenAI & LLMs</div>
                <div class="tooltip-item">Pinecone & Vector DBs</div>
                <div class="tooltip-item">Streamlit & Web Apps</div>
                <div class="tooltip-item">Linux & Cloud Platforms</div>
                <div class="tooltip-item">Machine Learning Libraries</div>
                <div class="tooltip-item">AutoGen & Multi-Agent Systems</div>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add some spacing before cards
    st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
    
    # Cards section - inside the container
    col1, col2 = st.columns(2)
    
    with col1:
        # AI & Engineering Expertise
        st.markdown("""
        <div class="qual-card">
            <div class="qual-card-header">
                <div class="qual-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L8 6H16L12 2Z" fill="url(#aiGradient)"/>
                        <path d="M12 22L8 18H16L12 22Z" fill="url(#aiGradient)"/>
                        <path d="M2 12L6 8V16L2 12Z" fill="url(#aiGradient)"/>
                        <path d="M22 12L18 8V16L22 12Z" fill="url(#aiGradient)"/>
                        <circle cx="12" cy="12" r="3" fill="url(#aiGradient)"/>
                        <defs>
                            <linearGradient id="aiGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#06B6D4"/>
                                <stop offset="100%" style="stop-color:#8B5CF6"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <h3 class="qual-card-title">AI & Engineering Expertise</h3>
            </div>
            <div class="qual-card-content">
                <div class="qual-card-text">
                    • Experienced in AI Engineering and backend architecture<br>
                    • Expert in semantic search and data pipeline development<br>
                    • Proficient in FastAPI, Docker, SQL, Git, and Vector Databases
                </div>
                <div class="experience-badge">2+ Years Experience</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Academic & Teaching
        st.markdown("""
        <div class="qual-card">
            <div class="qual-card-header">
                <div class="qual-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 3L1 9L12 15L21 10.09V17H23V9L12 3Z" fill="url(#academicGradient)"/>
                        <path d="M5 13.18V17.18C5 19.54 8.58 21 12 21C15.42 21 19 19.54 19 17.18V13.18L12 17L5 13.18Z" fill="url(#academicGradient)"/>
                        <defs>
                            <linearGradient id="academicGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#8B5CF6"/>
                                <stop offset="100%" style="stop-color:#C084FC"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <h3 class="qual-card-title">Academic & Teaching</h3>
            </div>
            <div class="qual-card-content">
                <div class="qual-card-text">
                    • Master's in Applied Physics (In Progress)<br>
                    • Created engaging learning experiences in Physics<br>
                    • Strong analytical and problem-solving abilities
                </div>
                <div class="experience-badge">Educational Background</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Programming & Data Science
        st.markdown("""
        <div class="qual-card">
            <div class="qual-card-header">
                <div class="qual-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 3H16C17.1 3 18 3.9 18 5V19C18 20.1 17.1 21 16 21H8C6.9 21 6 20.1 6 19V5C6 3.9 6.9 3 8 3Z" stroke="url(#codingGradient)" stroke-width="2" fill="none"/>
                        <path d="M10 7L8 9L10 11" stroke="url(#codingGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14 7L16 9L14 11" stroke="url(#codingGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M9 15H15" stroke="url(#codingGradient)" stroke-width="2" stroke-linecap="round"/>
                        <defs>
                            <linearGradient id="codingGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#06B6D4"/>
                                <stop offset="100%" style="stop-color:#6366F1"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <h3 class="qual-card-title">Programming & Data Science</h3>
            </div>
            <div class="qual-card-content">
                <div class="qual-card-text">
                    • Proficient in Python, Data Analysis, and Engineering<br>
                    • Strong foundation in statistical principles and machine learning<br>
                    • Skilled in automated processes and efficiency improvement
                </div>
                <div class="experience-badge">3+ Years Experience</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Leadership & Collaboration
        st.markdown("""
        <div class="qual-card">
            <div class="qual-card-header">
                <div class="qual-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="url(#teamGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="9" cy="7" r="4" stroke="url(#teamGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M23 21V19C23 18.1645 22.7155 17.3541 22.2094 16.6977C21.7033 16.0414 20.9983 15.5757 20.2 15.3657" stroke="url(#teamGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke="url(#teamGradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <defs>
                            <linearGradient id="teamGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#8B5CF6"/>
                                <stop offset="100%" style="stop-color:#C084FC"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <h3 class="qual-card-title">Leadership & Collaboration</h3>
            </div>
            <div class="qual-card-content">
                <div class="qual-card-text">
                    • Excellent collaborator and proactive problem solver<br>
                    • Managed projects and shaped strategic direction<br>
                    • Cross-functional team integration and optimization
                </div>
                <div class="experience-badge">Proven Track Record</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

elif selection == "Skills":
    st.markdown("""
    <style>
    .skills-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(17, 24, 39, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .skills-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    .skills-title {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 32px;
        letter-spacing: -0.01em;
    }
    
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 25px;
        padding: 8px 16px;
        margin: 4px;
        color: #E2E8F0;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .skill-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
    }
    
    .skills-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="skills-card">
        <div class="skills-title">Hard Skills</div>
        <div class="skills-grid">
            <div class="skill-badge">Python</div>
            <div class="skill-badge">FastAPI</div>
            <div class="skill-badge">Machine Learning</div>
            <div class="skill-badge">OpenAI</div>
            <div class="skill-badge">Pinecone</div>
            <div class="skill-badge">Computer Vision</div>
            <div class="skill-badge">Data Engineering</div>
            <div class="skill-badge">REST APIs</div>
            <div class="skill-badge">Docker</div>
            <div class="skill-badge">Git</div>
            <div class="skill-badge">SQL</div>
            <div class="skill-badge">MongoDB</div>
            <div class="skill-badge">PostgreSQL</div>
            <div class="skill-badge">Streamlit</div>
            <div class="skill-badge">Linux</div>
            <div class="skill-badge">Shell Scripting</div>
            <div class="skill-badge">Data Analysis</div>
            <div class="skill-badge">AutoGen</div>
            <div class="skill-badge">Web Scraping</div>
            <div class="skill-badge">Physics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif selection == "Work History":
    st.markdown("""
    <style>
    .work-header {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 24px;
        margin: 24px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .work-title {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.01em;
    }
    
    .job-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(17, 24, 39, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    .job-title {
        color: #C084FC;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 16px;
    }
    
    .job-content {
        position: relative;
        padding-bottom: 40px;
        min-height: 120px;
    }
    
    .job-description {
        color: #E2E8F0;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    .job-period {
        position: absolute;
        bottom: 0;
        right: 0;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(6, 182, 212, 0.4);
        border-radius: 20px;
        padding: 4px 12px;
        color: #06B6D4;
        font-size: 0.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .job-period:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header section
    st.markdown("""
    <div class="work-header">
        <div class="work-title">Work History</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Job cards
    st.markdown("""
    <div class="job-card">
        <div class="job-title">AI Engineer | Social Explorer - Remote</div>
        <div class="job-content">
            <div class="job-description">
                • Designed and implemented fully AI-driven data service architecture using FastAPI<br>
                • Developed semantic search capabilities across entire Social Explorer databases using OpenAI and Pinecone<br>
                • Created comprehensive data pipelines to migrate data from standard databases to vector databases<br>
                • Specialized in data filtering, reranking, and preprocessing for optimal search performance<br>
                • Implemented AutoGen framework for multi-agent workflows and automated data processing
            </div>
            <div class="job-period">11/2024 - Present</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Second job
    st.markdown("""
    <div class="job-card">
        <div class="job-title">Data Engineer | Social Explorer - Remote</div>
        <div class="job-content">
            <div class="job-description">
                • Developed data processing pipelines and machine learning algorithms for predictive analytics<br>
                • Implemented computer vision models from Meta for advanced data analysis<br>
                • Created and maintained web scraping scripts for data acquisition
            </div>
            <div class="job-period">11/2024 - 01/2025</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Third job
    st.markdown("""
    <div class="job-card">
        <div class="job-title">API/Back-End Engineer | Skylark AI</div>
        <div class="job-content">
            <div class="job-description">
                • Engineering REST APIs and back-end systems for enhanced data processing<br>
                • Collaborating with cross-functional teams to integrate and optimize backend services
            </div>
            <div class="job-period">07/2024 - 11/2024</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fourth job
    st.markdown("""
    <div class="job-card">
        <div class="job-title">Data Science Engineer | Caze AI</div>
        <div class="job-content">
            <div class="job-description">
                • Developed full-stack backend architecture and data preprocessing pipelines<br>
                • Implemented machine learning models and managed projects, shaping strategic direction
            </div>
            <div class="job-period">02/2024 - 11/2024</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fifth job
    st.markdown("""
    <div class="job-card">
        <div class="job-title">Physics Teacher | Richmond Park Education</div>
        <div class="job-content">
            <div class="job-description">
                • Created engaging, interactive learning experiences for students<br>
                • Simplified complex physics concepts to foster a love for the subject
            </div>
            <div class="job-period">08/2023 - 06/2024</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sixth job
    st.markdown("""
    <div class="job-card">
        <div class="job-title">Sales Automation Director | Two Lights</div>
        <div class="job-content">
            <div class="job-description">
                • Designed and coded standardized email templates for communication<br>
                • Automated personalized email distribution, improving engagement and response times<br>
                • Integrated email systems with databases and CRM platforms for seamless operation
            </div>
            <div class="job-period">09/2023 - 02/2024</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Seventh job
    st.markdown("""
    <div class="job-card">
        <div class="job-title">Intern | Symphony</div>
        <div class="job-content">
            <div class="job-description">
                • Processed and visualized various data types<br>
                • Created a custom plotting library and backend services<br>
                • Containerized backend services and databases, and implemented machine learning models
            </div>
            <div class="job-period">02/2023 - 05/2023</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Eighth job
    st.markdown("""
    <div class="job-card">
        <div class="job-title">Intern | Cosylab</div>
        <div class="job-content">
            <div class="job-description">
                • Learned Linux, GIT, SVN, Python, Shell Scripting, EPICS software<br>
                • Designed project architectures during the EPICS academy
            </div>
            <div class="job-period">07/2022 - 08/2022</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif selection == "Education":
    st.markdown("""
    <style>
    .education-header {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 24px;
        margin: 24px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .education-title {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.01em;
    }
    
    .edu-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(17, 24, 39, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .edu-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    .edu-degree {
        color: #C084FC;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 16px;
    }
    
    .edu-content {
        position: relative;
        padding-bottom: 40px;
        min-height: 100px;
    }
    
    .edu-description {
        color: #E2E8F0;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    .edu-period {
        position: absolute;
        bottom: 0;
        right: 0;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(6, 182, 212, 0.4);
        border-radius: 20px;
        padding: 4px 12px;
        color: #06B6D4;
        font-size: 0.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .edu-period:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header section
    st.markdown("""
    <div class="education-header">
        <div class="education-title">Education</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Master's degree
    st.markdown("""
    <div class="edu-card">
        <div class="edu-degree">Master's degree, Applied Physics | University of Sarajevo</div>
        <div class="edu-content">
            <div class="edu-description">
                Pursuing a Master's degree in Applied Physics, focusing on advanced topics in physics and their applications in various fields. Currently working on finding the best solution for a flattening filter using Monte Carlo simulations.
            </div>
            <div class="edu-period">Oct 2023 — Present</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bachelor's degree
    st.markdown("""
    <div class="edu-card">
        <div class="edu-degree">Bachelor's degree, Applied Physics | University of Sarajevo</div>
        <div class="edu-content">
            <div class="edu-description">
                Completed a Bachelor's degree in Applied Physics, gaining strong abilities to solve problems, strong analytical skills, and programming skills.
            </div>
            <div class="edu-period">Sep 2018 — Jan 2023</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif selection == "Projects & Accomplishments":
    st.markdown("""
    <style>
    .projects-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(17, 24, 39, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    
    .projects-title {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.01em;
    }
    
    /* Enhanced expander styling */
    .stExpander {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 16px !important;
        margin-bottom: 16px !important;
        backdrop-filter: blur(5px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stExpander:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
    }
    
    .stExpander > div > div:first-child {
        background: transparent !important;
        color: #C084FC !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .stExpander > div > div:last-child {
        background: transparent !important;
        color: #E2E8F0 !important;
        padding: 16px !important;
        line-height: 1.6 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="projects-card">
        <div class="projects-title">Projects & Accomplishments</div>
    """, unsafe_allow_html=True)
    
    for project, details in PROJECTS.items():
        with st.expander(project):
            st.write(details['description'])
            st.write(f"**Skills:** {', '.join(details['skills'])}")
            st.markdown(f"[Learn more]({details['link']})", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif selection == "Send Me a Message":
    st.write("---")
    
    # Modern contact form styling
    st.markdown("""
    <style>
    /* Contact form container */
    .contact-form-container {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 24px 28px;
        margin: 24px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Form inputs styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
        color: #E2E8F0 !important;
        padding: 16px 20px !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
        background: rgba(15, 23, 42, 0.95) !important;
        outline: none !important;
    }
    
    /* Input labels */
    .stTextInput > label,
    .stTextArea > label {
        color: #C084FC !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    /* Submit button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        height: 56px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
        background: linear-gradient(135deg, #4C1D95 0%, #7C3AED 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* Form title */
    .contact-form-title {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 16px;
        letter-spacing: -0.01em;
    }
    
    /* Form description */
    .contact-form-description {
        color: #94A3B8;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get the user's name from session state if available
    stored_user_name = st.session_state.get('user_name', '')
    
    # Use container to ensure proper nesting
    with st.container():
        st.markdown("""
        <div class="contact-form-container">
            <div class="contact-form-title">
                Let's Connect
            </div>
            <div class="contact-form-description">
                I'd love to hear from you! Send me a message and I'll get back to you as soon as possible.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            # Create two columns for name and email
            col1, col2 = st.columns(2)
            
            with col1:
                # Use stored name as default value, or show placeholder
                if stored_user_name:
                    user_name = st.text_input(
                        "Your Name", 
                        value=stored_user_name,  # Pre-fill with their name
                        placeholder="John Doe"
                    )
                else:
                    user_name = st.text_input(
                        "Your Name", 
                        placeholder="John Doe"
                    )
            
            with col2:
                user_email = st.text_input("Your Email", placeholder=f"{stored_user_name}@example.com")
            
            # Message field (full width)
            # Personalize the message placeholder too
            if stored_user_name:
                message_placeholder = f"Hello Anes, this is {stored_user_name}. I would like to connect with you about..."
            else:
                message_placeholder = "Hello Anes, I would like to connect with you about..."
                
            user_message = st.text_area("Your Message", placeholder=message_placeholder, height=120)
            
            # Submit button with spacing
            st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
            submit_button = st.form_submit_button("Send Message")

            if submit_button:
                if user_name and user_email and user_message:
                    # Show loading animation first
                    loading_placeholder = st.empty()
                    with loading_placeholder.container():
                        st.markdown("""
                        <div style="
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            padding: 20px;
                            gap: 10px;
                        ">
                            <div style="
                                width: 20px;
                                height: 20px;
                                border: 2px solid #6366F1;
                                border-top: 2px solid transparent;
                                border-radius: 50%;
                                animation: spin 1s linear infinite;
                            "></div>
                            <span style="
                                color: #8B5CF6;
                                font-weight: 500;
                                font-size: 14px;
                            ">Sending your message...</span>
                        </div>
                        <style>
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                        </style>
                        """, unsafe_allow_html=True)
                    
                    # Send the email
                    success, message = send_email(user_name, user_email, user_message)
                    
                    # Clear loading animation
                    loading_placeholder.empty()
                    
                    if success:
                        # Show success toast notification that auto-closes
                        show_toast_notification(message, is_success=True)
                        
                    else:
                        # Show error toast notification that auto-closes
                        show_toast_notification(message, is_success=False)
                        
                else:
                    # Show error for missing fields
                    show_toast_notification("Please fill out all fields before sending.", is_success=False)
    
    # Privacy footer section
    st.markdown("""
    <div style="
        margin-top: 32px;
        padding: 24px;
        text-align: center;
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.4) 0%, rgba(17, 24, 39, 0.5) 100%);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(8px);
    ">
        <div style="
            color: #94A3B8;
            font-size: 0.95rem;
            line-height: 1.6;
            font-weight: 500;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        ">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 10V8C6 5.79086 7.79086 4 10 4H14C16.2091 4 18 5.79086 18 8V10" stroke="url(#lockGradient)" stroke-width="2" stroke-linecap="round"/>
                <rect x="4" y="10" width="16" height="10" rx="2" fill="url(#lockGradient)" fill-opacity="0.2"/>
                <rect x="4" y="10" width="16" height="10" rx="2" stroke="url(#lockGradient)" stroke-width="2"/>
                <circle cx="12" cy="15" r="2" fill="url(#lockGradient)"/>
                <defs>
                    <linearGradient id="lockGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#06B6D4;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#8B5CF6;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#C084FC;stop-opacity:1" />
                    </linearGradient>
                </defs>
            </svg>
            <strong>Privacy Notice:</strong> Your information is not stored anywhere on this website.
        </div>
        <div style="
            color: #64748B;
            font-size: 0.9rem;
            line-height: 1.5;
            font-weight: 400;
        ">
            This form uses Gmail's secure email service to send your message directly to my inbox.
            <br>No data is collected, stored, or shared with third parties.
        </div>
    </div>
    """, unsafe_allow_html=True)