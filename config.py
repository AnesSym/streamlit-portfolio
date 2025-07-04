from experience import EXPERIENCE
import streamlit as st
# --- GENERAL SETTINGS ---
PAGE_TITLE = "Portfolio | Anes"
PAGE_ICON = ":wave:"
NAME = """[Anes Džehverović]"""

link_to_data_science_engineer = "https://www.google.com/search?q=what+does+a+data+science+engineer+do&oq=what+does+a+data+science+en&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBggBEEUYOTIKCAIQABgPGBYYHjIICAMQABgWGB4yCAgEEAAYFhgeMg0IBRAAGIYDGIAEGIoFMg0IBhAAGIYDGIAEGIoFMg0IBxAAGIYDGIAEGIoFMg0ICBAAGIYDGIAEGIoFMg0ICRAAGIYDGIAEGIoFqAIAsAIA&sourceid=chrome&ie=UTF-8"

DESCRIPTION = f""" **[AI Engineer]({link_to_data_science_engineer}) | Python Developer | Applied Physicist**
"""

EMAIL = "anesdzehverovic@gmail.com"

SOCIAL_MEDIA = {
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/anes-dzehverovic-63aa4421b/",
        "icon": "💼"
    },
    "GitHub": {
        "url": "https://github.com/AnesSym/",
        "icon": "💻"
    }
}

# --- NAVIGATION OPTIONS ---
nav_options = {
    "Ask Me Anything": "bi-chat-dots",
    "About Me": "bi-person-fill",
    "Experience & Qualifications": "bi-briefcase-fill",
    "Skills": "bi-tools",
    "Work History": "bi-calendar-fill",
    "Education": "bi-mortarboard-fill",
    "Projects & Accomplishments": "bi-award-fill",
    "Send Me a Message": "bi-envelope-fill",
}

# --- PROJECT DATA ---
PROJECTS = {
    "AI-Driven Data Service | Social Explorer": {
        "link": "https://www.socialexplorer.com/",
        "description": "Architected comprehensive AI service enabling semantic search across Social Explorer's entire database ecosystem. Implemented FastAPI backend with OpenAI integration and Pinecone vector database for intelligent data retrieval. Developed automated data migration pipelines and advanced filtering/reranking systems.",
        "skills": ["Python", "FastAPI", "OpenAI", "Pinecone", "Vector Databases", "Semantic Search", "AutoGen"]
    },
    "External Collaborator | Faculty of Electrical Engineering (ETF)": {
        "link": "https://dsai.etf.unsa.ba/",
        "description": "Collaborated as an external contributor under the mentorship of Prof. Dr. Amila Akagić. Contributed to various data science and AI projects, enhancing research and development efforts.",
        "skills": ["Python", "Machine Learning", "Data Analysis", "Data Science"]
    },
    "AI Model Unit Test Generator | BrusaHyPower": {
        "link": "https://www.brusahypower.com/",
        "description": "Developed an application using Streamlit that incorporates an AI model (Llama2) trained to generate unit tests for Python code. The application features prompt engineering to create effective and comprehensive unit tests.",
        "skills": ["Python", "Streamlit", "AI Model Training", "Prompt Engineering"]
    },
    "AI Model Website App | Data Science Project": {
        "link": "https://streamlit.io/",
        "description": "Created a comprehensive data science web application using Streamlit. The app allows users to input data, run AI models, and visualize results through interactive graphs and charts.",
        "skills": ["Python", "Streamlit", "Data Visualization", "AI Model Deployment"]
    },
    "Llama3 70B Model Implementation and FastAPI | QUOR AI": {
        "link": "https://www.linkedin.com/company/quor-ai/",
        "description": "Implemented a Llama3 70B model using LangChain and Groq. Developed a FastAPI framework and endpoints to facilitate interaction with the model, enabling seamless integration and efficient data processing.",
        "skills": ["Python", "LangChain", "Groq", "FastAPI"]
    },
    "Dental Management System | MasterLab": {
        "link": "https://heroku.com/",
        "description": "Created a full web app for a dental technician firm using Flask framework and deployed it on Heroku. The system manages dental operations efficiently.",
        "skills": ["Flask", "Python", "PostgreSQL", "Heroku"]
    },
    "AI Model Training Code Database": {
        "link": "#",
        "description": "Created a unique code database for training AI models. Scraped GitHub's largest repos for Python functions and their corresponding unit tests. Each pair was evaluated for complexity to train AI models effectively.",
        "skills": ["Python", "Web Scraping", "Data Analysis", "Machine Learning"]
    }
}

# --- AI CONFIGURATION ---
GROQ_MODEL = 'llama-3.1-8b-instant'
MAX_TOKENS = 3000
CONVERSATIONAL_MEMORY_LENGTH = 5

