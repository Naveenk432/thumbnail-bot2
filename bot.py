import os
import threading
from flask import Flask
from pyrogram import Client, filters, idle

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_bot():
    bot.start()
    print("Bot Started Successfully!")
    idle()
    bot.stop()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
