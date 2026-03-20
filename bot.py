import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

FORCE_CHANNEL = "your_channel_username"

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== DEBUG START =====

@bot.on_message(filters.all)
async def debug_all(client, message):
    print("🔥 MESSAGE RECEIVED:", message.text)

# ===== JOIN CHECK =====

async def check_join(client, message):
    try:
        await client.get_chat_member(FORCE_CHANNEL, message.from_user.id)
        return True
    except:
        return False

def join_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_CHANNEL}")]
    ])

# ===== START =====

@bot.on_message(filters.command("start"))
async def start(client, message):
    print("✅ START COMMAND HIT")

    if not await check_join(client, message):
        return await message.reply("Join channel first", reply_markup=join_button())

    await message.reply("Bot working ✅")

# ===== MAIN =====

async def main():
    await bot.start()
    print("🤖 Bot Started Successfully")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
