import os
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "thumbbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

users = {}

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "Send a file.\n\n"
        "Then send thumbnail.\n"
        "Then send caption."
    )


@bot.on_message(filters.document | filters.video | filters.audio)
async def file_receive(client, message: Message):

    uid = message.from_user.id

    await message.reply_text("⬇ Downloading file...")

    file_path = await message.download()

    users[uid] = {"file": file_path}

    await message.reply_text("🖼 Now send thumbnail image.")


@bot.on_message(filters.photo)
async def thumb_receive(client, message: Message):

    uid = message.from_user.id

    if uid not in users:
        return

    thumb = await message.download()

    users[uid]["thumb"] = thumb

    await message.reply_text("✏ Now send caption text.")


@bot.on_message(filters.text & ~filters.command)
async def caption_receive(client, message: Message):

    uid = message.from_user.id

    if uid not in users:
        return

    caption = message.text
    file_path = users[uid]["file"]
    thumb = users[uid]["thumb"]

    await message.reply_text("⬆ Uploading file...")

    await message.reply_document(
        document=file_path,
        thumb=thumb,
        caption=caption
    )

    os.remove(file_path)
    os.remove(thumb)

    users.pop(uid)

    await message.reply_text("✅ Done!")

print("Bot Started Successfully")

bot.run()