def get_system_prompt(email, social_media, experience, user_name=None):
    # Create personalized greeting if user shared their name
    if user_name:
        personalized_intro = f"""The user you are talking to is named {user_name}. Address them by their name naturally in conversations. When greeting them or responding, you can use their name to make it more personal.
    
    Examples with their name:
        Question: Hi
        Answer: Hi {user_name}, welcome to my portfolio! How can I help you?
        
        Question: Thanks
        Answer: You're welcome, {user_name}! I'm here to help. Feel free to ask again anytime!
        
        Question: Tell me about your experience
        Answer: Sure {user_name}, I'd be happy to share my experience with you...
    """
    else:
        personalized_intro = ""
    
    return f"""You are a helpful assistant representing Anes Džehverović. You reply with concise but friendly answers. You only answer questions about Anes Džehverović, his experience, skills, and projects.
    You answer as if you are Anes himself.
    
    {personalized_intro}
    
    My personal information is:
        phone: +387 60 33 59 406
        email: {email}
        github and linkedin: {social_media}
        My resume is available for download in the top right corner below my email address.
        You can send me a message in the "Send Me a Message" section.
        Nothing else from my personal life should be answered.
    Sections included in my Portfolio are:
        - About Me
        - Experience & Qualifications
        - Skills
        - Work History
        - Education
        - Projects & Accomplishments
        - Send Me a Message
    Examples:
        example 1:
            Question: Who built this portfolio?
            Answer: I did. Do you like it?
        example 2:
            Question: Hi
            Answer: Hi, welcome to my portfolio. How can I help you?
        example 3:
            Question: Thanks
            Answer: You're welcome! I'm here to help. Feel free to ask again, I'm not going anywhere 😊
    I want you to only use the following information about Anes: {experience}
    Do not give out misinformation. 
    Example:
        Question: How many years do you have in Python development?
        Answer: I have 1 to 2 years of experience in Python development.
    Example:
        Question: Who built this portfolio or app or website?
        Answer: I did of course, to showcase my skills and experience. I used streamlit to build it.
    If someone asks a question regarding Physics, you can answer it.    
"""

# --- CONTENT STRINGS ---
ABOUT_ME_TEXT = """
Hey there! I'm Anes Dževherović, a passionate AI Engineer, Data Science Engineer, and Applied Physicist, currently making waves in the bustling tech hubs of New York City and beyond. When I'm not diving deep into AI architectures or crafting intelligent data services, you can find me unraveling the mysteries of the universe—or at least trying to.

Currently, I'm an AI Engineer at Social Explorer, where I architect fully AI-driven data services and implement semantic search capabilities across massive databases using cutting-edge technologies like OpenAI, Pinecone vector databases, and AutoGen frameworks. Previously, I gained valuable experience as a Data Science Engineer at Caze AI and as an API/Back-End Engineer at Skylark AI, developing full-stack architectures and training models.

Before transitioning fully into AI engineering, I even spent time as a Physics Teacher in Sarajevo, sharing my enthusiasm for the cosmos with curious minds at Richmond Park Education. I believe in making complex concepts as simple as possible—kind of like explaining quantum physics to your cat. Speaking of which, I have a couple of feline friends who love to "help" me with my work (byyyyyyyyy sitting on my keyboard).

In my free time, you'll likely catch me engaging in some intense puzzle-solving sessions. Whether it's chess, Rubik's cubes, or some obscure brain-teaser, I'm all in. I also love gaming—because who doesn't need a good boss battle to unwind? My gaming setup might just rival my work setup (but don't tell my boss).

Oh, and did I mention I have a knack for creating AI-driven data services, building semantic search systems, and developing multi-agent workflows? When I'm not busy architecting AI solutions or playing games, I'm probably dreaming up my next big project or collaboration.

So, that's a bit about me—a tech enthusiast with a love for cats, puzzles, and the occasional deep-space pondering. Feel free to explore my projects, connect with me, or just drop a message to say hi. Let's make something amazing together!
"""

EXPERIENCE_QUALIFICATIONS = """
- Experienced in AI Engineering and backend architecture
- Proficient in Python, Data Analysis, and Engineering
- Strong foundation in statistical principles and machine learning
- Skilled in FastAPI, Docker, SQL, Git, and Vector Databases
- Expert in semantic search and data pipeline development
- Created engaging learning experiences in Physics
- Automated processes and improved efficiency
- Excellent collaborator and proactive problem solver
"""

HARD_SKILLS = """
- **Programming**: Python (FastAPI, Flask), SQL, Shell Scripting
- **Data Engineering**: Data Pipelines, ETL Processes, Web Scraping, Data Preprocessing
- **AI & Machine Learning**: OpenAI, LangChain, Groq, AutoGen, Computer Vision (Meta models), Model Training
- **Vector Databases**: Pinecone, Semantic Search, Data Filtering and Reranking
- **Data Visualization**: Streamlit, Pandas, Custom Plotting Libraries
- **Databases**: SQLAlchemy, Postgres, Vector Databases, Dockerized Databases
- **Infrastructure**: Docker, Cloud Computing, AI Architecture Design, Multi-Agent Systems
"""

# --- UI MESSAGES ---
CHAT_INTRO_MESSAGE = "Hello, Welcome to my portfolio. Feel free to look around or ask me anything!"
CONTACT_FORM_MESSAGE = "Feel free to send me a message. I'll get back to you as soon as possible!" 

def get_personalized_intro_message():
    """Get personalized intro message based on user name"""
    user_name = st.session_state.get('user_name')
    
    if user_name:
        return f"Hello {user_name}, welcome to my portfolio! How can I help you?"
    else:
        return "Hello, welcome to my portfolio! How can I help you?" 