from pyrogram import Client, filters
import os

# ==============================
# BOT CONFIG
# ==============================

API_ID = 123456
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=100
)

# ==============================
# START COMMAND
# ==============================

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hello!\n\n"
        "Send me any video or file.\n"
        "I will download and resend it.\n\n"
        "Supports files up to 4GB 🚀"
    )

# ==============================
# FILE HANDLER
# ==============================

@bot.on_message(filters.video | filters.document)
async def process_file(client, message):

    status = await message.reply_text("📥 Downloading...")

    file_path = await message.download()

    await status.edit("✏ Send caption (or type /skip)")

    try:
        caption_msg = await bot.listen(message.chat.id)
        caption = caption_msg.text
        if caption == "/skip":
            caption = None
    except:
        caption = None

    await status.edit("🖼 Send thumbnail (or type /skip)")

    thumb = None
    try:
        thumb_msg = await bot.listen(message.chat.id)

        if thumb_msg.text == "/skip":
            thumb = None
        elif thumb_msg.photo:
            thumb = await thumb_msg.download()
    except:
        thumb = None

    await status.edit("📤 Uploading file...")

    await message.reply_document(
        file_path,
        caption=caption,
        thumb=thumb
    )

    os.remove(file_path)

    if thumb:
        os.remove(thumb)

    await status.delete()

# ==============================
# RUN BOT
# ==============================

print("Bot Started Successfully 🚀")

bot.run()
