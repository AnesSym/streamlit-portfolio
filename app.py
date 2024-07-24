from pathlib import Path
from groq import Groq
import streamlit as st
from PIL import Image
import base64
import os
from dotenv import load_dotenv
import time
from experience import EXPERIENCE


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "resume_anes-dzehverovic.pdf"
profile_pic_path = current_dir / "assets" / "Untitled.png"
profile_pic_hover_path = current_dir / "assets" / "Untitled4.png"

link_to_data_science_engineer = "https://www.google.com/search?q=what+does+a+data+science+engineer+do&oq=what+does+a+data+science+en&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBggBEEUYOTIKCAIQABgPGBYYHjIICAMQABgWGB4yCAgEEAAYFhgeMg0IBRAAGIYDGIAEGIoFMg0IBhAAGIYDGIAEGIoFMg0IBxAAGIYDGIAEGIoFMg0ICBAAGIYDGIAEGIoFMg0ICRAAGIYDGIAEGIoFqAIAsAIA&sourceid=chrome&ie=UTF-8"
# --- GENERAL SETTINGS ---
PAGE_TITLE = "Portfolio | Anes"
PAGE_ICON = ":wave:"
NAME = """[Anes Džehverović]"""
DESCRIPTION = f""" **[Data Science Engineer]({link_to_data_science_engineer}) | Python Developer | Applied Phyicisist**
"""
EMAIL = "anesdzehverovic@gmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/anes-dzehverovic-63aa4421b/",
    "GitHub": "https://github.com/AnesSym/"
}


PROJECTS = {
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


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON,  layout="centered")
st.markdown(
    """
    <style>
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
        max-height: 500px; /* Adjust as needed */
    }
    
    </style>
    <script>
    function toggleDescription(event) {
        var element = event.currentTarget;
        element.classList.toggle("open");
    }
    </script>
    """,
    unsafe_allow_html=True
)

# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()

# --- ENCODE IMAGES TO BASE64 ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

profile_pic_base64 = get_base64_of_bin_file(profile_pic_path)
profile_pic_hover_base64 = get_base64_of_bin_file(profile_pic_hover_path)

# --- HERO SECTION ---
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
    if 'intro_shown_name' not in st.session_state:
        st.session_state['intro_shown_name'] = False

    if not st.session_state['intro_shown_name']:
        import_text = """streamlit run .\portfolio.py
                         from information.py import NAME
                         
                            """
        placeholder = st.empty()
        displayed_text = ""

        for char in import_text:
            displayed_text += char
            placeholder.markdown(f"<h1>{displayed_text}</h1>", unsafe_allow_html=True)
            time.sleep(0.01)

        time.sleep(0.1)  # Pause before showing the actual name
        placeholder.markdown(f"<h1>{NAME}</h1>", unsafe_allow_html=True)
        st.session_state['intro_shown_name'] = True
    else:
        st.title(NAME)
    st.write(DESCRIPTION)
    st.write("📫", EMAIL)
    st.download_button(
        label=" 📄 Download Resume",
        data=PDFbyte,
        file_name=resume_file.name,
        mime="application/octet-stream",
    )
    


# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")

# --- AI ---
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")
client = Groq(api_key=api_key)



system_prompt = {
    "role": "system",
    "content": f"""You are a helpful assistant. You reply with very short answers. You only answer questions about Anes Džehverović, his experience, skills, and projects.
    You answer like someone is talking to Anes.
    My personal infomration is:
        phone: +387 60 33 59 406
        email: {EMAIL}
        github and linkedin: {SOCIAL_MEDIA}
        My resume is available for download in the top right corner below my email address.
    Examples:
        example 1:
            Question: Who built this portfolio?
            Answer: I did. Do you like it?.
        example 2:
            Question: Hi
            Answer: Hi, welcome to my portfolio. How can I help you?
        example 2:
            Question: Thanks
            Answer: You're welcome! I'm here to help. Feel free to ask again, im not going anywhere :smiley_face:
    I want you to only use the following information about Anes: {EXPERIENCE}
    Do not give out missinformation. 
    Example:
        Question: How many years do you have in Python development?
        Answer: I have 1 to 2 years of experience in Python development.
    If someone asks a question regarding Physics, you can answer.    
"""
    
}

# Initialize the chat history
chat_history = [system_prompt]

# Function to get a response from the Groq AI model
def get_groq_response(question):
    chat_history.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=150,
        temperature=0.5
    )
    answer = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": answer})
    return answer

st.sidebar.write("---")
st.sidebar.subheader("Navigation")
nav_options = ["Ask Me Anything", "Home", "Experience & Qualifications", "Skills", "Work History", "Education", "Projects & Accomplishments"]
selection = st.sidebar.radio("Go to", nav_options)

if 'question_asked' not in st.session_state:
    st.session_state['question_asked'] = False

def print_letter_by_letter(message, avatar=":material/neurology:", delay=0.025):
    chat_placeholder = st.chat_message("ai", avatar=avatar)
    message_placeholder = chat_placeholder.empty()

    displayed_message = ""
    for char in message:
        displayed_message += char
        message_placeholder.write(displayed_message)
        time.sleep(delay)

