import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait

# ===== Environment Variables =====
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ===== Create Bot =====
bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== Start Command =====
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    try:
        await message.reply_text("✅ Bot is working properly!")
    except FloodWait as e:
        print(f"FloodWait detected. Sleeping {e.value} seconds...")
        await asyncio.sleep(e.value)
        await message.reply_text("✅ Bot is working properly!")

# ===== Main Runner =====
async def main():
    print("🚀 Starting Bot...")
    await bot.start()
    print("✅ Bot Started Successfully!")
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
