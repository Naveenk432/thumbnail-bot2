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
    workers=50
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hello 👋\n\nSend me a file and I will download and resend it."
    )

@bot.on_message(filters.video | filters.document)
async def handle_file(client, message):

    msg = await message.reply_text("📥 Downloading...")

    file_path = await message.download()

    await msg.edit("📤 Uploading...")

    await message.reply_document(file_path)

    os.remove(file_path)

    await msg.delete()

print("Bot Started Successfully 🚀")

bot.run()
