# --- GENERAL SETTINGS ---
PAGE_TITLE = "Anes Džehverović | AI Engineer"
NAME = "Anes Džehverović"
ROLE = "AI Engineer · Multi-agent & LLM systems · Applied physicist"
LOCATION = "Sarajevo, Bosnia and Herzegovina"

EMAIL = "anesdzehverovic@gmail.com"

SOCIAL_MEDIA = {
    "LinkedIn": {"url": "https://www.linkedin.com/in/anes-dzehverovic-63aa4421b/"},
    "GitHub": {"url": "https://github.com/AnesSym/"},
}

# --- CHAT LANDING ---
RIGHT_NOW = (
    "I'm an AI engineer at Social Explorer, where my agent architecture runs "
    "four production chatbots on a US demographic data platform."
)

SUGGESTED_QUESTIONS = [
    "What does your multi-agent chatbot platform do?",
    "How do you keep your chatbots fast and affordable?",
    "What are you building as an independent contractor?",
    "How does physics shape the way you build AI?",
]

# --- ABOUT ME ---
ABOUT_SUBTITLE = (
    "AI Engineer building production LLM systems: multi-agent chatbots, "
    "semantic search and AI evaluation"
)

ABOUT_DESCRIPTION = (
    "I'm an AI Engineer with 3 years of experience building production LLM systems: multi-agent chatbots, "
    "semantic search over millions of records, and AI evaluation and monitoring. I'm currently an AI "
    "engineer at Social Explorer, where my agent architecture powers four production chatbots. "
    "Alongside this, I lead AI research projects, from agent frameworks that analyse codebases to AI tools for "
    "scientific research. I work daily with Anthropic's Claude models and tooling: the Claude API, Claude Code, "
    "MCP, agent skills and subagents. My background in applied physics shapes how I test, measure and debug AI systems."
)

ABOUT_INTERESTS = [
    "Problem Solving", "Continuous Learning", "Physics & Research",
    "Mentoring", "Innovation", "Teaching",
]

# (period, event) pairs for the "My Journey" timeline, newest first
JOURNEY = [
    ("2024 - Present", "AI Engineer at Social Explorer: multi-agent chatbots, semantic search and AI monitoring"),
    ("2023 - Present", "Independent AI contractor: research assistant for a biomedical consortium, Quor AI, BRUSA HyPower, Caze AI, Skylark AI"),
    ("2023 - 2024", "Physics Teacher at Richmond Park Education, Sarajevo"),
    ("2023 - Present", "Master's in Applied Physics, University of Sarajevo (thesis defence pending)"),
    ("2022 - 2023", "Internships at Cosylab (EPICS Academy) and Symphony"),
    ("2018 - 2023", "Bachelor's in Applied Physics, University of Sarajevo"),
]

# --- ABOUT: FOCUS AREAS ---
QUALIFICATIONS = [
    {
        "title": "AI & LLM Engineering",
        "points": [
            "Multi-agent chatbot platform with a router and four specialist assistants",
            "Semantic search across 13 million records with Pinecone and AutoGen",
            "Prompt and context engineering across every AI product at Social Explorer",
        ],
        "badge": "3 Years Experience",
    },
    {
        "title": "Evaluation, Monitoring & Cost",
        "points": [
            "SE Sentinel: detects failures and wrong answers with decision models and agents",
            "Evaluation framework that grades systems against configurable question banks",
            "Kept chatbots affordable with prompt caching and model routing",
        ],
        "badge": "Production Focus",
    },
    {
        "title": "Research & Leadership",
        "points": [
            "Lead AI Engineer on a research assistant for a biomedical research consortium",
            "Own client communication and UAT presentations",
            "Trained a senior full-stack engineer in AI development",
        ],
        "badge": "Lead Role",
    },
    {
        "title": "Physics & Teaching",
        "points": [
            "Master's in Applied Physics (coursework complete, thesis defence pending)",
            "Taught secondary school physics with clear, interactive lessons",
            "Scientific approach to testing, measuring and debugging AI systems",
        ],
        "badge": "Applied Physicist",
    },
]

