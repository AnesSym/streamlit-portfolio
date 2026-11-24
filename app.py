from pathlib import Path
import base64
import html
import re

import anthropic
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="Anes Džehverović | AI Engineer",
    page_icon=str(ROOT / "assets" / "Untitled.png"),
    layout="centered",
)

from config import (  # noqa: E402  (page config must run first)
    NAME, LOCATION, EMAIL, SOCIAL_MEDIA, RIGHT_NOW, SUGGESTED_QUESTIONS,
    ABOUT_SUBTITLE, ABOUT_DESCRIPTION, ABOUT_INTERESTS, JOURNEY, QUALIFICATIONS,
    SKILL_GROUPS, WORK_HISTORY, EDUCATION, CERTIFICATIONS, PROJECTS,
    CHAT_MODEL, CHAT_EFFORT, MAX_TOKENS, CONVERSATIONAL_MEMORY_LENGTH, get_system_prompt,
)
from experience import EXPERIENCE  # noqa: E402
from email_sender import send_email  # noqa: E402

# Served by Streamlit static file serving (server.enableStaticServing in .streamlit/config.toml)
RESUME_URL = "app/static/Anes_Dzehverovic-CV.pdf"
AVATAR_FILE = ROOT / "assets" / "Untitled.png"

st.html(ROOT / "styles" / "main.css")
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("user_name", None)
st.session_state.setdefault("welcome_form_completed", False)


# ---------- Small helpers ----------
@st.cache_data
def data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def esc(text) -> str:
    return html.escape(str(text))


def show(markup: str):
    """Render a block of trusted HTML. Kept on one line so markdown never reinterprets it."""
    st.markdown(markup.replace("\n", " "), unsafe_allow_html=True)


def label(text: str):
    show(f'<div class="label section-label">{esc(text)}</div>')


def page_header(kicker: str, title: str, lede: str = ""):
    lede_html = f'<p class="lede">{esc(lede)}</p>' if lede else ""
    show(f'<div class="page-head"><div class="label">{esc(kicker)}</div>'
         f'<div class="page-title">{esc(title)}</div>{lede_html}</div>')


def chips(items, small=False) -> str:
    return f'<div class="chips{" small" if small else ""}">' + "".join(
        f'<span class="chip">{esc(i)}</span>' for i in items) + "</div>"


def points(items) -> str:
    # Items may contain <b> emphasis from config, so they are trusted HTML.
    return '<ul class="points">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------- Thinking orb (thinking-orbs engine by Libraries.dev, MIT) ----------
ORB_JS = """
export default function (component) {
  const { parentElement, data } = component;
  const canvas = parentElement.querySelector("canvas");
  const size = (data && data.size) || 20;
  let raf = 0;
  let stopped = false;

  (async () => {
    try {
      const engine = await import("https://cdn.jsdelivr.net/npm/thinking-orbs@0.3.2/dist/engine.es.js");
      if (stopped) return;
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      canvas.width = Math.round(size * dpr);
      canvas.height = Math.round(size * dpr);
      const ctx = canvas.getContext("2d");
      const { mode, speed, opts } = engine.resolvePreset((data && data.state) || "working", size);
      const frameFn = engine.MODE_FRAMES[mode];
      const tint = data && data.tint;
      const draw = (t) => {
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, size, size);
        engine.paintFrame(ctx, frameFn(size, t, opts), true, tint);
      };
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        draw(0.6);
        return;
      }
      const loop = () => {
        if (stopped) return;
        draw((performance.now() / 1000) * speed);
        raf = requestAnimationFrame(loop);
      };
      loop();
    } catch (err) {
      parentElement.querySelector(".orb").classList.add("fallback");
    }
  })();

  return () => {
    stopped = true;
    cancelAnimationFrame(raf);
  };
}
"""

ORB_CSS = """
.orb { display: flex; align-items: center; gap: 10px; padding: 4px 0; font-family: 'IBM Plex Sans', sans-serif; }
.orb canvas { width: 20px; height: 20px; }
.orb span { font-size: 14.5px; color: #959ba1; }
.orb.fallback canvas { border-radius: 50%; border: 2px dotted #6cc79a; animation: spin 1.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .orb.fallback canvas { animation: none; } }
"""


