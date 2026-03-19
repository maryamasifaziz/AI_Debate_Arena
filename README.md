# 🎤 AI Debate Arena

**Students vs AI. AI vs AI. Who wins?**

A Django-powered debate platform where users can engage in structured debates against AI opponents — or watch two AI agents argue both sides of a topic. A JudgeAgent evaluates the debate and scores both sides.

🌐 **Live Demo:** [aidebatearena-production.up.railway.app](https://aidebatearena-production.up.railway.app/accounts/login/)  
📁 **GitHub:** [maryamasifaziz/AI_Debate_Arena](https://github.com/maryamasifaziz/AI_Debate_Arena)

---

## ✨ Features

- 🧠 **AI vs Student** - Debate against an AI opponent in real time
- 🤖 **AI vs AI** - Watch ProAgent and ConAgent argue both sides of any topic
- ⚖️ **JudgeAgent** - An AI judge scores both sides out of 10 and gives feedback
- 👤 **User Authentication** - Register and login to start debating
- ⚡ **Powered by Groq** - Fast LLM inference for snappy AI responses
- 🔄 **Switchable AI Provider** - Supports both Groq and OpenAI backends
- 🚀 **Deployed on Railway** - Live and accessible from anywhere

---

## 🤖 How the Agents Work

| Agent | Role |
|---|---|
| **ProAgent** | Argues FOR the topic - gives 3 arguments + a challenge question |
| **ConAgent** | Argues AGAINST the topic - gives 3 counter-arguments + a challenge question |
| **JudgeAgent** | Scores both sides out of 10, gives a 4-line summary + improvement tips |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django |
| AI / LLM | Groq API (OpenAI compatible) |
| Server | Gunicorn |
| Deployment | Railway |
| Database | SQLite |

---

## 🚀 Getting Started (Local Setup)

### 1. Clone the repo
```bash
git clone https://github.com/maryamasifaziz/AI_Debate_Arena.git
cd AI_Debate_Arena
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
> Get your free API key at [console.groq.com](https://console.groq.com)

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 🌐 Deployment (Railway)

This project is deployed on **Railway** using **Gunicorn**.

### Environment Variables on Railway
```
GROQ_API_KEY=your_groq_api_key_here
```

### Procfile
```
web: gunicorn arena.wsgi:application
```

---

## 📁 Project Structure

```
AI_Debate_Arena/
├── manage.py
├── Procfile
├── requirements.txt
├── .gitignore
├── arena/                  # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── debate/                 # Main app
    ├── agents.py           # ProAgent, ConAgent, JudgeAgent
    ├── views.py
    ├── models.py
    ├── urls.py
    └── templates/
        ├── base.html
        ├── debate/
        │   └── arena.html
        └── registration/
            └── login.html
```

---

## 🔑 Login & Demo

Register your own account at the login page to get started.

> **Admin access:** `python manage.py createsuperuser`

---

## 👩‍💻 Author

**Maryam Asif Aziz**  
GitHub: [@maryamasifaziz](https://github.com/maryamasifaziz)

---
