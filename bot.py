import os
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "thumbnail_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

user_data = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send a file.")

@bot.on_message(filters.document | filters.video | filters.audio)
async def file_receive(client, message):
    user_id = message.from_user.id

    await message.reply_text("Downloading file...")

    file_path = await message.download()

    user_data[user_id] = {"file": file_path}

    await message.reply_text("Send thumbnail image.")

@bot.on_message(filters.photo)
async def thumb_receive(client, message):

    user_id = message.from_user.id

    if user_id not in user_data:
        return

    thumb = await message.download()

    user_data[user_id]["thumb"] = thumb

    await message.reply_text("Send caption text.")

@bot.on_message(filters.text & ~filters.command)
async def caption_receive(client, message):

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

print("Bot Started Successfully")

bot.run()
