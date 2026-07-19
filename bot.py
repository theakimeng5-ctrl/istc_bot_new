"""
ISTC AI Telegram Bot — Single File Version
Deploy on Railway.app | No subfolders needed.

Requirements:
    pip install python-telegram-bot[webhooks] google-generativeai openai python-dotenv
"""

import logging
import os
from dotenv import load_dotenv

# ── Load .env (local dev only; Railway uses dashboard env vars) ────────────────
load_dotenv()

import google.generativeai as genai
from openai import AsyncOpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

TELEGRAM_TOKEN  = os.getenv("TELEGRAM_TOKEN", "")
WEBHOOK_SECRET  = os.getenv("WEBHOOK_SECRET", "istc_secret_token")
WEBHOOK_URL     = os.getenv("WEBHOOK_URL", "")          # empty = polling mode
PORT            = int(os.getenv("PORT", 8443))

AI_PROVIDER     = os.getenv("AI_PROVIDER", "gemini")    # "gemini" | "openai"
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL    = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL    = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

BOT_NAME        = os.getenv("BOT_NAME", "ISTC AI Assistant")
MAX_HISTORY     = int(os.getenv("MAX_HISTORY", "20"))
SYSTEM_PROMPT   = os.getenv(
    "SYSTEM_PROMPT",
    "You are ISTC AI, a helpful and friendly assistant. "
    "Answer clearly and concisely. "
    "Always respond in the same language the user writes in.",
)

# ── Validate required variables ────────────────────────────────────────────────
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is not set!")
if AI_PROVIDER == "gemini" and not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set!")
if AI_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set!")

# ══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# AI SERVICE
# ══════════════════════════════════════════════════════════════════════════════

# Per-user conversation history  {user_id: [{"role": ..., "content": ...}, ...]}
_sessions: dict[int, list[dict]] = {}

# ── Setup AI client ────────────────────────────────────────────────────────────
if AI_PROVIDER == "gemini":
    genai.configure(api_key=GEMINI_API_KEY)
    
    _gemini_model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT,
    )
    logger.info(f"Gemini AI ready ({GEMINI_MODEL})")
else:
    _openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    logger.info(f"OpenAI ready ({OPENAI_MODEL})")


def _update_history(user_id: int, user_msg: str, assistant_msg: str) -> None:
    """Append turn to history and trim to MAX_HISTORY pairs."""
    if user_id not in _sessions:
        _sessions[user_id] = []
    _sessions[user_id].append({"role": "user",  "content": user_msg})
    _sessions[user_id].append({"role": "model", "content": assistant_msg})
    cap = MAX_HISTORY * 2
    if len(_sessions[user_id]) > cap:
        _sessions[user_id] = _sessions[user_id][-cap:]


def clear_history(user_id: int) -> None:
    _sessions.pop(user_id, None)


def history_length(user_id: int) -> int:
    return len(_sessions.get(user_id, [])) // 2


async def _gemini_chat(user_id: int, message: str) -> str:
    history = _sessions.get(user_id, [])
    gemini_history = [
        {"role": turn["role"], "parts": [turn["content"]]}
        for turn in history
    ]
    chat = _gemini_model.start_chat(history=gemini_history)
    response = await chat.send_message_async(message)
    reply = response.text
    _update_history(user_id, message, reply)
    return reply


async def _openai_chat(user_id: int, message: str) -> str:
    history = _sessions.get(user_id, [])
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history:
        role = "assistant" if turn["role"] == "model" else turn["role"]
        messages.append({"role": role, "content": turn["content"]})
    messages.append({"role": "user", "content": message})
    response = await _openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7,
    )
    reply = response.choices[0].message.content
    _update_history(user_id, message, reply)
    return reply


async def ai_chat(user_id: int, message: str) -> str:
    """Main entry-point: route to the configured AI provider."""
    try:
        if AI_PROVIDER == "gemini":
            return await _gemini_chat(user_id, message)
        else:
            return await _openai_chat(user_id, message)
    except Exception as e:
        logger.error(f"AI error for user {user_id}: {e}", exc_info=True)
        return (
            "Sorry, I encountered an error. Please try again in a moment."
        )