@st.cache_resource
def orb_component():
    return st.components.v2.component(
        "thinking_orb",
        html='<div class="orb" role="status"><canvas aria-hidden="true"></canvas><span>Thinking…</span></div>',
        css=ORB_CSS,
        js=ORB_JS,
    )


def thinking_orb():
    orb_component()(data={"state": "working", "size": 20, "tint": {"r": 108, "g": 199, "b": 154}})


# ---------- Page links inside chat replies ----------
# The chatbot links pages as markdown, e.g. [Work history](work). A normal link would reload the app and start
# a new session (welcome screen again, chat lost), so this component catches clicks on those links and asks
# Python to switch pages in place.
LINK_CATCHER_JS = """
export default function (component) {
  const { data, setTriggerValue } = component;
  const pages = new Set((data && data.pages) || []);
  const onClick = (event) => {
    const link = event.target.closest && event.target.closest("a[href]");
    if (!link || !link.closest('[class*="st-key-reply-"]')) return;
    const url = new URL(link.getAttribute("href"), window.location.href);
    if (url.origin !== window.location.origin) return;
    const slug = url.pathname.split("/").filter(Boolean).pop() || "";
    if (!pages.has(slug)) return;
    event.preventDefault();
    event.stopPropagation();
    setTriggerValue("go", slug);
  };
  document.addEventListener("click", onClick, true);
  return () => document.removeEventListener("click", onClick, true);
}
"""


@st.cache_resource
def link_catcher_component():
    return st.components.v2.component("reply_page_links", html="<span hidden></span>", js=LINK_CATCHER_JS)


def follow_reply_links():
    """Mount the click catcher; if a page link in a reply was clicked, go to that page."""
    result = link_catcher_component()(
        key="page-link-catcher",
        data={"pages": [p.url_path for p in PAGES.values()]},
        on_go_change=lambda: None,
    )
    slug = getattr(result, "go", None)
    if slug:
        if slug == PAGES["home"].url_path:
            st.session_state["chat_open"] = False
        st.switch_page(next(p for p in PAGES.values() if p.url_path == slug))


def linkify_pages(text: str) -> str:
    """Turn bolded page names (**Work history**) into page links, in case the model bolds instead of linking."""
    for page in PAGES.values():
        text = re.sub(rf"\*\*{re.escape(page.title)}\*\*", f"[{page.title}]({page.url_path})", text, flags=re.I)
    return text


# ---------- Claude ----------
@st.cache_resource
def get_claude_client():
    # Reads ANTHROPIC_API_KEY from the environment (.env locally, config vars on Heroku)
    return anthropic.Anthropic()


def build_api_messages(history):
    """The last CONVERSATIONAL_MEMORY_LENGTH exchanges plus the new question, starting on a user turn."""
    recent = history[-(CONVERSATIONAL_MEMORY_LENGTH * 2 + 1):]
    while recent and recent[0]["role"] != "user":
        recent = recent[1:]
    return [{"role": m["role"], "content": m["content"]} for m in recent]


def stream_claude_reply(messages):
    """Stream Claude's reply under the question. Returns the reply text, or None if the request failed."""
    system_prompt = get_system_prompt(EMAIL, SOCIAL_MEDIA, EXPERIENCE, st.session_state["user_name"])
    with st.container(key="reply-live"):
        slot = st.empty()
        with slot.container():
            thinking_orb()

        def fail(message):
            slot.markdown(f'<p class="chat-error">{esc(message)}</p>', unsafe_allow_html=True)

        text = ""
        try:
            with get_claude_client().messages.stream(
                model=CHAT_MODEL,
                max_tokens=MAX_TOKENS,
                output_config={"effort": CHAT_EFFORT},
                system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
                messages=messages,
            ) as stream:
                for chunk in stream.text_stream:
                    text += chunk
                    slot.markdown(linkify_pages(text) + " ▍")
                final = stream.get_final_message()
        except anthropic.AuthenticationError:
            print("Claude API error: invalid or missing ANTHROPIC_API_KEY")
            fail("The chat isn't available right now. You can still reach me through the Contact page.")
            return None
        except anthropic.RateLimitError:
            fail("Too many questions at once. Try again in a minute.")
            return None
        except (anthropic.APIStatusError, anthropic.APIConnectionError) as e:
            print(f"Claude API error: {e!r}")
            fail("The reply didn't come through. Try sending your question again.")
            return None

        if final.stop_reason == "refusal":
            text = "I can't help with that one. Ask me about my work, skills or projects instead."
        elif final.stop_reason == "max_tokens":
            text += "\n\n_My answer got cut short. Ask me to continue._"
        elif not text:
            text = "I didn't catch that. Could you rephrase your question?"

        slot.markdown(linkify_pages(text))
        return text


