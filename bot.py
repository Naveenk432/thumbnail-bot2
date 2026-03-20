import os
import asyncio

# 🔥 IMPORTANT FIX (for Python 3.14)
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters, idle

# ✅ ENV VARIABLES
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ✅ BOT CLIENT
bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

# ✅ STORAGE
thumbs = {}
captions = {}
wait_thumb = set()
wait_caption = set()


# ✅ START
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hello!\n\n"
        "/setthumb - Set thumbnail\n"
        "/setcaption - Set caption\n\n"
        "Then send any file."
    )


# ✅ SET THUMB
@bot.on_message(filters.command("setthumb"))
async def set_thumb(client, message):
    if not message.from_user:
        return
    wait_thumb.add(message.from_user.id)
    await message.reply_text("📸 Send image for thumbnail")


# ✅ SAVE THUMB
@bot.on_message(filters.photo)
async def save_thumb(client, message):
    if not message.from_user:
        return

    user = message.from_user.id

    if user in wait_thumb:
        try:
            file = await message.download()
            thumbs[user] = file
            wait_thumb.remove(user)
            await message.reply_text("✅ Thumbnail saved")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")


# ✅ SET CAPTION
@bot.on_message(filters.command("setcaption"))
async def set_caption(client, message):
    if not message.from_user:
        return
    wait_caption.add(message.from_user.id)
    await message.reply_text("✍️ Send caption text")


# ✅ SAVE CAPTION
@bot.on_message(filters.text & ~filters.command(["start", "setthumb", "setcaption"]))
async def save_caption(client, message):
    if not message.from_user:
        return

    user = message.from_user.id

    if user in wait_caption:
        captions[user] = message.text
        wait_caption.remove(user)
        await message.reply_text("✅ Caption saved")


# ✅ PROCESS FILE
@bot.on_message(filters.document | filters.video)
async def process_file(client, message):
    if not message.from_user:
        return

    user = message.from_user.id

    try:
        status = await message.reply_text("📥 Downloading...")

        file_path = await message.download()

        await status.edit("📤 Uploading...")

        await message.reply_document(
            file_path,
            caption=captions.get(user, ""),
            thumb=thumbs.get(user, None),
            force_document=True
        )

        os.remove(file_path)

        await status.delete()

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


# ✅ MAIN RUN (WORKS ON PYTHON 3.14)
async def main():
    await bot.start()
    print("🤖 Bot Started Successfully")
    await idle()


if __name__ == "__main__":
    asyncio.run(main())
