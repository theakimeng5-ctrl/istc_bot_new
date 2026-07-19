# 📦 Student Guide: Upload ISTC AI Bot to GitHub & Deploy on Railway

---

## 🗂️ STEP 1 — Get the Project Files

Your teacher will share a file called **`ISTC-AI-Bot.zip`**.

1. Download it to your computer
2. **Right-click** the ZIP → **Extract All...**
3. Choose a folder, e.g. `Documents/ISTC-AI-Bot`
4. Open the extracted folder — you should see:

```
ISTC-AI-Bot/
├── bot.py
├── config.py
├── requirements.txt
├── railway.toml
├── Procfile
├── .python-version
├── .gitignore
├── .env.example      ← template (DO NOT put real keys here)
├── README.md
├── handlers/
│   ├── commands.py
│   ├── messages.py
│   └── callbacks.py
└── services/
    └── ai_service.py
```

---

## 🐙 STEP 2 — Create a GitHub Account

1. Go to **https://github.com**
2. Click **Sign up** → fill your details → verify email
3. Log in to your account

---

## 📁 STEP 3 — Create a New Repository

1. Click the **+** button (top right) → **New repository**
2. Fill in:
   - **Repository name:** `istc-ai-bot`
   - **Description:** `ISTC AI Telegram Bot`
   - Visibility: **Public**
   - Do NOT check "Add a README file"
3. Click **Create repository**

---

## ⬆️ STEP 4 — Upload Files to GitHub

### Option A — Upload via Browser (Easiest)

1. On your new empty repo page, click **uploading an existing file**
2. Drag and drop ALL extracted files into the browser window
3. Scroll down → type commit message: `Initial commit`
4. Click **Commit changes**

> ⚠️ GitHub browser upload does NOT support folders directly.
> Upload the root files first, then for `handlers/` and `services/`:
> Click **Add file → Upload files** again, and type the path manually like `handlers/commands.py`

### Option B — Upload via Git (Recommended)

Open **Command Prompt** or **PowerShell** inside the project folder, then run:

```powershell
git init
git remote add origin https://github.com/YOUR_USERNAME/istc-ai-bot.git
git add .
git commit -m "Initial commit: ISTC AI Bot"
git branch -M main
git push -u origin main
```

> GitHub will ask for your username + a Personal Access Token (not your password).
> Get token: GitHub → Settings → Developer Settings → Personal access tokens → Generate new token

---

## 🔑 STEP 5 — Get Your API Keys

### A) Telegram Bot Token
1. Open Telegram → search **@BotFather**
2. Send: `/newbot`
3. Pick a name (e.g. `ISTC AI Bot`) and username (e.g. `istc_ai_bot`)
4. Copy the token: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### B) Google Gemini API Key (Free!)
1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with Google account
3. Click **Create API Key** → copy it

---

## ☁️ STEP 6 — Deploy on Railway

1. Go to **https://railway.app** → **Login with GitHub**
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your `istc-ai-bot` repository
4. Railway builds it automatically

### Add Environment Variables

Click your service → **Variables** tab → add each one:

| Variable | Value |
|---|---|
| `TELEGRAM_TOKEN` | Your token from @BotFather |
| `GEMINI_API_KEY` | Your key from AI Studio |
| `AI_PROVIDER` | `gemini` |
| `BOT_NAME` | `ISTC AI Assistant` |
| `WEBHOOK_SECRET` | Any random string (e.g. `secret123`) |

### Get Your Public URL

Service → **Settings** → **Networking** → **Generate Domain**

Copy the URL, e.g. `https://istc-ai-bot.up.railway.app`

### Add Webhook Variables

Back in **Variables** tab, also add:

| Variable | Value |
|---|---|
| `WEBHOOK_URL` | `https://istc-ai-bot.up.railway.app` |
| `PORT` | `8443` |

Railway will redeploy automatically. Your bot is now **LIVE!** 🎉

---

## 🧪 STEP 7 — Test Your Bot

1. Open Telegram
2. Search for your bot username (e.g. `@istc_ai_bot`)
3. Send `/start`
4. The bot should reply with a welcome message!

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| Bot doesn't respond | Railway → Service → Deployments → View Logs |
| "TELEGRAM_TOKEN not set" error | Check Variables tab in Railway |
| AI gives no reply | Check `GEMINI_API_KEY` is correct |
| `git push` rejected | Use Personal Access Token, not password |
| Can't find `.gitignore` file | Enable "Show hidden files" in Windows Explorer |

---

## 🔒 Security Rules

> [!CAUTION]
> NEVER put your real API keys in the code files or share your `.env` file!
> The `.gitignore` file already prevents `.env` from being uploaded to GitHub.

```
NEVER share:  .env             (contains your real secret keys)
Safe to share: .env.example    (just a template with no real keys)
```

---

*Made with love by ISTC — Good luck with your bot! 🚀*
