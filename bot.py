import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# ================= CONFIG =================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

FORCE_CHANNEL = "your_channel_username"   # without @

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

# ================= STORAGE =================
thumbs = {}
captions = {}
wait_thumb = set()
wait_caption = set()

# ================= JOIN CHECK =================

async def check_join(client, message):
    try:
        user_id = message.from_user.id
        await client.get_chat_member(FORCE_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return True

def join_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{FORCE_CHANNEL}")],
        [InlineKeyboardButton("✅ I Joined", callback_data="check_join")]
    ])

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(client, message):

    if not await check_join(client, message):
        return await message.reply_text(
            "❌ You must join our channel first!",
            reply_markup=join_button()
        )

    await message.reply_text(
        "👋 Welcome!\n\n"
        "/setthumb - Set thumbnail\n"
        "/setcaption - Set caption\n\n"
        "Send any file 📁"
    )

# ================= CALLBACK =================

@bot.on_callback_query(filters.regex("check_join"))
async def join_callback(client, callback_query):

    if not await check_join(client, callback_query.message):
        return await callback_query.answer("❌ You didn't join yet!", show_alert=True)

    await callback_query.message.edit_text(
        "✅ You joined successfully!\n\nNow you can use the bot."
    )

# ================= THUMB =================

@bot.on_message(filters.command("setthumb"))
async def set_thumb(client, message):

    if not await check_join(client, message):
        return await message.reply_text(
            "❌ Join channel first",
            reply_markup=join_button()
        )

    wait_thumb.add(message.from_user.id)
    await message.reply_text("📸 Send thumbnail image")

@bot.on_message(filters.photo)
async def save_thumb(client, message):

    user = message.from_user.id

    if user in wait_thumb:
        file = await message.download()
        thumbs[user] = file
        wait_thumb.remove(user)

        await message.reply_text("✅ Thumbnail saved")

# ================= CAPTION =================

@bot.on_message(filters.command("setcaption"))
async def set_caption(client, message):

    if not await check_join(client, message):
        return await message.reply_text(
            "❌ Join channel first",
            reply_markup=join_button()
        )

    wait_caption.add(message.from_user.id)
    await message.reply_text("✍️ Send caption text")

@bot.on_message(filters.text & ~filters.command(["start", "setthumb", "setcaption"]))
async def save_caption(client, message):

    user = message.from_user.id

    if user in wait_caption:
        captions[user] = message.text
        wait_caption.remove(user)

        await message.reply_text("✅ Caption saved")

# ================= FILE PROCESS =================

@bot.on_message(filters.document | filters.video)
async def process_file(client, message):

    if not await check_join(client, message):
        return await message.reply_text(
            "❌ Join channel to use bot",
            reply_markup=join_button()
        )

    user = message.from_user.id
    status = await message.reply_text("📥 Downloading...")

    try:
        file_path = await message.download()

        await status.edit("📤 Uploading...")

        await message.reply_document(
            document=file_path,
            caption=captions.get(user, ""),
            thumb=thumbs.get(user, None),
            force_document=True
        )

        os.remove(file_path)
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ Error: {e}")

# ================= MAIN =================

async def main():
    await bot.start()
    print("🤖 Bot Started Successfully")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
