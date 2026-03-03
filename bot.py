import os
import threading
import time
from flask import Flask
from pyrogram import Client, filters

# Flask keep-alive server
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot running"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# Telegram bot
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("👋 Bot working!")

print("Bot starting...")
bot.start()
print("Bot started!")

while True:
    time.sleep(100)
