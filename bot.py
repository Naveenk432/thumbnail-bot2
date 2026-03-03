import os
from pyrogram import Client, filters

print("Loading variables...")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

print("Creating client...")

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.text)
async def echo(client, message):
    print("Message received:", message.text)
    await message.reply_text("Working: " + message.text)

print("Bot started successfully!")

app.run()
