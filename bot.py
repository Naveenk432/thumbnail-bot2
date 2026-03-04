import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hello!\n\nSend me a video or file and I will return it with a thumbnail."
    )

# Handle video/document
@bot.on_message(filters.video | filters.document)
async def handle_file(client, message):
    try:
        msg = await message.reply_text("📥 Downloading file...")

        file_path = await message.download()

        await msg.edit("🖼 Creating thumbnail...")

        thumb = await client.download_media(message.from_user.photo.big_file_id) if message.from_user.photo else None

        await msg.edit("📤 Uploading file with thumbnail...")

        await message.reply_document(
            file_path,
            thumb=thumb
        )

        await msg.delete()

        os.remove(file_path)
        if thumb:
            os.remove(thumb)

    except FloodWait as e:
        await asyncio.sleep(e.value)

# Run bot
print("🚀 Starting Bot...")
bot.run()
