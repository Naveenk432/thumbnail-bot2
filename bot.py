import os
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "thumbnailbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=60
)

user_data = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send a file to start.")

@bot.on_message(filters.document | filters.video | filters.audio)
async def get_file(client, message):
    user_id = message.from_user.id
    file_path = await message.download()

    user_data[user_id] = {"file": file_path}

    await message.reply_text("Send thumbnail image.")

@bot.on_message(filters.photo)
async def get_thumb(client, message):
    user_id = message.from_user.id

    if user_id not in user_data:
        return

    thumb = await message.download()
    user_data[user_id]["thumb"] = thumb

    await message.reply_text("Send caption text.")

@bot.on_message(filters.text & ~filters.command)
async def get_caption(client, message):
    user_id = message.from_user.id

    if user_id not in user_data:
        return

    caption = message.text
    file_path = user_data[user_id]["file"]
    thumb = user_data[user_id]["thumb"]

    await message.reply_document(
        document=file_path,
        thumb=thumb,
        caption=caption
    )

    os.remove(file_path)
    os.remove(thumb)

    user_data.pop(user_id)

    await message.reply_text("Done!")

bot.run()