# ══════════════════════════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("Clear Chat", callback_data="clear"),
        ],
        [InlineKeyboardButton("About", callback_data="about")],
    ]
    text = (
        f"Hello, *{user.first_name}*!\n\n"
        f"I am *{BOT_NAME}* — your intelligent AI assistant.\n\n"
        "*What I can help with:*\n"
        "- Answer questions & explain concepts\n"
        "- Help with coding & debugging\n"
        "- Write & proofread text\n"
        "- Translate languages\n"
        "- Solve math & logic problems\n\n"
        "Just send me any message to get started!"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    logger.info(f"/start from {user.id} (@{user.username})")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"*{BOT_NAME} — Help*\n\n"
        "Just type any message to chat with me!\n\n"
        "*Commands:*\n"
        "- /start — Welcome message\n"
        "- /help  — Show this help\n"
        "- /clear — Clear conversation history\n"
        "- /about — Bot info\n\n"
        "_I remember your conversation context. Use /clear to start fresh._"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clear_history(update.effective_user.id)
    await update.message.reply_text(
        "*Conversation cleared!* Send me a message to start fresh.",
        parse_mode="Markdown",
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model = GEMINI_MODEL if AI_PROVIDER == "gemini" else OPENAI_MODEL
    text = (
        f"*About {BOT_NAME}*\n\n"
        f"- AI Engine: {AI_PROVIDER.upper()}\n"
        f"- Model: `{model}`\n"
        f"- Framework: python-telegram-bot v21\n"
        f"- Hosted on: Railway.app\n\n"
        "Built with love by ISTC"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ══════════════════════════════════════════════════════════════════════════════
# MESSAGE HANDLER
# ══════════════════════════════════════════════════════════════════════════════

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_msg = update.message.text
    logger.info(f"Msg from {user.id}: {user_msg[:80]}")

    await update.message.chat.send_action(ChatAction.TYPING)

    reply = await ai_chat(user_id=user.id, message=user_msg)

    # Split replies longer than Telegram's 4096-char limit
    for i in range(0, len(reply), 4096):
        chunk = reply[i : i + 4096]
        try:
            await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception:
            # Fallback without Markdown if parsing fails
            await update.message.reply_text(chunk)

# ══════════════════════════════════════════════════════════════════════════════
# CALLBACK HANDLER (inline buttons)
# ══════════════════════════════════════════════════════════════════════════════

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "help":
        text = (
            f"*{BOT_NAME} — Help*\n\n"
            "Just type any message to chat!\n\n"
            "*Commands:*\n"
            "- /start — Welcome\n"
            "- /help  — Help\n"
            "- /clear — Clear history\n"
            "- /about — About"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

    elif data == "clear":
        clear_history(update.effective_user.id)
        await query.edit_message_text(
            "*Conversation cleared!* Send me a message to start fresh.",
            parse_mode="Markdown",
        )

    elif data == "about":
        model = GEMINI_MODEL if AI_PROVIDER == "gemini" else OPENAI_MODEL
        text = (
            f"*About {BOT_NAME}*\n\n"
            f"- AI Engine: {AI_PROVIDER.upper()}\n"
            f"- Model: `{model}`\n"
            f"- Framework: python-telegram-bot v21\n"
            f"- Hosted on: Railway.app\n\n"
            "Built with love by ISTC"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("about", about_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inline buttons
    app.add_handler(CallbackQueryHandler(handle_callback))

    if WEBHOOK_URL:
        logger.info(f"Running in WEBHOOK mode on port {PORT}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            secret_token=WEBHOOK_SECRET,
            webhook_url=f"{WEBHOOK_URL}/webhook",
            url_path="/webhook",
        )
    else:
        logger.info("Running in POLLING mode (local development)")
        app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
