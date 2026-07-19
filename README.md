# 🤖 ISTC AI Telegram Bot

A production-ready AI-powered Telegram bot built with **python-telegram-bot v21**, supporting **Google Gemini** and **OpenAI**, deployed on **Railway.app**.

---

## ✨ Features

- 🧠 **Dual AI engine** – Google Gemini (default) or OpenAI GPT
- 💬 **Conversation memory** – per-user chat history with configurable length
- ⚡ **Webhook mode** on Railway, **polling mode** for local dev
- 🎛️ **Inline keyboard** buttons for quick actions
- 📝 **Long message splitting** – handles Telegram's 4096-char limit
- 🔒 **Secure** – secrets via environment variables, never in code

---

## 📁 Project Structure

```
AI Bot ISTC/
├── bot.py                  # Entry point
├── config.py               # Configuration (env vars)
├── handlers/
│   ├── commands.py         # /start /help /clear /about
│   ├── messages.py         # Text message handler
│   └── callbacks.py        # Inline button handler
├── services/
│   └── ai_service.py       # Gemini + OpenAI wrapper
├── requirements.txt
├── railway.toml            # Railway deployment config
├── Procfile
├── .python-version
├── .env.example            # Template – copy to .env
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone <your-repo>
cd "AI Bot ISTC"
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your actual keys
```

### 3. Get API Keys

| Key | How to get |
|-----|-----------|
| `TELEGRAM_TOKEN` | Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) |

### 4. Run Locally

```bash
python bot.py
```

The bot will start in **polling mode** automatically when `WEBHOOK_URL` is not set.

---

## ☁️ Deploy to Railway

### Step 1 – Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/istc-ai-bot.git
git push -u origin main
```

### Step 2 – Create Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your repository
4. Railway will auto-detect Python and install dependencies

### Step 3 – Add Environment Variables

In Railway dashboard → your service → **Variables** tab, add:

```
TELEGRAM_TOKEN     = <your bot token>
GEMINI_API_KEY     = <your gemini key>
AI_PROVIDER        = gemini
BOT_NAME           = ISTC AI Assistant
WEBHOOK_SECRET     = <random strong string>
```

> ⚠️ Do NOT add `WEBHOOK_URL` yet — do this AFTER deploy.

### Step 4 – Generate Railway Domain

1. Railway service → **Settings** → **Networking** → **Generate Domain**
2. Copy the generated URL (e.g., `https://istc-ai-bot.up.railway.app`)

### Step 5 – Add Webhook URL

Back in **Variables** tab, add:

```
WEBHOOK_URL = https://istc-ai-bot.up.railway.app
PORT        = 8443
```

Railway will redeploy automatically. Your bot is now live! 🎉

---

## 🔧 Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_TOKEN` | *(required)* | Your Telegram bot token |
| `GEMINI_API_KEY` | *(required if gemini)* | Google Gemini API key |
| `OPENAI_API_KEY` | *(required if openai)* | OpenAI API key |
| `AI_PROVIDER` | `gemini` | `gemini` or `openai` |
| `GEMINI_MODEL` | `gemini-pro` | Gemini model name |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model name |
| `BOT_NAME` | `ISTC AI Assistant` | Display name |
| `MAX_HISTORY` | `20` | Max conversation turns to remember |
| `SYSTEM_PROMPT` | *(see config.py)* | AI system instruction |
| `WEBHOOK_URL` | *(empty = polling)* | Public URL for webhook mode |
| `WEBHOOK_SECRET` | `my-secret-token` | Webhook validation secret |
| `PORT` | `8443` | Webhook server port |

---

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message + quick action buttons |
| `/help` | Show help menu |
| `/clear` | Clear your conversation history |
| `/about` | Bot info and AI model details |

---

## 🛠️ Switching Between Gemini and OpenAI

Set `AI_PROVIDER` in your environment:

```bash
# Use Gemini (default)
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-pro  # or gemini-1.5-pro

# Use OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini  # or gpt-4o
```

---

## 📝 License

MIT License – Built with ❤️ by ISTC
