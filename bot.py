import os
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

users = {}

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    users[message.from_user.id] = {}
    await message.reply_text(
        "Send me the file you want to edit.\n\n"
        "After that I will ask thumbnail and description."
    )


@bot.on_message(filters.document | filters.video | filters.audio)
async def get_file(client, message: Message):
    user_id = message.from_user.id
    users[user_id] = {}

    await message.reply_text("⬇ Downloading file...")

    file_path = await message.download()

    users[user_id]["file"] = file_path

    await message.reply_text("🖼 Now send thumbnail image.")


@bot.on_message(filters.photo)
async def get_thumb(client, message: Message):
    user_id = message.from_user.id

    if user_id not in users or "file" not in users[user_id]:
        return

    thumb = await message.download()
    users[user_id]["thumb"] = thumb

    await message.reply_text("✏ Send description / caption.")


@bot.on_message(filters.text & ~filters.command)
async def get_caption(client, message: Message):
    user_id = message.from_user.id

    if user_id not in users or "thumb" not in users[user_id]:
        return

    caption = message.text
    users[user_id]["caption"] = caption

    file_path = users[user_id]["file"]
    thumb = users[user_id]["thumb"]

    await message.reply_text("⬆ Uploading file...")

    await message.reply_document(
        document=file_path,
        thumb=thumb,
        caption=caption
    )

    os.remove(file_path)
    os.remove(thumb)

    users.pop(user_id)

    await message.reply_text("✅ Done!")

bot.run()