# ---------- Pages ----------
def ask_page():
    follow_reply_links()
    history = st.session_state["chat_history"]
    with st.bottom:  # docked at the bottom of the page, the note sits right under the input
        typed = st.chat_input("Ask about my work, projects or skills…")
        show('<div class="chat-footnote">Answers come from my CV and can be outdated.</div>')
    question = typed or st.session_state.pop("pending_question", None)
    if question:
        st.session_state["chat_open"] = True

    # The landing and the conversation live in separate slots. Streamlit only removes leftovers from the
    # previous run when a run ends, and this run streams for a while. Replacing the landing slot with an
    # empty element removes the landing at once; reusing one container would keep its old children around.
    landing_slot = st.empty()
    chat_slot = st.empty()
    if not st.session_state.get("chat_open"):
        with landing_slot.container(key="view-landing"):
            render_landing()
        return

    landing_slot.empty()
    with chat_slot.container(key="view-chat"):
        render_conversation(history, question)


def render_conversation(history, question):
    for i, msg in enumerate(history):
        render_message(msg, i)

    if question:
        history.append({"role": "user", "content": question})
        render_message(history[-1], len(history) - 1)
        reply = stream_claude_reply(build_api_messages(history))
        if reply is None:
            history.pop()  # keep the history alternating user/assistant
        else:
            history.append({"role": "assistant", "content": reply})
            st.session_state["chat_history"] = history[-20:]
            st.rerun()


def render_landing():
    name = st.session_state["user_name"]
    greeting = f"Hi {esc(name)}. What would you like to know?" if name else "Hi. What would you like to know?"
    show(
        f'<div class="hero"><img class="avatar" src="{data_uri(AVATAR_FILE)}" alt="Pixel-art portrait of Anes">'
        f'<div><div class="page-title">{greeting}</div>'
        f'<p class="lede">I\'m {esc(NAME)}, an AI engineer in Sarajevo. Ask me anything about my work; '
        f'this chat answers from my CV.</p></div></div>'
    )
    show(f'<div class="note"><span class="note-mark"></span><div><b>Right now:</b> {esc(RIGHT_NOW)}</div></div>')

    # Coming back to the start keeps the conversation; offer a way back into it.
    asked = sum(m["role"] == "user" for m in st.session_state["chat_history"])
    if asked:
        with st.container(border=True, key="resume-chat"):
            text_col, button_col = st.columns([5, 1], vertical_alignment="center")
            text_col.markdown(
                f'<div class="resume-text"><b>Your conversation is still here.</b> '
                f'{asked} question{"s" if asked != 1 else ""} so far.</div>', unsafe_allow_html=True)
            if button_col.button("Continue", key="resume-button", type="primary", width="stretch"):
                st.session_state["chat_open"] = True
                st.rerun()

    label("Try asking")
    cols = st.columns(2, gap="small")
    for i, q in enumerate(SUGGESTED_QUESTIONS):
        if cols[i % 2].button(q, key=f"suggest-{i}", width="stretch"):
            st.session_state["pending_question"] = q
            st.rerun()

    label("Explore")
    cols = st.columns(3, gap="small")
    for col, (page, blurb) in zip(cols, [
        (PAGES["about"], "Background, focus areas and how I got here"),
        (PAGES["work"], "Social Explorer, contract work, teaching and internships"),
        (PAGES["projects"], "Chatbots, semantic search, monitoring and research tools"),
    ]):
        with col.container(border=True, key=f"explore-{page.url_path}"):
            show(f'<div class="card-title">{esc(page.title)}</div>'
                 f'<p class="lede" style="font-size:14px;margin-top:4px">{esc(blurb)}</p>')
            st.page_link(page, label="Open")


def render_message(msg, index):
    if msg["role"] == "user":
        show(f'<div class="msg-user"><div class="bubble">{esc(msg["content"])}</div></div>')
    else:
        with st.container(key=f"reply-{index}"):
            st.markdown(linkify_pages(msg["content"]))


