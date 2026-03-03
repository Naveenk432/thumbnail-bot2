import os
import threading
from flask import Flask
from pyrogram import Client, filters

# -----------------------
# Flask Web Server
# -----------------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# Start web server in background thread
threading.Thread(target=run_web).start()

print("🌐 Web server started")

# -----------------------
# Telegram Bot
# -----------------------
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    print("Message received:", message.text)
    await message.reply_text("👋 Hello! Bot is working perfectly.")

@app.on_message(filters.command("ping"))
async def ping_handler(client, message):
    await message.reply_text("🏓 Pong!")

print("🚀 Bot starting...")
app.run()
