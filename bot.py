import os
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user_files = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send a file.")

@bot.on_message(filters.document | filters.video | filters.audio)
async def receive_file(client, message):
    uid = message.from_user.id
    file_path = await message.download()
    user_files[uid] = file_path
    await message.reply_text("Send caption text.")

@bot.on_message(filters.text & ~filters.command)
async def receive_caption(client, message):
    uid = message.from_user.id

    if uid not in user_files:
        return

    file_path = user_files[uid]
    caption = message.text

    await message.reply_document(
        document=file_path,
        caption=caption
    )

    os.remove(file_path)
    del user_files[uid]

    await message.reply_text("Done")

print("Bot Started")

bot.run()

