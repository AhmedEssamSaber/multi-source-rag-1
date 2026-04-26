import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

import streamlit as st
from chatbot import Chatbot

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroRAG — Medical AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0a0e1a;
    --bg2:       #0f1528;
    --surface:   #141929;
    --surface2:  #1a2035;
    --border:    rgba(99,179,237,0.12);
    --accent:    #63b3ed;
    --accent2:   #4fd1c5;
    --danger:    #fc8181;
    --warn:      #f6ad55;
    --success:   #68d391;
    --text:      #e2e8f0;
    --muted:     #718096;
    --glow:      rgba(99,179,237,0.15);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.2rem !important;
}

/* ── Sidebar logo area ── */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}
.sidebar-logo .icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 0 20px var(--glow);
}
.sidebar-logo .brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}
.sidebar-logo .version {
    font-size: 0.65rem;
    color: var(--muted);
    margin-top: -2px;
}

/* ── Sidebar section label ── */
.sidebar-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.2rem 0 0.5rem 0;
}

/* ── Stat cards ── */
.stat-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 1rem;
}
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 12px;
    text-align: center;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: var(--accent); }
.stat-card .val {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}
.stat-card .lbl {
    font-size: 0.65rem;
    color: var(--muted);
    margin-top: 3px;
}

/* ── Source badge ── */
.src-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    color: var(--accent);
    margin: 3px 3px 3px 0;
    transition: all 0.2s;
}
.src-badge:hover {
    background: var(--glow);
    border-color: var(--accent);
}
.src-badge .dot {
    width: 6px; height: 6px;
    background: var(--accent2);
    border-radius: 50%;
}

/* ── Confidence bar ── */
.conf-bar-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 14px;
    margin-top: 8px;
}
.conf-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    color: var(--muted);
    margin-bottom: 6px;
}
.conf-bar-track {
    background: var(--bg);
    border-radius: 4px;
    height: 5px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}

/* ── Chat layout ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: var(--bg);
}
.chat-header {
    padding: 1rem 2rem;
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
}
.chat-header-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.chat-header-sub {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 1px;
}
.status-dot {
    width: 8px; height: 8px;
    background: var(--success);
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 8px var(--success);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Messages area ── */
.messages-area {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem 2rem;
}

/* ── Message bubbles ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1.2rem;
    animation: slideInRight 0.3s ease;
}
.msg-assistant {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1.2rem;
    animation: slideInLeft 0.3s ease;
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
.bubble-user {
    background: linear-gradient(135deg, #2b4a7a, #1e3a5f);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    max-width: 65%;
    font-size: 0.9rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.bubble-assistant {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.7;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.bubble-assistant strong {
    color: var(--accent);
    font-weight: 600;
}
.bubble-assistant ul {
    margin: 6px 0 6px 1rem;
    padding: 0;
}
.bubble-assistant li {
    margin-bottom: 4px;
    color: var(--text);
}
.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.avatar-user {
    background: linear-gradient(135deg, #2b4a7a, #63b3ed);
    margin-left: 10px;
}
.avatar-bot {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    margin-right: 10px;
    box-shadow: 0 0 12px var(--glow);
}
.msg-meta {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
}

/* ── Input area ── */
.input-area {
    padding: 1rem 2rem 1.5rem;
    background: var(--bg2);
    border-top: 1px solid var(--border);
    flex-shrink: 0;
}

/* ── Streamlit chat input override ── */
.stChatInput {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}
.stChatInput:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--glow) !important;
}
.stChatInput textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stChatInput button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    border-radius: 10px !important;
}

/* ── Streamlit button ── */
.stButton > button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    padding: 6px 14px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--glow) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Quick questions ── */
.quick-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 0.78rem;
    color: var(--text);
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 6px;
    width: 100%;
    text-align: left;
}
.quick-btn:hover {
    background: var(--glow);
    border-color: var(--accent);
    color: var(--accent);
}

/* ── Welcome screen ── */
.welcome-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh;
    text-align: center;
    gap: 12px;
}
.welcome-icon {
    font-size: 3.5rem;
    filter: drop-shadow(0 0 20px rgba(99,179,237,0.4));
    animation: floatIcon 3s ease-in-out infinite;
}
@keyframes floatIcon {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-8px); }
}
.welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}
.welcome-sub {
    font-size: 0.9rem;
    color: var(--muted);
    max-width: 400px;
    line-height: 1.6;
}
.welcome-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 8px;
}
.chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.78rem;
    color: var(--accent);
}

