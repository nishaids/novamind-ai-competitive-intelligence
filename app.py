import streamlit as st
from crewai import Agent, Task, Crew, LLM
from groq import Groq
import time

st.set_page_config(
    page_title="NovaMind AI",
    page_icon="🧠",
    layout="wide"
)

if "emotion" not in st.session_state:
    st.session_state.emotion = "idle"
if "report_done" not in st.session_state:
    st.session_state.report_done = False
if "report_text" not in st.session_state:
    st.session_state.report_text = ""
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "groq_key" not in st.session_state:
    st.session_state.groq_key = ""
if "chat_key" not in st.session_state:
    st.session_state.chat_key = 0

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

.stApp {
    background: #000000;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(255,0,128,0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(0,200,255,0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 80%, rgba(138,0,255,0.06) 0%, transparent 60%);
    min-height: 100vh;
}
.stApp > header { background: transparent !important; }
section[data-testid="stSidebar"] { display: none !important; }

.hero-section {
    text-align: center;
    padding: 60px 20px 40px;
    position: relative;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 2px;
    background: linear-gradient(90deg, transparent, #ff0080, #00c8ff, transparent);
    animation: scanline 3s ease-in-out infinite;
}
@keyframes scanline {
    0%, 100% { opacity: 0.3; width: 200px; }
    50%       { opacity: 1;   width: 600px; }
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ff0080, #ff6ec7, #00c8ff, #0080ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
    margin-bottom: 10px;
    animation: titleGlow 4s ease-in-out infinite alternate;
}
@keyframes titleGlow {
    0%   { filter: brightness(1);   }
    100% { filter: brightness(1.4); }
}
.hero-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    color: #cccccc;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.system-ready {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 30px;
    font-weight: 600;
    background: linear-gradient(90deg, #ff0080, #ff6ec7, #00c8ff, #8000ff, #ff0080);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: colorShift 5s linear infinite;
}
@keyframes colorShift {
    0%   { background-position: 0%   center; }
    100% { background-position: 300% center; }
}

/* ROBOT */
.robot-widget {
    margin-top: 14px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
}
.robot-avatar {
    min-width: 130px;
    height: 48px;
    border: 1px solid rgba(47,230,255,0.45);
    border-radius: 12px;
    background: rgba(0,0,0,0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 16px rgba(47,230,255,0.2);
    animation: robotIdle 2.2s ease-in-out infinite;
}
.robot-avatar::before {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #ff4db8, #2fe6ff, #9d7bff, #4aa3ff, #ff4db8);
    background-size: 320% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: footerShift 7s linear infinite;
}
.robot-state {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #ffffff;
}
.robot-widget.idle     .robot-avatar::before { content: "[o_o]"; }
.robot-widget.thinking .robot-avatar::before { content: "[o_o]"; }
.robot-widget.happy    .robot-avatar::before { content: "[^_^]"; }
.robot-widget.sad      .robot-avatar::before { content: "[-_-]"; }
.robot-widget.angry    .robot-avatar::before { content: "[>_<]"; }
.robot-widget.crazy    .robot-avatar::before { content: "[@_@]"; }

.robot-widget.thinking .robot-avatar { animation: robotThink 0.95s ease-in-out infinite; }
.robot-widget.happy    .robot-avatar { animation: robotHappy 1.1s ease-in-out infinite;  }
.robot-widget.sad      .robot-avatar { animation: robotSad   1.6s ease-in-out infinite;  }
.robot-widget.angry    .robot-avatar { animation: robotAngry 0.6s linear infinite;       }
.robot-widget.crazy    .robot-avatar { animation: robotCrazy 0.28s linear infinite;      }

@keyframes robotIdle  { 0%,100%{transform:translateY(0)}  50%{transform:translateY(-2px)} }
@keyframes robotThink { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(-3px) scale(1.02)} }
@keyframes robotHappy { 0%,100%{transform:translateY(0)} 25%{transform:translateY(-3px)} 75%{transform:translateY(-2px)} }
@keyframes robotSad   { 0%,100%{transform:translateY(0);opacity:1} 50%{transform:translateY(2px);opacity:0.88} }
@keyframes robotAngry { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-2px)} 75%{transform:translateX(2px)} }
@keyframes robotCrazy { 0%,100%{transform:translate(0,0) rotate(0deg)} 25%{transform:translate(-1px,1px) rotate(-1deg)} 75%{transform:translate(1px,-1px) rotate(1deg)} }

