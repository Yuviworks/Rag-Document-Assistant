import streamlit as st
import requests
from datetime import datetime

# Page Config

st.set_page_config(
    page_title="Technical Documentation Assistant",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="expanded"
)

FASTAPI_URL = "http://127.0.0.1:8000"

# Design tokens


INK        = "#0b0e14"
PANEL      = "#12161f"
PANEL_2    = "#171c27"
BORDER     = "#242b38"
TEXT       = "#e6e9ef"
MUTED      = "#8891a3"
AMBER      = "#e8a33d"
AMBER_DIM  = "#8a6425"
GREEN      = "#4fae7a"
RED        = "#d9686b"

# Custom CSS

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: {INK};
}}

.main .block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}}

h1, h2, h3, h4, h5, h6, p, label, span, div {{
    color: {TEXT};
}}

/* ---- Header ---- */
.console-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding-bottom: 4px;
}}
.console-dot {{
    width: 10px; height: 10px; border-radius: 50%;
    background: {AMBER};
    box-shadow: 0 0 10px {AMBER};
}}
.console-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin: 0;
}}
.console-subtitle {{
    font-family: 'JetBrains Mono', monospace;
    color: {MUTED};
    font-size: 0.85rem;
    margin-top: 2px;
    letter-spacing: 0.5px;
}}
.console-subtitle .sep {{ color: {AMBER_DIM}; margin: 0 6px; }}

hr, .stDivider {{ border-color: {BORDER} !important; }}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {{
    background: {PANEL};
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] .block-container {{
    padding-top: 1.5rem;
}}
.sidebar-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: {AMBER};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}
.doc-pill {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    background: {PANEL_2};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    margin: 4px 0;
    color: {TEXT};
}}

/* ---- Inputs ---- */
.stTextArea textarea, .stTextInput input {{
    background: {PANEL_2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
    font-size: 0.95rem !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
    border-color: {AMBER} !important;
    box-shadow: 0 0 0 1px {AMBER} !important;
}}
.stTextArea label, .stTextInput label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem !important;
    color: {MUTED} !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

/* ---- Buttons ---- */
div.stButton > button {{
    width: 100%;
    border-radius: 8px;
    height: 44px;
    font-size: 0.95rem;
    font-weight: 600;
    background: {PANEL_2};
    color: {TEXT};
    border: 1px solid {BORDER};
    transition: all 0.15s ease;
}}
div.stButton > button:hover {{
    border-color: {AMBER};
    color: {AMBER};
}}
div.stButton > button:active {{
    background: {AMBER_DIM};
}}
/* Primary ask button gets amber emphasis via key targeting through markdown wrapper below */

/* ---- Answer card ---- */
.answer-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-left: 3px solid {AMBER};
    border-radius: 10px;
    padding: 22px 24px;
    line-height: 1.65;
    font-size: 0.98rem;
}}
.answer-card-empty {{
    background: {PANEL};
    border: 1px dashed {BORDER};
    border-radius: 10px;
    padding: 32px 24px;
    text-align: center;
    color: {MUTED};
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}}

/* ---- Section labels ---- */
.section-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: {MUTED};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 28px 0 10px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.section-label::before {{
    content: "";
    width: 5px; height: 5px;
    background: {AMBER};
    border-radius: 50%;
}}

/* ---- Source chips ---- */
.source-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {PANEL_2};
    border: 1px solid {BORDER};
    color: {TEXT};
    padding: 7px 13px;
    border-radius: 8px;
    margin: 4px 6px 4px 0;
    font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
}}

/* ---- Status badge ---- */
.status-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 20px;
    border: 1px solid {BORDER};
}}
.status-ok {{ color: {GREEN}; border-color: {GREEN}44; }}
.status-err {{ color: {RED}; border-color: {RED}44; }}

/* Feedback confirmation text */
.feedback-note {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: {GREEN};
    margin-top: 6px;
}}

