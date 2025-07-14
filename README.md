# 🤖 Scheduling Assistant (AI + Google Calendar + Flask)

A smart meeting scheduler powered by **Meta LLaMA 3**, **Google Calendar**, and **Flask**, deployed via **Cloudflare Tunnel**.  
It extracts meeting info from natural language and finds optimal meeting slots for multiple attendees.

---

## 📦 Features
- 🔍 Extracts date, time, and duration from natural email/text using LLaMA 3
- 📅 Checks attendee availability via Google Calendar API
- ⚙️ Auto-suggests conflict-free meeting slots
- ☁️ Deployable using Cloudflare for public testing

---

## 🚀 Getting Started

### Prerequisites:
- Python 3.10+
- vLLM LLaMA-3 running locally on `http://localhost:4000`
- Google Calendar API access tokens stored in `creds/`

### Setup:
```bash
pip install -r requirements.txt
python app1.py
