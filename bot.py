import os
import threading
from flask import Flask
from pyrogram import Client, filters

# ----------------------
# Telegram Bot Setup
# ----------------------

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    print("Received:", message.text)
    await message.reply_text("👋 Bot is working perfectly!")

# ----------------------
# Flask Keep-Alive Server
# ----------------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ----------------------
# Start Everything Properly
# ----------------------

print("🚀 Starting Bot...")

bot.start()  # Start Telegram bot FIRST
print("✅ Telegram Bot Started!")

# Start Flask in background thread
threading.Thread(target=run_flask).start()

print("🌐 Web Server Started!")

bot.idle()  # Keep bot alive properly
