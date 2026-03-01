# 🧠 NovaMind AI — Competitive Intelligence System

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge)

> **Autonomous AI system that researches any company, analyzes competitors, and generates executive intelligence reports in under 60 seconds.**

---

## 🚀 Live Demo
> Enter any company name → 4 AI Agents activate → Full intelligence report generated

---

## ✨ Features

- 🔬 **Research Agent** — Deep company data gathering
- 🎯 **Competitor Agent** — Identifies top 3 competitors
- 📈 **Market Agent** — Analyzes market trends & opportunities
- 📝 **Report Agent** — Generates 6-section executive report
- 💬 **AI Chat Assistant** — Ask follow-up questions about any company
- 🤖 **Robot Emotion Engine** — Real-time AI mood visualization
- 📥 **Report Download** — Export intelligence report as .txt

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3.10 | Core language |
| CrewAI | Multi-agent orchestration |
| Groq API | LLM inference engine |
| LLaMA 3.3 70B | AI model |
| Streamlit | Web UI framework |
| python-dotenv | API key security |

---

## ⚙️ Setup & Installation
```bash
# 1. Clone the repository
git clone https://github.com/nishaids/novamind-ai-competitive-intelligence.git
cd novamind-ai-competitive-intelligence

# 2. Install dependencies
pip install crewai groq streamlit python-dotenv

# 3. Add your API key
echo "GROQ_API_KEY=your_groq_key_here" > .env

# 4. Run the app
streamlit run app.py
```

---

## 🎯 How It Works

1. Enter your **Groq API Key** and **Target Company**
2. Click **Initialize Intelligence Scan**
3. Watch 4 AI Agents work in real-time
4. Get a complete **Executive Intelligence Report**
5. Ask follow-up questions via the **AI Chat Assistant**

---

## 📁 Project Structure
```
novamind-ai-competitive-intelligence/
├── agents/
│   ├── research_agent.py
│   ├── competitor_agent.py
│   ├── analysis_agent.py
│   └── report_agent.py
├── output/           # Generated reports
├── app.py            # Main Streamlit app
├── main.py           # Core logic
├── .env              # API keys (not committed)
└── .gitignore
```

---

## 👨‍💻 Developer

**Nishanth R**  
Built as part of a 6-day AI development challenge

---

## 📄 License
MIT License