if 'question' not in st.session_state:
    st.session_state['question'] = ""

if 'intro_shown' not in st.session_state:
    st.session_state['intro_shown'] = False

if selection == "Ask Me Anything":
    if not st.session_state['intro_shown']:
        print_letter_by_letter("Hello, Welcome to my portfolio. Feel free to look around or ask me anything!")
        st.session_state['intro_shown'] = True
    st.write("---")
    
    question = st.chat_input("Ask me anything about my experience and skills")
    
    if question:
        st.session_state['question'] = question
        st.session_state['question_asked'] = True
        #st.rerun()

if st.session_state['question_asked']:
    with st.chat_message("user", avatar=":material/face:"):
        st.text(st.session_state['question'])
    with st.spinner("Thinking..."):   
        answer = get_groq_response(st.session_state['question'])
    
    print_letter_by_letter(answer, avatar=":material/neurology:")
    
    st.session_state['question_asked'] = False
    st.session_state['question'] = ""


# --- MAIN SECTION ---
if selection == "Home":
    # --- EXPERIENCE & QUALIFICATIONS ---
    st.write('\n')
    st.subheader("Experience & Qulifications")
    st.write("---")
    st.write(
        """
    - ✔️ Experienced in Data Science and backend architecture
    - ✔️ Proficient in Python, Data Analysis, and Engineering
    - ✔️ Strong foundation in statistical principles
    - ✔️ Skilled in FastAPI, Docker, SQL, and Git
    - ✔️ Created engaging learning experiences in Physics
    - ✔️ Automated processes and improved efficiency
    - ✔️ Excellent collaborator and proactive problem solver


    """
    )


    # --- SKILLS ---
    
    st.write('\n')
    st.subheader("Hard Skills")
    st.write("---")
    st.write(
        """
        - 👩‍💻 Programming: Python (FastAPI, Flask), SQL, Shell Scripting
        - 📊 Data Visualization: Streamlit, Pandas, Custom Plotting Libraries
        - 📚 Modeling: Machine Learning, Data Preprocessing, Model Training
        - 🗄️ Databases: SQLAlchemy, Postgres, Dockerized Databases
        - 🧠 AI: Llama models, LangChain, OpenAI,  Groq
        """
    )


    # --- WORK HISTORY ---
    st.write('\n')
    st.subheader("Work History")
    st.write("---")

    st.write("🚧", "Transfered to **API/Back-End Engineer | [Skylark.ai](https://www.skylarkai.com)**")
    st.write("07/2024 - Present")
    st.write(
        """
    - ► Engineering APIs and back-end systems for enhanced data processing
    - ► Collaborating with cross-functional teams to integrate and optimize backend services
    """
    )
    st.write('\n')
    st.write("🚧", "**Data Science Engineer | [Caze AI](https://caze.ai/)**")
    st.write("02/2024 - Present")
    st.write(
        """
    - ► Developed full-stack backend architecture and data preprocessing pipelines
    - ► Implemented machine learning models and managed projects, shaping strategic direction
    """
    )
    st.write('\n')
    st.write("🚧", "**Physics Teacher | [Richmond Park Education](https://secondary.rps.edu.ba/en/)**")
    st.write("08/2023 - 06/2024")
    st.write(
        """
    - ► Created engaging, interactive learning experiences for students
    - ► Simplified complex physics concepts to foster a love for the subject
    """
    )
    st.write('\n')
    st.write("🚧", "**Sales Automation Director | [Two Lights](https://twolights.dev/)**")
    st.write("09/2023 - 02/2024")
    st.write(
        """
    - ► Designed and coded standardized email templates for communication
    - ► Automated personalized email distribution, improving engagement and response times
    - ► Integrated email systems with databases and CRM platforms for seamless operation
    """
    )
    st.write('\n')
    st.write("🚧", "**Intern | [Symphony](https://symphony.is/)**")
    st.write("02/2023 - 05/2023")
    st.write(
        """
    - ► Processed and visualized various data types
    - ► Created a custom plotting library and backend services
    - ► Containerized backend services and databases, and implemented machine learning models
    """
    )
    st.write('\n')
    st.write("🚧", "**Intern | [Cosylab](https://cosylab.com/)**")
    st.write("07/2022 - 08/2022")
    st.write(
        """
    - ► Learned Linux, GIT, SVN, Python, Shell Scripting, EPICS software
    - ► Designed project architectures during the EPICS academy
    """
    )
    st.write('\n')
    st.subheader("Education")
    st.write("---")
    st.write("🎓 **Master's degree, Applied Physics | [University of Sarajevo](https://fizika.pmf.unsa.ba/)**")
    st.write("Oct 2023 — Present")
    st.write(
        """
        Pursuing a Master's degree in Applied Physics, focusing on advanced topics in physics and their applications in various fields.
        Currently working on finding the best solution for a flattening filter using Monte Carlo simulations.
        """
    )
    st.write('\n')
    st.write("🎓 **Bachelor's degree, Applied Physics | [University of Sarajevo](https://fizika.pmf.unsa.ba/)**")
    st.write("Sep 2018 — Jan 2023")
    st.write(
        """
        Completed a Bachelor's degree in Applied Physics, gaining strong abilities to solve problems, strong analytical skills, and programming skills.
        """
    )

    # --- Projects & Accomplishments ---
    st.write('\n')
    st.subheader("Projects & Accomplishments")
    st.write("---")
    for project, details in PROJECTS.items():
        with st.expander(project):
            st.write(details['description'])
            st.write(f"**Skills:** {', '.join(details['skills'])}")
            st.markdown(f"[Learn more]({details['link']})", unsafe_allow_html=True)