# --- SKILLS ---
SKILL_GROUPS = {
    "AI & LLM Engineering": [
        "Multi-Agent Systems", "Agent Orchestration", "RAG", "Embeddings & Semantic Search",
        "Prompt & Context Engineering", "Structured Outputs", "MCP", "LLM Evaluation & Monitoring",
        "Training Dataset Curation", "Cost Optimisation",
    ],
    "Agent Frameworks": [
        "Claude Agent SDK", "OpenAI Agents SDK", "Microsoft AutoGen", "LangGraph", "LangChain",
        "LlamaIndex", "CrewAI",
    ],
    "Anthropic Ecosystem (daily use)": [
        "Claude Models & API", "Claude Code", "MCP", "Agent Skills", "Subagents", "Claude on Amazon Bedrock",
    ],
    "Other Models & Providers": [
        "OpenAI", "Groq", "Hugging Face", "Llama", "Decision Models (Jev)",
    ],
    "Machine Learning & Data": [
        "Pandas", "NumPy", "SciPy", "scikit-learn", "Matplotlib", "Plotly", "Data Pipelines",
        "BeautifulSoup", "Playwright",
    ],
    "Backend": [
        "Python (async)", "FastAPI", "Pydantic", "SQLAlchemy", "WebSockets & Streaming", "C# / .NET", "Streamlit",
    ],
    "Databases": ["PostgreSQL", "Redis", "SQL", "Pinecone", "Weaviate"],
    "DevOps & Testing": [
        "Docker", "AWS", "GitHub Actions", "Git", "Linux", "Shell Scripting", "pytest", "LangSmith",
    ],
    "Frontend (basic)": ["TypeScript", "Node.js"],
    "Languages": ["Bosnian (native)", "English (fluent)", "German (B2)"],
}

# --- WORK HISTORY ---
WORK_HISTORY = [
    {
        "title": "AI Engineer | Social Explorer - Sarajevo (hybrid)",
        "period": "11/2024 - Present",
        "summary": "AI engineer at a US demographic data platform serving universities, governments and "
                   "businesses. I own the AI stack end to end.",
        "points": [
            "<b>Multi-agent chatbot platform:</b> model-agnostic data chatbot that searches, fetches and analyses census data, forked into specialist chatbots and connected to a base router chatbot",
            "<b>Cost optimisation:</b> lowered the cost of every chatbot request through prompt caching, selective context injection and model routing",
            "<b>Semantic search service:</b> FastAPI service used across the whole stack, accurate retrieval across 13M geography records in Pinecone",
            "<b>Data pipeline:</b> pulls metadata from AWS, cleans it and upserts it into the vector database",
            "<b>MCP tooling:</b> exposed Python endpoints and native .NET tools (rewritten in C#) as MCP tools for every chatbot",
            "<b>SE Sentinel:</b> monitoring for all AI apps using decision models (TypeSafe Jev) and agents, with generated regression tests",
            "<b>Prompt and context engineering</b> across the company's AI products",
        ],
    },
    {
        "title": "AI Engineer | Independent Contractor - Remote",
        "period": "11/2023 - Present",
        "summary": "Contract AI engineering for startups and research clients, alongside my main role. "
                   "Several projects are under NDA.",
        "points": [
            "<b>Lead AI Engineer</b> on an AI research assistant for an international biomedical research consortium (2025 - Present, NDA)",
            "<b>Evaluation framework</b> that assembles evidence packages from systems and codebases and grades them against question banks",
            "<b>Quor AI</b> (2024): FastAPI service returning structured outputs from small LLMs in under one second",
            "<b>BRUSA HyPower</b> (2024, NDA): LLM-agent framework for code review and unit test generation, plus a fine-tuning dataset pipeline",
            "<b>Caze AI and Skylark AI</b> (11/2023 - 01/2025): backend and AI engineer for two New York startups",
        ],
    },
    {
        "title": "Physics Teacher | Richmond Park Education - Sarajevo",
        "period": "08/2023 - 06/2024",
        "summary": "",
        "points": ["Taught secondary school physics, turning complex concepts into clear, interactive lessons"],
    },
    {
        "title": "Data Engineering Intern | Symphony - Sarajevo",
        "period": "03/2023 - 05/2023",
        "summary": "",
        "points": [
            "Processed and visualised data and built a custom plotting library",
            "Built and containerised backend services and databases with Docker, and implemented ML models",
        ],
    },
    {
        "title": "Software Intern, EPICS Academy | Cosylab - Ljubljana",
        "period": "07/2022 - 08/2022",
        "summary": "Cosylab builds control systems for particle accelerators, lasers, fusion and other large "
                   "scientific facilities.",
        "points": [
            "<b>Final project:</b> physics-based weather simulation and control software for an air-conditioning unit, connected to real hardware",
            "Trained in Linux, Git, SVN, Python, shell scripting, EPICS control software and project architecture",
        ],
    },
]

