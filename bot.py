import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Load environment variables safely
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Safety checks
if not API_ID or not API_HASH or not BOT_TOKEN:
    print("❌ Missing environment variables!")
    exit()

try:
    API_ID = int(API_ID)
except ValueError:
    print("❌ API_ID must be a number!")
    exit()

# Create bot
app = Client(
    "thumbnail_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("🚀 Bot started successfully")

# Start command
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("👋 Hello! Bot is working perfectly.")

# Keep bot alive
app.run()
