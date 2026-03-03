import os
import threading
from flask import Flask
from pyrogram import Client, filters, idle

# Environment variables
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Create bot
bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Flask app (required for Railway)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Telegram handlers
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("✅ Bot is working!")

# Run bot in background
def run_bot():
    bot.start()
    print("✅ Bot Started Successfully!")
    idle()
    bot.stop()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