elif selection == "Experience & Qualifications":
    st.subheader("Experience & Qualifications")
    st.write("---")
    st.write(
        """
        - ✔️ Experienced in Data Science and backend architecture
        - ✔️ Proficient in Python, Data Analysis, and Engineering
        - ✔️ Strong foundation in statistical principles
        - ✔️ Skilled in FastAPI, Docker, SQL, and Git
        - ✔️ Created engaging learning experiences in Physics
        - ✔️ Automated processes and improved efficiency
        - ✔️ Excellent collaborator and proactive problem solver
        """
    )

elif selection == "Skills":
    st.subheader("Hard Skills")
    st.write("---")
    st.write(
        """
        - 👩‍💻 Programming: Python (FastAPI, Flask), SQL, Shell Scripting
        - 📊 Data Visualization: Streamlit, Pandas, Custom Plotting Libraries
        - 📚 Modeling: Machine Learning, Data Preprocessing, Model Training
        - 🗄️ Databases: SQLAlchemy, Postgres, Dockerized Databases
        - 🧠 AI: Llama models, LangChain, OpenAI,  Groq
        """
    )

elif selection == "Work History":
    st.subheader("Work History")
    st.write("---")
    st.write("🚧", "Transferred to **API/Back-End Engineer | [Skylark.ai](https://www.skylarkai.com)**")
    st.write("07/2024 - Present")
    st.write(
        """
        - ► Engineering APIs and back-end systems for enhanced data processing
        - ► Collaborating with cross-functional teams to integrate and optimize backend services
        """
    )
    st.write('\n')
    st.write("🚧", "**Data Science Engineer | [Caze AI](https://caze.ai/)**")
    st.write("02/2024 - Present")
    st.write(
        """
        - ► Developed full-stack backend architecture and data preprocessing pipelines
        - ► Implemented machine learning models and managed projects, shaping strategic direction
        """
    )
    st.write('\n')
    st.write("🚧", "**Physics Teacher | [Richmond Park Education](https://secondary.rps.edu.ba/en/)**")
    st.write("08/2023 - 06/2024")
    st.write(
        """
        - ► Created engaging, interactive learning experiences for students
        - ► Simplified complex physics concepts to foster a love for the subject
        """
    )
    st.write('\n')
    st.write("🚧", "**Sales Automation Director | [Two Lights](https://twolights.dev/)**")
    st.write("09/2023 - 02/2024")
    st.write(
        """
        - ► Designed and coded standardized email templates for communication
        - ► Automated personalized email distribution, improving engagement and response times
        - ► Integrated email systems with databases and CRM platforms for seamless operation
        """
    )
    st.write('\n')
    st.write("🚧", "**Intern | [Symphony](https://symphony.is/)**")
    st.write("02/2023 - 05/2023")
    st.write(
        """
        - ► Processed and visualized various data types
        - ► Created a custom plotting library and backend services
        - ► Containerized backend services and databases, and implemented machine learning models
        """
    )
    st.write('\n')
    st.write("🚧", "**Intern | [Cosylab](https://cosylab.com/)**")
    st.write("07/2022 - 08/2022")
    st.write(
        """
        - ► Learned Linux, GIT, SVN, Python, Shell Scripting, EPICS software
        - ► Designed project architectures during the EPICS academy
        """
    )

elif selection == "Education":
    st.subheader("Education")
    st.write("---")
    st.write("🎓 **Master's degree, Applied Physics | [University of Sarajevo](https://fizika.pmf.unsa.ba/)**")
    st.write("Oct 2023 — Present")
    st.write(
        """
        Pursuing a Master's degree in Applied Physics, focusing on advanced topics in physics and their applications in various fields.
        Currently working on finding the best solution for a flattening filter using Monte Carlo simulations.
        """
    )
    st.write('\n')
    st.write("🎓 **Bachelor's degree, Applied Physics | [University of Sarajevo](https://fizika.pmf.unsa.ba/)**")
    st.write("Sep 2018 — Jan 2023")
    st.write(
        """
        Completed a Bachelor's degree in Applied Physics, gaining strong abilities to solve problems, strong analytical skills, and programming skills.
        """
    )

elif selection == "Projects & Accomplishments":
    st.subheader("Projects & Accomplishments")
    st.write("---")
    for project, details in PROJECTS.items():
        with st.expander(project):
            st.write(details['description'])
            st.write(f"**Skills:** {', '.join(details['skills'])}")
            st.markdown(f"[Learn more]({details['link']})", unsafe_allow_html=True)
