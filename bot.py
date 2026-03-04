from pyrogram import Client, filters
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=60
)

user_files = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hello!\n\nSend me a file.\n"
        "I will ask for description and thumbnail."
    )

# Step 1: receive file
@bot.on_message(filters.video | filters.document)
async def receive_file(client, message):

    msg = await message.reply_text("📥 Downloading file...")

    file_path = await message.download()

    user_files[message.chat.id] = {"file": file_path}

    await msg.edit("✏ Send description text")

# Step 2: receive description
@bot.on_message(filters.text & ~filters.command)
async def receive_description(client, message):

    if message.chat.id not in user_files:
        return

    user_files[message.chat.id]["caption"] = message.text

    await message.reply_text("🖼 Send thumbnail image")

# Step 3: receive thumbnail
@bot.on_message(filters.photo)
async def receive_thumbnail(client, message):

    if message.chat.id not in user_files:
        return

    thumb = await message.download()

    data = user_files[message.chat.id]

    await message.reply_text("📤 Uploading file...")

    await message.reply_document(
        data["file"],
        caption=data["caption"],
        thumb=thumb
    )

    os.remove(data["file"])
    os.remove(thumb)

    del user_files[message.chat.id]

print("Bot Started Successfully 🚀")

bot.run()