/* INPUT */
.input-container {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,0,128,0.25);
    border-radius: 16px;
    padding: 40px;
    margin: 20px auto;
    max-width: 800px;
    backdrop-filter: blur(20px);
    box-shadow: 0 0 40px rgba(255,0,128,0.05), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.3s ease;
}
.input-container:hover {
    border-color: rgba(255,0,128,0.4);
    box-shadow: 0 0 60px rgba(255,0,128,0.1);
}
.stTextInput > div > div > input {
    background: rgba(0,0,0,0.6) !important;
    border: 1px solid rgba(0,200,255,0.3) !important;
    border-radius: 10px !important;
    color: #f5fbff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    padding: 15px 20px !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff0080 !important;
    box-shadow: 0 0 20px rgba(255,0,128,0.3) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.3) !important; }
.stTextInput label {
    color: #ff6ec7 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
}

/* BUTTON */
div.stButton > button {
    background: linear-gradient(135deg, #ff0080, #8000ff) !important;
    color: #f5fbff !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 18px 50px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    animation: buttonPulse 2s ease-in-out infinite !important;
}
div.stButton > button p {
    color: #f5fbff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-shadow: 0 0 10px rgba(0,200,255,0.45) !important;
}
@keyframes buttonPulse {
    0%,100% { box-shadow: 0 0 30px rgba(255,0,128,0.5), 0 0 60px rgba(255,0,128,0.2); }
    50%      { box-shadow: 0 0 60px rgba(255,0,128,0.9), 0 0 120px rgba(255,0,128,0.5); }
}
div.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 0 80px rgba(255,0,128,0.9) !important;
}

