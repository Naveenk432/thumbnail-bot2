import os
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

user_data = {}

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "Hello!\n\nSend a file.\n"
        "Then send thumbnail.\n"
        "Then send caption."
    )

@bot.on_message(filters.document | filters.video | filters.audio)
async def receive_file(client, message: Message):

    user_id = message.from_user.id

    await message.reply_text("Downloading file...")

    file_path = await message.download()

    user_data[user_id] = {"file": file_path}

    await message.reply_text("Now send thumbnail image.")

@bot.on_message(filters.photo)
async def receive_thumb(client, message: Message):

    user_id = message.from_user.id

    if user_id not in user_data:
        return

    thumb_path = await message.download()

    user_data[user_id]["thumb"] = thumb_path

    await message.reply_text("Now send caption text.")

@bot.on_message(filters.text & ~filters.command)
async def receive_caption(client, message: Message):

    user_id = message.from_user.id

    if user_id not in user_data:
        return

    caption = message.text
    file_path = user_data[user_id]["file"]
    thumb_path = user_data[user_id]["thumb"]

    await message.reply_text("Uploading file...")

    await message.reply_document(
        document=file_path,
        thumb=thumb_path,
        caption=caption
    )

    os.remove(file_path)
    os.remove(thumb_path)

    user_data.pop(user_id)

    await message.reply_text("Done!")

print("Bot Started Successfully")

bot.run()