/* ── Thinking animation ── */
.thinking {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 12px 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
}
.thinking span {
    width: 7px; height: 7px;
    background: var(--accent);
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.thinking span:nth-child(2) { animation-delay: 0.2s; }
.thinking span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
    40%            { transform: scale(1);   opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ── Load chatbot ──────────────────────────────────────────────────
@st.cache_resource
def load_bot():
    return Chatbot()

bot = load_bot()

# ── Session state ─────────────────────────────────────────────────
if "messages"       not in st.session_state: st.session_state.messages       = []
if "total_queries"  not in st.session_state: st.session_state.total_queries  = 0
if "quick_query"    not in st.session_state: st.session_state.quick_query    = None

# ── Helper: confidence bar ────────────────────────────────────────
def conf_bar(confidence):
    pct   = min(int(confidence / 0.01 * 100), 100)
    if confidence < 0.0001:
        color, label = "#fc8181", "Low"
    elif confidence < 0.001:
        color, label = "#f6ad55", "Moderate"
    else:
        color, label = "#68d391", "High"
    return f"""
    <div class="conf-bar-wrap">
        <div class="conf-bar-label">
            <span>Confidence</span>
            <span style="color:{color};font-weight:600">{label} ({confidence:.4f})</span>
        </div>
        <div class="conf-bar-track">
            <div class="conf-bar-fill" style="width:{max(pct,4)}%;background:{color}"></div>
        </div>
    </div>"""

# ── Helper: source badges ─────────────────────────────────────────
def source_badges(sources):
    badges = ""
    for s in sources:
        badges += f'<span class="src-badge"><span class="dot"></span>{s["source"]} <span style="color:#718096">·</span> {s["score"]:.4f}</span>'
    return f'<div class="msg-meta">{badges}</div>'

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="icon">🧠</div>
        <div>
            <div class="brand">NeuroRAG</div>
            <div class="version">Medical AI Assistant v1.0</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Stats
    chunks = len(bot.store.chunks)
    turns  = len(bot.memory.get_history()) // 2
    st.markdown(f"""
    <div class="sidebar-label">System Status</div>
    <div class="stat-row">
        <div class="stat-card"><div class="val">{chunks}</div><div class="lbl">Chunks</div></div>
        <div class="stat-card"><div class="val">{st.session_state.total_queries}</div><div class="lbl">Queries</div></div>
        <div class="stat-card"><div class="val">{turns}</div><div class="lbl">Turns</div></div>
        <div class="stat-card"><div class="val">✓</div><div class="lbl">Online</div></div>
    </div>""", unsafe_allow_html=True)

    # Quick questions
    st.markdown('<div class="sidebar-label">Quick Questions</div>', unsafe_allow_html=True)
    quick_qs = [
        "📋 Explain my patient report",
        "🔬 What is my diagnosis?",
        "💊 What treatment options exist?",
        "🧬 What is meningioma?",
        "🧠 What causes brain edema?",
        "💉 What is a glioma?",
        "📊 What is mass effect?",
        "🔭 Explain hydrocephalus",
    ]
    for q in quick_qs:
        if st.button(q, key=f"quick_{q}"):
            st.session_state.quick_query = q[2:].strip()

    # Controls
    st.markdown('<div class="sidebar-label">Controls</div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        bot.memory.clear()
        st.session_state.total_queries = 0
        st.rerun()

    if st.button("🔄 Rebuild Index"):
        bot.store.clear()
        import os
        cache = os.path.join(ROOT, "data", "vector_store_cache.pkl")
        if os.path.exists(cache):
            os.remove(cache)
        bot._load_all_sources()
        st.success("Index rebuilt!")

    # Sources list
    st.markdown('<div class="sidebar-label">Indexed Sources</div>', unsafe_allow_html=True)
    sources_seen = list(dict.fromkeys(c["source"] for c in bot.store.chunks))
    for src in sources_seen:
        count = sum(1 for c in bot.store.chunks if c["source"] == src)
        st.markdown(f'<span class="src-badge"><span class="dot"></span>{src} · {count} chunks</span>', unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────
# Header
st.markdown("""
<div class="chat-header">
    <div>
        <div class="chat-header-title">Medical RAG Assistant</div>
        <div class="chat-header-sub">Powered by Cohere + Groq · Multi-source retrieval</div>
    </div>
    <div style="font-size:0.8rem;color:var(--muted)">
        <span class="status-dot"></span>All systems operational
    </div>
</div>""", unsafe_allow_html=True)

# Messages or welcome
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-icon">🧠</div>
        <div class="welcome-title">NeuroRAG Assistant</div>
        <div class="welcome-sub">
            Ask me anything about your patient report or medical conditions.
            I retrieve answers from indexed medical documents in real time.
        </div>
        <div class="welcome-chips">
            <span class="chip">📋 Patient Reports</span>
            <span class="chip">🔬 Brain Tumors</span>
            <span class="chip">🧬 Glioma</span>
            <span class="chip">💊 Treatment</span>
            <span class="chip">🧠 Neurology</span>
        </div>
    </div>""", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="bubble-user">{msg["content"]}</div>
                <div class="avatar avatar-user">👤</div>
            </div>""", unsafe_allow_html=True)
        else:
            content = msg["content"].replace("\n", "<br>")
            badges  = source_badges(msg.get("sources", []))
            bar     = conf_bar(msg.get("confidence", 0))
            st.markdown(f"""
            <div class="msg-assistant">
                <div class="avatar avatar-bot">🧠</div>
                <div>
                    <div class="bubble-assistant">{content}</div>
                    {badges}
                    {bar}
                </div>
            </div>""", unsafe_allow_html=True)

# ── Handle quick query ────────────────────────────────────────────
if st.session_state.quick_query:
    prompt = st.session_state.quick_query
    st.session_state.quick_query = None
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_queries += 1
    with st.spinner(""):
        answer, sources, confidence = bot.chat(prompt)
    st.session_state.messages.append({
        "role": "assistant", "content": answer,
        "sources": sources, "confidence": confidence
    })
    st.rerun()

# ── Chat input ────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about your patient report or any medical condition..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_queries += 1
    with st.spinner(""):
        answer, sources, confidence = bot.chat(prompt)
    st.session_state.messages.append({
        "role": "assistant", "content": answer,
        "sources": sources, "confidence": confidence
    })
    st.rerun()