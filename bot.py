import os
import asyncio
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "test-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    print("START COMMAND RECEIVED")
    await message.reply_text("✅ Bot is working!")

async def main():
    await bot.start()
    print("🔥 BOT RUNNING")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
