import os
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

thumbs = {}
captions = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hello!\n\n"
        "Commands:\n"
        "/setthumb - Set thumbnail\n"
        "/setcaption - Set caption\n\n"
        "Then send a file."
    )

# SET THUMBNAIL
@bot.on_message(filters.command("setthumb"))
async def set_thumb(client, message):
    await message.reply_text("📸 Send me the image to set as thumbnail.")

@bot.on_message(filters.photo)
async def save_thumb(client, message):
    user_id = message.from_user.id

    file = await message.download()

    thumbs[user_id] = file

    await message.reply_text("✅ Thumbnail saved!")

# SET CAPTION
@bot.on_message(filters.command("setcaption"))
async def set_caption(client, message):
    await message.reply_text("✏️ Send me the caption text.")

@bot.on_message(filters.text & ~filters.command)
async def save_caption(client, message):
    user_id = message.from_user.id

    captions[user_id] = message.text

    await message.reply_text("✅ Caption saved!")

# HANDLE FILE
@bot.on_message(filters.video | filters.document)
async def handle_file(client, message):
    user_id = message.from_user.id

    msg = await message.reply_text("📥 Downloading file...")

    file_path = await message.download()

    thumb = thumbs.get(user_id)
    caption = captions.get(user_id)

    await msg.edit("📤 Uploading file...")

    await message.reply_document(
        file_path,
        caption=caption,
        thumb=thumb
    )

    os.remove(file_path)

    await msg.delete()

print("🚀 Starting Bot...")
bot.run()

