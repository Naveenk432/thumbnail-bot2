import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# ---------------- CONFIG ----------------
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "your_channel_username"  # بدون @

bot = Client(
    "rename-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

# ---------------- STORAGE ----------------
thumbs = {}
captions = {}
wait_thumb = set()
wait_caption = set()

# ---------------- FORCE JOIN ----------------
async def check_join(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def force_join(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]
    ])

    await message.reply_text(
        "🚫 You must join our channel to use this bot!",
        reply_markup=buttons
    )

# ---------------- START ----------------
@bot.on_message(filters.command("start"))
async def start(client, message):

    if not await check_join(client, message.from_user.id):
        return await force_join(client, message)

    await message.reply_text(
        "👋 Hello!\n\n"
        "/setthumb - Set thumbnail\n"
        "/setcaption - Set caption\n\n"
        "📁 Send file → I will rename & send back"
    )

# ---------------- THUMB ----------------
@bot.on_message(filters.command("setthumb"))
async def thumb(client, message):

    if not await check_join(client, message.from_user.id):
        return await force_join(client, message)

    wait_thumb.add(message.from_user.id)
    await message.reply_text("📸 Send image for thumbnail")


@bot.on_message(filters.photo)
async def save_thumb(client, message):

    user = message.from_user.id

    if user in wait_thumb:
        file = await message.download()
        thumbs[user] = file
        wait_thumb.remove(user)
        await message.reply_text("✅ Thumbnail saved")

# ---------------- CAPTION ----------------
@bot.on_message(filters.command("setcaption"))
async def caption(client, message):

    if not await check_join(client, message.from_user.id):
        return await force_join(client, message)

    wait_caption.add(message.from_user.id)
    await message.reply_text("✍️ Send caption text")


@bot.on_message(filters.text & ~filters.command(["start","setthumb","setcaption"]))
async def save_caption(client, message):

    user = message.from_user.id

    if user in wait_caption:
        captions[user] = message.text
        wait_caption.remove(user)