# --- EDUCATION ---
EDUCATION = [
    {
        "degree": "Master's degree, Applied Physics | University of Sarajevo",
        "period": "Oct 2023 - Present",
        "description": "Coursework complete; thesis defence pending.",
    },
    {
        "degree": "Bachelor's degree, Applied Physics | University of Sarajevo",
        "period": "Sep 2018 - Jan 2023",
        "description": "Built strong problem-solving, analytical and programming skills.",
    },
]

CERTIFICATIONS = [
    {
        "issuer": "Anthropic Education",
        "period": "Oct 2026",
        "items": [
            "Building with the Claude API", "Introduction to Model Context Protocol",
            "Model Context Protocol: Advanced Topics", "Claude with Amazon Bedrock",
        ],
    },
    {
        "issuer": "Anthropic Education",
        "period": "Jul 2026",
        "items": ["Claude Code 101", "Claude 101"],
    },
]

# --- PROJECT DATA ---
PROJECTS = {
    "Multi-Agent Chatbot Platform | Social Explorer": {
        "link": "https://www.socialexplorer.com/",
        "description": "Built a model-agnostic data chatbot that searches, fetches and analyses census data, runs statistics and produces tables and charts. Forked it into specialist chatbots for each major product and connected all four to a base router chatbot that delegates questions, summarises answers and links users to the right assistant. Lowered the cost of each request through prompt caching, selective context injection and routing work to cheaper models.",
        "skills": ["Python", "Multi-Agent Systems", "Prompt Caching", "MCP", "Context Engineering"]
    },
    "Semantic Search Service | Social Explorer": {
        "link": "https://www.socialexplorer.com/",
        "description": "Built a FastAPI service, now used across the whole Social Explorer stack, that finds metadata tables and geographies in Pinecone. Solved accurate retrieval across 13 million geography records using metadata filters, Microsoft AutoGen agent orchestration and Pydantic structured outputs. Includes the pipeline that pulls metadata from AWS, cleans it and upserts it into the vector database.",
        "skills": ["Python", "FastAPI", "Pinecone", "AutoGen", "Pydantic", "AWS"]
    },
    "SE Sentinel | AI Monitoring": {
        "link": "https://www.socialexplorer.com/",
        "description": "A monitoring system for all AI-powered apps at Social Explorer. It detects failures and wrong answers using decision models (TypeSafe Jev) and agents, and generates regression tests that rerun as a suite.",
        "skills": ["LLM Evaluation", "Decision Models", "Agents", "Regression Testing"]
    },
    "MCP Tooling | Social Explorer": {
        "link": "https://www.socialexplorer.com/",
        "description": "Exposed internal Python endpoints and native .NET application tools as MCP tools, rewriting the .NET endpoints in C#, so every chatbot can use them.",
        "skills": ["MCP", "Python", "C# / .NET"]
    },
    "AI Research Assistant | Biomedical Research Consortium (NDA)": {
        "link": "#",
        "description": "Leading the build of an AI research assistant for an international biomedical research consortium as Lead AI Engineer (contract). Ran an in-depth analysis of comparable systems (Google AI co-scientist, Claude Code and others) to inform the architecture. Own client communication and UAT presentations.",
        "skills": ["Agent Architecture", "Research", "Client Communication"]
    },
    "AI Evaluation Framework": {
        "link": "#",
        "description": "Built a dynamic framework that assembles evidence packages from systems and codebases and grades them against configurable question banks.",
        "skills": ["LLM Evaluation", "Python", "Agents"]
    },
    "Structured-Output LLM Service | Quor AI": {
        "link": "https://www.linkedin.com/company/quor-ai/",
        "description": "Built a complete FastAPI service that uses small LLMs to return structured outputs in under one second, using Pydantic for validation.",
        "skills": ["Python", "FastAPI", "Pydantic", "Groq"]
    },
    "Code Review & Unit Test Agents | BRUSA HyPower (NDA)": {
        "link": "https://www.brusahypower.com/",
        "description": "Built an LLM-agent framework for automated code review and unit test generation, and a data pipeline for building code datasets for model fine-tuning. Supervised by Prof. Amila Akagić, Faculty of Electrical Engineering, University of Sarajevo.",
        "skills": ["Python", "LLM Agents", "Dataset Curation", "Fine-Tuning Data"]
    },
    "Physics-Based Weather Simulation | Cosylab EPICS Academy": {
        "link": "https://cosylab.com/",
        "description": "Final project at Cosylab: built a physics-based weather simulation and wrote control software for an air-conditioning unit, then connected it to real hardware.",
        "skills": ["Python", "EPICS", "Linux", "Control Software"]
    },
    "Dental Management System | MasterLab": {
        "link": "#",
        "description": "Created a full web app for a dental technician firm using the Flask framework and deployed it on Heroku. The system manages dental operations efficiently.",
        "skills": ["Flask", "Python", "PostgreSQL", "Heroku"]
    },
}

