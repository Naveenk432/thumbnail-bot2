import os
import logging
from pyrogram import Client, filters
from pyrogram.errors import RPCError

# ----------------------------
# Logging Setup
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("🚀 Starting Telegram Bot...")

# ----------------------------
# Load Environment Variables
# ----------------------------
try:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if not API_ID or not API_HASH or not BOT_TOKEN:
        raise ValueError("Missing environment variables!")

except Exception as e:
    print("❌ Environment Variable Error:", e)
    exit(1)

# ----------------------------
# Create Client
# ----------------------------
app = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ----------------------------
# Handlers
# ----------------------------
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("👋 Hello! Bot is working perfectly.")

@app.on_message(filters.command("ping"))
async def ping_handler(client, message):
    await message.reply_text("🏓 Pong! Bot is alive.")

@app.on_message(filters.private & filters.document)
async def document_handler(client, message):
    await message.reply_text("📁 File received successfully!")

# ----------------------------
# Run Bot
# ----------------------------
try:
    print("✅ Bot is running...")
    app.run()
except RPCError as e:
    print("❌ Telegram RPC Error:", e)
except Exception as e:
    print("❌ Unexpected Error:", e)
