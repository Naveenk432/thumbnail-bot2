import os
from pyrogram import Client, filters
from pyrogram.types import Message

# =============================
# GET ENVIRONMENT VARIABLES
# =============================

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_ID or not API_HASH or not BOT_TOKEN:
    print("❌ Missing environment variables!")
    exit()

# Convert API_ID to integer safely
try:
    API_ID = int(API_ID)
except ValueError:
    print("❌ API_ID must be a number!")
    exit()

# =============================
# CREATE BOT CLIENT
# =============================

app = Client(
    "thumbnail_bot",
   import os
from pyrogram import Client

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "thumbnail_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("Bot is running...")

app.run()

print("✅ Bot is starting...")

# =============================
# COMMAND: /start
# =============================

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text(
        "👋 Hello!\n\nSend me a file and I will process it."
    )

# =============================
# HANDLE DOCUMENT FILES
# =============================

@app.on_message(filters.document)
async def file_handler(client, message: Message):
    await message.reply_text("📂 File received successfully!")

print("🚀 Bot is running...")

# =============================
# RUN BOT
# =============================

app.run()