# --- AI CONFIGURATION ---
CHAT_MODEL = "claude-haiku-5-5"
CHAT_EFFORT = "low"  # chat replies are short; low effort keeps them fast and cheap
MAX_TOKENS = 8000
CONVERSATIONAL_MEMORY_LENGTH = 5  # number of previous user/assistant exchanges sent with each question


def get_system_prompt(email, social_media, experience, user_name=None):
    # Stable instructions come first so the prompt prefix can be cached; the visitor's name goes last.
    prompt = f"""You are Anes Džehverović, answering visitors' questions on your own portfolio website. Speak in the first person, as Anes. Keep answers concise and friendly, and use markdown when a list helps.

Only answer questions about Anes: his experience, skills, projects, education and how to contact him. Questions about physics are also fine. Politely decline anything else, and don't share personal-life details beyond what is listed here.

Only state facts that appear in the information below. If something isn't covered, say you'd be happy to discuss it and point the visitor to the [Contact](contact) page. Some contract work is under NDA, so don't invent client details for it.

Contact details:
- phone: +387 60 33 59 406
- email: {email}
- GitHub and LinkedIn: {social_media}
- The CV can be downloaded with the "Download CV" button in the sidebar.
- Visitors can message Anes on the [Contact](contact) page.

Pages on this site (in the sidebar), with their link paths: Home (home, the start page where this chat lives), About me (about), Work history (work), Projects (projects), Skills (skills), Education (education), Contact (contact). When you point a visitor to a page, link it in markdown with its path, for example [Work history](work) or [Contact](contact). Don't bold page names, and only link pages from this list.

If asked who built this portfolio: you did, with Streamlit, and this chat runs on Claude Haiku 5.5 through the Anthropic API.

Information about Anes:
{experience}"""

    if user_name:
        prompt += f"\n\nThe visitor's name is {user_name}. Use it naturally now and then, for example when greeting them."
    return prompt
