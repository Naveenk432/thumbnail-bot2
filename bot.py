import os
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "thumbnail_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

users = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send a file to begin.")

@bot.on_message(filters.document | filters.video | filters.audio)
async def file_handler(client, message):

    user_id = message.from_user.id

    await message.reply_text("Downloading file...")

    file_path = await message.download()

    users[user_id] = {"file": file_path}

    await message.reply_text("Now send thumbnail image.")

@bot.on_message(filters.photo)
async def thumb_handler(client, message):

    user_id = message.from_user.id

    if user_id not in users:
        return

    thumb = await message.download()

    users[user_id]["thumb"] = thumb

    await message.reply_text("Now send caption.")

@bot.on_message(filters.text & ~filters.command)
async def caption_handler(client, message):

    user_id = message.from_user.id

    if user_id not in users:
        return

    caption = message.text
    file_path = users[user_id]["file"]
    thumb = users[user_id]["thumb"]

    await message.reply_text("Uploading file...")

    await message.reply_document(
        document=file_path,
        thumb=thumb,
        caption=caption
    )

    os.remove(file_path)
    os.remove(thumb)

    users.pop(user_id)

    await message.reply_text("Finished!")

print("Bot Started Successfully")

bot.run()
