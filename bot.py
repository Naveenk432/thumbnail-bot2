import os
from pyrogram import Client, filters

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
async def start(client, message):
    await message.reply_text("Bot is working!")

@bot.on_message(filters.text & ~filters.command)
async def text_handler(client, message):
    await message.reply_text("You sent: " + message.text)

print("Bot started")

bot.run()