/* AGENT CARDS */
.agent-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin: 30px 0;
}
.agent-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 12px;
    padding: 20px 15px;
    text-align: center;
    transition: all 0.3s ease;
    font-family: 'Rajdhani', sans-serif;
}
.agent-card:hover {
    border-color: rgba(0,200,255,0.5);
    box-shadow: 0 0 25px rgba(0,200,255,0.15);
    transform: translateY(-3px);
}
.agent-card .icon   { font-size: 2rem; margin-bottom: 8px; }
.agent-card .name   { color: #00c8ff; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }
.agent-card .status { color: #bbbbbb; font-size: 0.75rem; margin-top: 4px; letter-spacing: 1px; }

/* STATS */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin: 30px 0;
    flex-wrap: wrap;
}
.stat-item { text-align: center; font-family: 'Rajdhani', sans-serif; }
.stat-number {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ff0080, #00c8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label { color: #cccccc; font-size: 0.8rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 4px; font-weight: 600; }

/* REPORT */
.report-wrapper {
    background: rgba(0,0,0,0.82);
    border: 1px solid rgba(0,200,255,0.35);
    border-radius: 16px;
    padding: 40px;
    margin: 30px 0;
    line-height: 2;
    font-size: 1.05rem;
    box-shadow: 0 0 40px rgba(0,200,255,0.14), inset 0 0 24px rgba(255,0,128,0.06);
}
.report-wrapper p,
.report-wrapper li,
.stMarkdown p,
.stMarkdown li,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #d8e6ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem !important;
    line-height: 2 !important;
}
.report-wrapper h1 {
    color: #ffffff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.4rem !important;
    letter-spacing: 3px !important;
    margin: 28px 0 12px !important;
    text-shadow: 0 0 20px rgba(255,0,128,0.5) !important;
    border-bottom: 1px solid rgba(255,0,128,0.3) !important;
    padding-bottom: 8px !important;
}
.report-wrapper h2,
.stMarkdown h2 {
    background: linear-gradient(90deg, #ff4db8, #2fe6ff, #39ff14, #ff3b3b, #b066ff) !important;
    background-size: 320% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: colorShift 5s linear infinite !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.2rem !important;
    letter-spacing: 3px !important;
    margin: 24px 0 10px !important;
    text-shadow: none !important;
}
.report-wrapper h3,
.stMarkdown h3 {
    color: #00c8ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1rem !important;
    letter-spacing: 2px !important;
    margin: 20px 0 8px !important;
}
.report-wrapper strong,
.report-wrapper b {
    color: #00c8ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-shadow: 0 0 10px rgba(0,200,255,0.3) !important;
}
.report-wrapper em { color: #ff6ec7 !important; }

/* CHAT BOX */
.chat-container {
    background: rgba(0,0,0,0.85);
    border: 1px solid rgba(255,0,128,0.35);
    border-radius: 16px;
    padding: 30px;
    margin: 30px 0;
    box-shadow: 0 0 40px rgba(255,0,128,0.1);
}
.chat-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #ff0080, #00c8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
    text-align: center;
}
.chat-msg-user {
    background: linear-gradient(135deg, rgba(255,0,128,0.15), rgba(128,0,255,0.15));
    border: 1px solid rgba(255,0,128,0.3);
    border-radius: 12px 12px 4px 12px;
    padding: 12px 18px;
    margin: 10px 0 10px 20%;
    font-family: 'Rajdhani', sans-serif;
    color: #ffffff !important;
    font-size: 1rem;
    letter-spacing: 1px;
}
.chat-msg-ai {
    background: linear-gradient(135deg, rgba(0,200,255,0.1), rgba(0,128,255,0.1));
    border: 1px solid rgba(0,200,255,0.25);
    border-radius: 12px 12px 12px 4px;
    padding: 12px 18px;
    margin: 10px 20% 10px 0;
    font-family: 'Rajdhani', sans-serif;
    color: #e0e8ff !important;
    font-size: 1rem;
    letter-spacing: 1px;
    line-height: 1.7;
}
.chat-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.chat-label.you  { color: #ff6ec7; text-align: right; }
.chat-label.nova { color: #00c8ff; }

/* MISC */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,0,128,0.4), rgba(0,200,255,0.4), transparent);
    margin: 30px 0;
}
.success-banner {
    background: linear-gradient(135deg, rgba(0,255,128,0.1), rgba(0,200,255,0.1));
    border: 1px solid rgba(0,255,128,0.3);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    font-family: 'Orbitron', monospace;
    color: #00ff80;
    letter-spacing: 3px;
    font-size: 0.9rem;
    box-shadow: 0 0 30px rgba(0,255,128,0.1);
}
.stProgress > div > div > div { background: linear-gradient(90deg, #ff0080, #8000ff, #00c8ff) !important; border-radius: 10px !important; }
.stProgress > div > div { background: rgba(255,255,255,0.05) !important; border-radius: 10px !important; }
.stDownloadButton > button {
    background: rgba(0,200,255,0.1) !important;
    border: 1px solid rgba(0,200,255,0.4) !important;
    color: #00c8ff !important;
    border-radius: 50px !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}
.stDownloadButton > button:hover { background: rgba(0,200,255,0.25) !important; box-shadow: 0 0 30px rgba(0,200,255,0.4) !important; }
.stAlert > div { color: #ffffff !important; font-family: 'Rajdhani', sans-serif !important; }

/* FOOTER */
.footer-section {
    text-align: center;
    padding: 30px 20px;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 3px;
    font-size: 0.8rem;
    text-transform: uppercase;
}
@keyframes footerShift {
    0%   { background-position: 0%   center; }
    100% { background-position: 320% center; }
}
.footer-powered, .footer-devby {
    background: linear-gradient(90deg, #ff4db8, #2fe6ff, #b066ff, #4aa3ff, #ff4db8);
    background-size: 320% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: footerShift 7s linear infinite;
}
.footer-powered { margin-bottom: 12px; font-size: 0.75rem; }
.footer-devby   { margin-bottom: 10px; font-size: 0.8rem; letter-spacing: 4px; }

.typewriter-wrap { display: flex; justify-content: center; align-items: center; height: 2.2rem; }
.typewriter-name {
    font-family: 'Orbitron', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ff4db8, #2fe6ff, #b066ff, #4aa3ff, #ff4db8);
    background-size: 320% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    white-space: nowrap;
    overflow: hidden;
    display: inline-block;
    border-right: 2px solid #ff6ec7;
    width: 0ch;
    max-width: 12ch;
    animation: typewriter 7s steps(12, end) infinite, footerShift 7s linear infinite;
}
@keyframes typewriter {
    0%   { width: 0ch;  border-color: #ff6ec7; }
    17%  { width: 12ch; border-color: #ff6ec7; }
    60%  { width: 12ch; border-color: #ff6ec7; }
    77%  { width: 0ch;  border-color: #ff6ec7; }
    100% { width: 0ch;  border-color: #ff6ec7; }
}
footer    { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
def render_hero(slot):
    labels = {
        "idle": "Idle", "thinking": "Thinking...",
        "happy": "Joy Mode", "sad": "Sad",
        "angry": "Angry", "crazy": "System Overload"
    }
    label = labels.get(st.session_state.emotion, "Idle")
    slot.markdown(f"""
<div class="hero-section">
    <div class="hero-title">NOVAMIND AI</div>
    <div class="hero-sub">Competitive Intelligence · Autonomous Agents · Real-time Analysis</div>
    <div class="system-ready">▸ SYSTEM READY · INTELLIGENCE ENGINE ONLINE · ALL AGENTS ACTIVE</div>
    <div class="robot-widget {st.session_state.emotion}">
        <div class="robot-avatar"></div>
        <div class="robot-state">Robot Emotion:&nbsp;
            <span style="background:linear-gradient(90deg,#ff4db8,#2fe6ff,#9d7bff);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;">{label}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


hero_slot = st.empty()
render_hero(hero_slot)

# ── STATS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-item"><div class="stat-number">4</div><div class="stat-label">AI Agents</div></div>
    <div class="stat-item"><div class="stat-number">60s</div><div class="stat-label">Analysis Time</div></div>
    <div class="stat-item"><div class="stat-number">6</div><div class="stat-label">Report Sections</div></div>
    <div class="stat-item"><div class="stat-number">∞</div><div class="stat-label">Companies</div></div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── INPUTS ────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-container">', unsafe_allow_html=True)
api_key = st.secrets["GROQ_API_KEY"]
company = st.text_input("🏢  TARGET COMPANY", placeholder="e.g.  TESLA  ·  APPLE  ·  ZOHO  ·  INFOSYS")
st.markdown("<br>", unsafe_allow_html=True)
generate = st.button("⚡  INITIALIZE INTELLIGENCE SCAN")
st.markdown('</div>', unsafe_allow_html=True)

# ── AGENT CARDS ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="agent-grid">
    <div class="agent-card"><div class="icon">🔬</div><div class="name">Research Agent</div><div class="status">STANDBY</div></div>
    <div class="agent-card"><div class="icon">🎯</div><div class="name">Competitor Agent</div><div class="status">STANDBY</div></div>
    <div class="agent-card"><div class="icon">📈</div><div class="name">Market Agent</div><div class="status">STANDBY</div></div>
    <div class="agent-card"><div class="icon">📝</div><div class="name">Report Agent</div><div class="status">STANDBY</div></div>
</div>
""", unsafe_allow_html=True)

# ── GENERATE ──────────────────────────────────────────────────────────────────
if generate:
    if not company:
        st.error("⚠️ Please enter a Target Company name!")
    else:
        st.session_state.groq_key    = api_key
        st.session_state.company_name = company
        st.session_state.chat_history = []
        st.session_state.report_done  = False

        st.session_state.emotion = "thinking"
        render_hero(hero_slot)

        progress = st.progress(0)
        status   = st.empty()

        llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=api_key)

        master_agent = Agent(
            role="Elite Business Intelligence Analyst",
            goal=f"Produce a complete competitive intelligence report for {company}",
            backstory="""You are a world-class business analyst who researches companies,
            identifies competitors, analyzes markets, and writes executive reports.""",
            llm=llm, verbose=False, max_iter=2
        )

        master_task = Task(
            description=f"""Create a complete Executive Intelligence Report for '{company}'.
            Use ## for section headings:

            ## 1. Executive Summary
            ## 2. Company Overview
            ## 3. Top 3 Competitors
            ## 4. Market Opportunities
            ## 5. Key Threats
            ## 6. Strategic Recommendations

            Keep each section concise. Total under 500 words.""",
            expected_output="Complete 6-section Executive Intelligence Report",
            agent=master_agent
        )

        crew = Crew(agents=[master_agent], tasks=[master_task], verbose=False)

        steps    = [
            ("🔬 Research Agent scanning company data...", 25),
            ("🎯 Competitor Agent identifying rivals...",  50),
            ("📈 Market Agent analyzing trends...",        75),
            ("📝 Report Agent compiling intelligence...", 90),
        ]
        emotions = ["thinking", "crazy", "sad", "happy"]

        try:
            for i, (label, prog) in enumerate(steps):
                st.session_state.emotion = emotions[i]
                render_hero(hero_slot)
                status.markdown(
                    f"<p style='font-family:Rajdhani;color:#ff6ec7;letter-spacing:3px;"
                    f"text-align:center;font-size:1.1rem'>{label}</p>",
                    unsafe_allow_html=True
                )
                progress.progress(prog)
                time.sleep(0.5)

            result = crew.kickoff()
            result_text = str(result).lower()

            st.session_state.emotion = "happy" if ("opportunity" in result_text or "growth" in result_text) else "angry"
            st.session_state.report_text = str(result)
            st.session_state.report_done = True

            render_hero(hero_slot)
            progress.progress(100)
            status.empty()
            st.balloons()

            st.markdown(
                f'<div class="success-banner">✨ INTELLIGENCE REPORT GENERATED · {company.upper()} · ANALYSIS COMPLETE ✨</div>',
                unsafe_allow_html=True
            )
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-wrapper">', unsafe_allow_html=True)
            st.markdown(str(result))
            st.markdown('</div>', unsafe_allow_html=True)

            filename = f"output/{company.lower().replace(' ', '_')}_report.txt"
            with open(filename, "w") as f:
                f.write(str(result))

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥  DOWNLOAD INTELLIGENCE REPORT",
                data=str(result),
                file_name=f"{company}_intelligence_report.txt",
                mime="text/plain"
            )

        except Exception:
            st.session_state.emotion = "crazy"
            render_hero(hero_slot)
            st.error("⚠️  SCAN FAILED — Rate limit reached. Wait 60 seconds and retry.")

# ── AI CHAT ASSISTANT (appears after report) ──────────────────────────────────
if st.session_state.report_done and st.session_state.report_text:

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">💬 ASK NOVAMIND AI ASSISTANT</div>
        <p style="font-family:Rajdhani;color:#888;letter-spacing:2px;font-size:0.85rem;
                  text-align:center;margin-bottom:20px;">
            ASK ANYTHING ABOUT THE COMPANY · POWERED BY LLAMA 3.3
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Render existing chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-label you">YOU</div>
            <div class="chat-msg-user">{msg["content"]}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-label nova">⚡ NOVAMIND</div>
            <div class="chat-msg-ai">{msg["content"]}</div>
            """, unsafe_allow_html=True)

    # Chat input
    user_question = st.text_input(
        "💬  ASK ABOUT THE COMPANY",
        placeholder=f"e.g. What is {st.session_state.company_name}'s biggest risk?",
        key=f"chat_input_{st.session_state.chat_key}"
    )

    col1, col2 = st.columns([3, 1])
    with col2:
        ask_btn = st.button("⚡  ASK", key="ask_button")

    if ask_btn and user_question:
        with st.spinner("🤖 NovaMind thinking..."):
            try:
                client = Groq(api_key=st.session_state.groq_key)

                # Build context-aware system prompt
                system_prompt = f"""You are NovaMind AI, an expert business intelligence assistant.
You have just analyzed {st.session_state.company_name} and generated this report:

{st.session_state.report_text}

Answer the user's questions about {st.session_state.company_name} using this report as context.
Be concise, professional, and insightful. Keep answers under 150 words."""

                messages = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.chat_history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                messages.append({"role": "user", "content": user_question})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    max_tokens=200
                )

                ai_reply = response.choices[0].message.content

                st.session_state.chat_history.append({"role": "user",      "content": user_question})
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                st.session_state.chat_key += 1
                st.rerun()

            except Exception:
                st.error("⚠️  Chat failed — rate limit. Wait 30 seconds and retry.")

    if st.session_state.chat_history:
        if st.button("🗑️  CLEAR CHAT"):
            st.session_state.chat_history = []
            st.rerun()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer-section">
    <div class="footer-powered">NOVAMIND AI · COMPETITIVE INTELLIGENCE SYSTEM · POWERED BY CREWAI + LLAMA 3.3</div>
    <div class="footer-devby">DEVELOPED BY</div>
    <div class="typewriter-wrap">
        <span class="typewriter-name">NISHANTH R</span>
    </div>
</div>
""", unsafe_allow_html=True)