/* File uploader */
[data-testid="stFileUploader"] section {{
    background: {PANEL_2};
    border: 1px dashed {BORDER};
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

# Session State

defaults = {
    "answer": "",
    "sources": [],
    "question": "",
    "feedback_given": None,
    "last_query_time": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Sidebar

with st.sidebar:
    st.markdown('<div class="sidebar-label">Knowledge base</div>', unsafe_allow_html=True)

    if st.button("↻  Refresh index"):
        try:
            response = requests.get(f"{FASTAPI_URL}/documents", timeout=10)
            if response.status_code == 200:
                docs = response.json()["documents"]
                st.markdown(
                    f'<span class="status-badge status-ok">● {len(docs)} documents indexed</span>',
                    unsafe_allow_html=True
                )
                st.write("")
                for d in docs:
                    st.markdown(f'<div class="doc-pill">📄 {d}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-badge status-err">● index unavailable</span>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<span class="status-badge status-err">● server offline</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Add document</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
    "Upload PDF, TXT, or Markdown",
    type=["pdf", "txt", "md"],
    label_visibility="collapsed"
)

    if st.button("⬆  Upload"):
        if uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                response = requests.post(f"{FASTAPI_URL}/ingest", files=files, timeout=30)
                if response.status_code == 200:
                    st.success("Indexed successfully")
                else:
                    st.error("Upload failed")
            except Exception:
                st.error("Server offline")
        else:
            st.warning("Choose a file first")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:{MUTED};line-height:1.8;">'
        f'STACK<br>LangGraph · ChromaDB<br>Groq · FastAPI'
        f'</div>',
        unsafe_allow_html=True
    )

# Header

st.markdown(f"""
<div class="console-header">
    <div class="console-dot"></div>
    <h1 class="console-title">Technical Documentation Assistant</h1>
</div>
<div class="console-subtitle">RAG-BACKED Q&A <span class="sep">/</span> LANGGRAPH <span class="sep">/</span> CHROMADB <span class="sep">/</span> GROQ</div>
""", unsafe_allow_html=True)

st.write("")
st.divider()

# Question Input

question = st.text_area(
    "Ask a question",
    height=120,
    placeholder="e.g. Explain how LangGraph StateGraph works, and where checkpointing fits in..."
)

col_ask, col_spacer = st.columns([1, 3])
with col_ask:
    ask_clicked = st.button("⏎  Run query")

if ask_clicked:
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Querying knowledge base..."):
            try:
                response = requests.post(
                    f"{FASTAPI_URL}/query",
                    json={"question": question},
                    timeout=60
                )
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.answer = result["answer"]
                    st.session_state.sources = result["sources"]
                    st.session_state.question = question
                    st.session_state.feedback_given = None
                    st.session_state.last_query_time = datetime.now().strftime("%H:%M:%S")
                else:
                    st.error(response.text)
            except Exception:
                st.error("FastAPI server is not running.")

# Answer

label = "Response"
if st.session_state.last_query_time:
    label += f"  ·  {st.session_state.last_query_time}"
st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)

if st.session_state.answer:
    st.markdown(f'<div class="answer-card">{st.session_state.answer}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="answer-card-empty">// awaiting query</div>', unsafe_allow_html=True)

# Sources

st.markdown('<div class="section-label">Sources</div>', unsafe_allow_html=True)

if st.session_state.sources:
    html = "".join(f'<span class="source-chip">📄 {s}</span>' for s in st.session_state.sources)
    st.markdown(html, unsafe_allow_html=True)
else:
    st.markdown(f'<span style="color:{MUTED};font-family:JetBrains Mono,monospace;font-size:0.85rem;">none yet</span>', unsafe_allow_html=True)

# Feedback

if st.session_state.answer:
    st.markdown('<div class="section-label">Was this useful</div>', unsafe_allow_html=True)

    if st.session_state.feedback_given:
        icon = "👍" if st.session_state.feedback_given == "thumbs_up" else "👎"
        st.markdown(f'<div class="feedback-note">{icon}  Feedback recorded — thank you.</div>', unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("👍  Helpful"):
                try:
                    requests.post(
                        f"{FASTAPI_URL}/feedback",
                        json={
                            "question": st.session_state.question,
                            "answer": st.session_state.answer,
                            "rating": "thumbs_up",
                            "comment": ""
                        },
                        timeout=10
                    )
                except Exception:
                    pass
                st.session_state.feedback_given = "thumbs_up"
                st.rerun()

        with col2:
            if st.button("👎  Not helpful"):
                try:
                    requests.post(
                        f"{FASTAPI_URL}/feedback",
                        json={
                            "question": st.session_state.question,
                            "answer": st.session_state.answer,
                            "rating": "thumbs_down",
                            "comment": ""
                        },
                        timeout=10
                    )
                except Exception:
                    pass
                st.session_state.feedback_given = "thumbs_down"
                st.rerun()