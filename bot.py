import os
from pyrogram import Client, filters

api_id = int(os.getenv("22580782"))
api_hash = os.getenv("946a0cc78ab034f489ebd3584f7b3152")
bot_token = os.getenv("8306956637:AAFvt2fEhH057P1dyh3jlG6J712WE7vlJ14")

app = Client("thumb_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

user_files = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send or forward a file 📁\nThen send thumbnail 🖼")

# Store original message (not file)
@app.on_message(filters.document | filters.video)
async def save_file(client, message):
    user_files[message.from_user.id] = message
    await message.reply_text("✅ File saved in Telegram cloud!\nNow send thumbnail.")

# Apply thumbnail
@app.on_message(filters.photo)
async def apply_thumb(client, message):
    user_id = message.from_user.id

    if user_id not in user_files:
        await message.reply_text("❌ First send a file.")
        return

    thumb_path = await message.download()
    original_message = user_files[user_id]

    await original_message.copy(
        chat_id=message.chat.id,
        thumb=thumb_path,
        caption="✅ Processed using Telegram Cloud ☁🔥"
    )

    os.remove(thumb_path)
    del user_files[user_id]

print("Cloud Thumbnail Bot Running ☁🔥")
app.run()