def about_page():
    page_header("About", "About me", ABOUT_SUBTITLE)
    show(f'<p class="prose">{esc(ABOUT_DESCRIPTION)}</p>')

    label("What I focus on")
    show('<div class="cards">' + "".join(
        f'<div class="card"><div class="label">{esc(q["badge"])}</div>'
        f'<div class="card-title">{esc(q["title"])}</div>'
        f'<ul>{"".join(f"<li>{esc(p)}</li>" for p in q["points"])}</ul></div>'
        for q in QUALIFICATIONS) + "</div>")

    label("How I got here")
    show('<div class="rows">' + "".join(
        f'<div class="row compact"><div class="period">{esc(period)}</div>'
        f'<div class="row-text" style="margin:0">{esc(event)}</div></div>'
        for period, event in JOURNEY) + "</div>")

    label("Outside of work")
    show(chips(ABOUT_INTERESTS))


def work_page():
    page_header("Work history", "Where I've worked",
                "From physics internships and teaching to running production AI systems.")
    rows = []
    for job in WORK_HISTORY:
        role, _, place = job["title"].partition(" | ")
        summary = f'<div class="row-text">{esc(job["summary"])}</div>' if job["summary"] else ""
        rows.append(
            f'<div class="row"><div class="period">{esc(job["period"])}</div><div>'
            f'<div class="row-title">{esc(role)}</div><div class="row-sub">{esc(place)}</div>'
            f'{summary}{points(job["points"])}</div></div>'
        )
    show('<div class="rows">' + "".join(rows) + "</div>")


def projects_page():
    page_header("Projects", "Things I've built",
                "Production systems at Social Explorer, contract and research work, and an earlier web app. "
                "Some client work is under NDA, so details are limited.")
    cards = []
    for title, details in PROJECTS.items():
        name, _, org = title.partition(" | ")
        link = details["link"]
        visit = f'<a href="{esc(link)}" target="_blank" rel="noopener">Visit</a>' if link and link != "#" else ""
        cards.append(
            f'<div class="card"><div class="label">{esc(org or "Project")}</div>'
            f'<div class="card-title">{esc(name)}</div><p>{esc(details["description"])}</p>'
            f'<div class="card-foot">{chips(details["skills"], small=True)}{visit}</div></div>'
        )
    show('<div class="cards">' + "".join(cards) + "</div>")


def skills_page():
    page_header("Skills", "What I work with",
                "Grouped the way I use them. I work daily with Anthropic's Claude models and tooling.")
    show('<div class="rows">' + "".join(
        f'<div class="row"><div class="period">{esc(group)}</div><div>{chips(items)}</div></div>'
        for group, items in SKILL_GROUPS.items()) + "</div>")


def education_page():
    page_header("Education", "Education and certifications")
    rows = []
    for e in EDUCATION:
        degree, _, school = e["degree"].partition(" | ")
        rows.append(
            f'<div class="row"><div class="period">{esc(e["period"])}</div><div>'
            f'<div class="row-title">{esc(degree)}</div><div class="row-sub">{esc(school)}</div>'
            f'<div class="row-text">{esc(e["description"])}</div></div></div>'
        )
    show('<div class="rows">' + "".join(rows) + "</div>")

    label("Certifications")
    show('<div class="rows">' + "".join(
        f'<div class="row"><div class="period">{esc(c["period"])}</div><div>'
        f'<div class="row-title">{esc(c["issuer"])}</div>{points([esc(i) for i in c["items"]])}</div></div>'
        for c in CERTIFICATIONS) + "</div>")


def contact_page():
    page_header("Contact", "Send me a message",
                f"I read every message and reply by email. You can also write to me directly at {EMAIL}.")
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        sender_name = col1.text_input("Your name", value=st.session_state["user_name"] or "")
        sender_email = col2.text_input("Your email", placeholder="you@example.com")
        message = st.text_area("Message", height=150, placeholder="Hi Anes, I'd like to talk about…")
        submitted = st.form_submit_button("Send message", type="primary")

    if submitted:
        if not (sender_name.strip() and sender_email.strip() and message.strip()):
            st.toast("Fill in your name, email and message to send it.")
        else:
            with st.spinner("Sending…"):
                ok, result = send_email(sender_name.strip(), sender_email.strip(), message.strip())
            if ok:
                st.toast("Message sent. I'll reply to the email you gave.")
            else:
                print(f"Contact form error: {result}")
                st.toast("Your message wasn't sent. Check your email address, or email me directly.")

    show('<p class="lede" style="font-size:13px;margin-top:18px">Your message goes straight to my inbox '
         'through Gmail. Nothing is stored on this site.</p>')


