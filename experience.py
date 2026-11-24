EXPERIENCE = """
Anes Džehverović, AI Engineer, based in Sarajevo, Bosnia and Herzegovina.

Profile:
AI Engineer with 3 years of experience building production LLM systems: multi-agent chatbots, semantic search
over millions of records, and AI evaluation and monitoring. Currently an AI engineer on a live data platform,
where my agent architecture powers four production chatbots. Alongside this, I lead AI research
projects, from agent frameworks that analyse codebases to AI tools for scientific research. I work daily with
Anthropic's Claude models and tooling, including the Claude API, Claude Code, MCP, agent skills and subagents.
A background in applied physics shapes how I test, measure and debug AI systems.

Employment history:

Nov 2024 - Present: AI Engineer, [Social Explorer](https://www.socialexplorer.com/), Sarajevo (hybrid)
AI engineer at a US demographic data platform serving universities, governments and businesses. I own the AI
stack end to end, working with a senior full-stack engineer whom I also trained in AI development.
- Multi-agent chatbot platform: built a model-agnostic data chatbot that searches, fetches and analyses census data,
  runs statistics and produces tables and charts. Forked it into specialist chatbots for each major product and
  connected all four to a base router chatbot that delegates questions, summarises answers and links users to the
  right assistant.
- Cost optimisation: lowered the cost of chatbot requests through prompt caching, selective context injection
  and routing work to cheaper models.
- Semantic search service: built a FastAPI service, now used across the whole Social Explorer stack, that finds
  metadata tables and geographies in Pinecone. Solved accurate retrieval across 13 million geography records using
  metadata filters, Microsoft AutoGen agent orchestration and Pydantic structured outputs.
- Data pipeline: built the pipeline that pulls metadata from AWS, cleans it and upserts it into the vector database.
- MCP tooling: exposed internal Python endpoints and native .NET application tools as MCP tools, rewriting the .NET
  endpoints in C#, so every chatbot can use them.
- SE Sentinel: built a monitoring system for all AI-powered apps that detects failures and wrong answers using
  decision models (TypeSafe Jev) and agents, and generates regression tests that rerun as a suite.
- Prompt and context engineering: own all prompt and context engineering across the company's AI products.

Nov 2023 - Present: AI Engineer, Independent Contractor, Remote
Contract AI engineering for startups and research clients, run alongside my main role. Several projects are under
NDA, so client details are limited.
- Lead AI Engineer (contract), AI research assistant (2025 - Present, under NDA): leading the build of an AI research
  assistant for an international biomedical research consortium. Ran an in-depth analysis of comparable systems
  (Google AI co-scientist, Claude Code and others) to inform the architecture. Own client communication and UAT
  presentations.
- Evaluation framework: built a dynamic framework that assembles evidence packages from systems and codebases and
  grades them against configurable question banks.
- Quor AI (2024, 3 months): built a complete FastAPI service that uses small LLMs to return structured outputs in
  under one second, using Pydantic for validation.
- AI research project, [BRUSA HyPower](https://www.brusahypower.com/) (2024, under NDA): built an LLM-agent framework
  for automated code review and unit test generation, and a data pipeline for building code datasets for model
  fine-tuning. Supervised by Prof. Amila Akagić, Faculty of Electrical Engineering, University of Sarajevo.
- Caze AI and Skylark AI (Nov 2023 - Jan 2025): backend and AI engineer for two sister startups in New York.
  Implemented AI features and built FastAPI endpoints for their products.

Aug 2023 - Jun 2024: Physics Teacher, [Richmond Park Education](https://secondary.rps.edu.ba/en/), Sarajevo
- Taught secondary school physics, turning complex concepts into clear, interactive lessons.

Mar 2023 - May 2023: Data Engineering Intern, [Symphony](https://symphony.is/), Sarajevo
- Processed and visualised data and built a custom plotting library. Built and containerised backend services and
  databases with Docker, and implemented machine learning models.

Jul 2022 - Aug 2022: Software Intern, EPICS Academy, [Cosylab](https://cosylab.com/), Ljubljana
Cosylab builds control systems for particle accelerators, lasers, fusion and other large scientific facilities.
- Final project: built a physics-based weather simulation and wrote control software for an air-conditioning unit,
  then connected it to real hardware.
- Trained in Linux, Git, SVN, Python, shell scripting, EPICS control software and project architecture.

Education:
- Oct 2023 - Present: Master's degree, Applied Physics, [University of Sarajevo](https://fizika.pmf.unsa.ba/).
  Coursework complete; thesis defence pending.
- Sep 2018 - Jan 2023: Bachelor's degree, Applied Physics, [University of Sarajevo](https://fizika.pmf.unsa.ba/).

Certifications:
- Anthropic Education, Oct 2026: Building with the Claude API, Introduction to Model Context Protocol,
  Model Context Protocol: Advanced Topics, Claude with Amazon Bedrock.
- Anthropic Education, Jul 2026: Claude Code 101, Claude 101.

Skills:
- AI and LLM engineering: multi-agent systems, agent orchestration, RAG, embeddings and semantic search, prompt and
  context engineering, structured outputs, MCP, LLM evaluation and monitoring, training dataset curation,
  cost optimisation
- Agent frameworks: Claude Agent SDK, OpenAI Agents SDK, Microsoft AutoGen, LangGraph, LangChain, LlamaIndex, CrewAI
- Anthropic ecosystem (daily use): Claude models and API, Claude Code, MCP, agent skills, subagents,
  Claude on Amazon Bedrock
- Other models and providers: OpenAI, Groq, Hugging Face (models, embeddings), Llama, decision models (Jev)
- Machine learning and data: Pandas, NumPy, SciPy, scikit-learn, Matplotlib, Plotly, data pipelines,
  web scraping (BeautifulSoup, Playwright)
- Backend: Python (async), FastAPI, Pydantic, SQLAlchemy, WebSockets and streaming responses, C# / .NET, Streamlit
- Databases: PostgreSQL, Redis, SQL, Pinecone, Weaviate
- DevOps and testing: Docker, AWS, GitHub Actions, Git, Linux, shell scripting, pytest, LangSmith
- Frontend (basic): TypeScript, Node.js

Languages: Bosnian (native), English (fluent), German (B2)

References: Prof. Amila Akagić, PhD, Faculty of Electrical Engineering, University of Sarajevo
"""
