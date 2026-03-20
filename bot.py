import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🔥 PUT YOUR GROUP ID HERE
GROUP_ID = -1001234567890   # 👈 REPLACE THIS

# 🔗 PUT YOUR GROUP INVITE LINK
GROUP_LINK = "https://t.me/knmoviesrequest"

bot = Client(
    "thumbnail-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

thumbs = {}
captions = {}
wait_thumb = set()
wait_caption = set()


# ✅ FORCE JOIN CHECK (SAFE)
async def check_join(client, message):
    try:
        user_id = message.from_user.id
        member = await client.get_chat_member(GROUP_ID, user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True

    except Exception:
        pass

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔗 Join Group", url=GROUP_LINK)],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
        ]
    )

    await message.reply_text(
        "⚠️ Please join our group to use this bot!",
        reply_markup=buttons
    )
    return False


# 🔁 RECHECK BUTTON
@bot.on_callback_query(filters.regex("check_join"))
async def recheck(client, callback_query):
    if await check_join(client, callback_query.message):
        await callback_query.message.edit("✅ Now you can use the bot!")
    else:
        await callback_query.answer("❌ Join first!", show_alert=True)


# 🚀 START
@bot.on_message(filters.command("start"))
async def start(client, message):
    if not await check_join(client, message):
        return

    await message.reply_text(
        "Hello 👋\n\n"
        "/setthumb - Set thumbnail\n"
        "/setcaption - Set caption\n\n"
        "After setting send any file."
    )


# 🖼 SET THUMBNAIL
@bot.on_message(filters.command("setthumb"))
async def thumb(client, message):
    if not await check_join(client, message):
        return

    wait_thumb.add(message.from_user.id)
    await message.reply_text("📸 Send image for thumbnail")


@bot.on_message(filters.photo)
async def save_thumb(client, message):
    if not await check_join(client, message):
        return

    user = message.from_user.id

    if user in wait_thumb:
        file = await message.download()
        thumbs[user] = file
        wait_thumb.remove(user)

        await message.reply_text("✅ Thumbnail saved")


# ✏️ SET CAPTION
@bot.on_message(filters.command("setcaption"))
async def caption(client, message):
    if not await check_join(client, message):
        return

    wait_caption.add(message.from_user.id)
    await message.reply_text("📝 Send caption text")


@bot.on_message(filters.text)
async def save_caption(client, message):
    if not await check_join(client, message):
        return

    user = message.from_user.id

    if user in wait_caption:
        captions[user] = message.text
        wait_caption.remove(user)

        await message.reply_text("✅ Caption saved")


# 📂 PROCESS FILE
@bot.on_message(filters.document | filters.video)
async def process_file(client, message):
    if not await check_join(client, message):
        return

    user = message.from_user.id

    status = await message.reply_text("⬇️ Downloading...")

    file_path = await message.download()

    await status.edit("⬆️ Uploading...")

    await message.reply_document(
        file_path,
        caption=captions.get(user),
        thumb=thumbs.get(user),
        force_document=True
    )

    os.remove(file_path)

    await status.delete()
    if not await check_join(client, message):
    return
    @bot.on_message()
    async def get_group_id(client, message):
        print("GROUP ID:", message.chat.id)

# 🚀 START BOT
print("🚀 Bot Started Successfully")
bot.run()