# ---------- Welcome (asks the visitor's name once) ----------
def welcome_screen():
    show(
        f'<div class="welcome"><img class="avatar" src="{data_uri(AVATAR_FILE)}" alt="Pixel-art portrait of Anes">'
        f'<div class="page-title">Hi, I\'m Anes.</div>'
        f'<p class="lede">I build AI systems. What should I call you? '
        f'My chat assistant will greet you by name.</p></div>'
    )
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        with st.form("welcome_form", border=False):
            name = st.text_input("Your name", placeholder="Your name", label_visibility="collapsed")
            c1, c2 = st.columns(2)
            go = c1.form_submit_button("Continue", type="primary", use_container_width=True)
            skip = c2.form_submit_button("Skip", use_container_width=True)
    if go or skip:
        visitor = name.strip()[:40] if go else ""
        st.session_state["user_name"] = visitor or None
        st.session_state["welcome_form_completed"] = True
        st.rerun()


# ---------- Navigation ----------
PAGES = {
    "home": st.Page(ask_page, title="Home", icon=":material/home:", url_path="home", default=True),
    "about": st.Page(about_page, title="About me", icon=":material/person:", url_path="about"),
    "work": st.Page(work_page, title="Work history", icon=":material/work_history:", url_path="work"),
    "projects": st.Page(projects_page, title="Projects", icon=":material/deployed_code:", url_path="projects"),
    "skills": st.Page(skills_page, title="Skills", icon=":material/build:", url_path="skills"),
    "education": st.Page(education_page, title="Education", icon=":material/school:", url_path="education"),
    "contact": st.Page(contact_page, title="Contact", icon=":material/mail:", url_path="contact"),
}

if not st.session_state["welcome_form_completed"]:
    welcome_screen()
    st.stop()

# Built-in nav is hidden so the profile can sit above the page links in the sidebar.
nav = st.navigation(list(PAGES.values()), position="hidden")

# Contact links and the CV, shown under the name in the sidebar.
ICONS = {
    "LinkedIn": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.23 0z"/></svg>',
    "GitHub": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.23c-3.34.73-4.04-1.42-4.04-1.42-.55-1.39-1.33-1.76-1.33-1.76-1.09-.74.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.49 1 .11-.78.42-1.31.76-1.6-2.67-.31-5.47-1.34-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.65 1.66.24 2.88.12 3.18.77.84 1.23 1.91 1.23 3.22 0 4.61-2.81 5.62-5.48 5.92.43.37.82 1.1.82 2.22v3.29c0 .32.19.7.8.58A12 12 0 0 0 12 0z"/></svg>',
    "Email": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>',
    "CV": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M5 20h14"/></svg>',
}
contact_links = "".join(
    f'<a class="icon" href="{esc(d["url"])}" target="_blank" rel="noopener" title="{p}" aria-label="{p}">{ICONS[p]}</a>'
    for p, d in SOCIAL_MEDIA.items()
)
contact_links += f'<a class="icon" href="mailto:{esc(EMAIL)}" title="{esc(EMAIL)}" aria-label="Email {esc(EMAIL)}">{ICONS["Email"]}</a>'
contact_links += f'<a href="{RESUME_URL}" download="{RESUME_URL.rsplit("/", 1)[-1]}">{ICONS["CV"]}<span>CV</span></a>'

with st.sidebar:
    show(
        f'<div class="side-profile"><div class="side-name">{esc(NAME)}</div>'
        f'<div class="side-role">AI Engineer · {esc(LOCATION.split(",")[0])}</div>'
        f'<nav class="contact-row" aria-label="Contact links">{contact_links}</nav></div>'
    )
    # Home is a button rather than a page link so it also works from inside a conversation:
    # it always returns to the start screen (the conversation is kept and can be continued).
    on_home = nav.url_path == PAGES["home"].url_path
    if st.button("Home", icon=":material/home:", key="nav-home-active" if on_home else "nav-home", width="stretch"):
        st.session_state["chat_open"] = False
        st.switch_page(PAGES["home"])
    for key, page in PAGES.items():
        if key != "home":
            st.page_link(page)


nav.run()
