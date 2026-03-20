import os
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🔥 PUT YOUR GROUP USERNAME (NOT LINK)
CHANNEL = "knmovierequest"   # example: knmoviesgroup

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


# ✅ CHECK JOIN
async def check_join(client, message):
    user_id = message.from_user.id
    try:
        await client.get_chat_member(CHANNEL, user_id)
        return True
    except UserNotParticipant:
        await message.reply_text(
            "⚠️ Please join our group first!\n\n"
            f"👉 https://t.me/{CHANNEL}"
        )
        return False
    except Exception as e:
        print(e)
        return True  # avoid blocking if error


# START
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


# SET THUMB
@bot.on_message(filters.command("setthumb"))
async def thumb(client, message):

    if not await check_join(client, message):
        return

    wait_thumb.add(message.from_user.id)
    await message.reply_text("Send image for thumbnail")


@bot.on_message(filters.photo)
async def save_thumb(client, message):

    user = message.from_user.id

    if user in wait_thumb:
        file = await message.download()
        thumbs[user] = file
        wait_thumb.remove(user)
        await message.reply_text("Thumbnail saved ✅")


# SET CAPTION
@bot.on_message(filters.command("setcaption"))
async def caption(client, message):

    if not await check_join(client, message):
        return

    wait_caption.add(message.from_user.id)
    await message.reply_text("Send caption text")


@bot.on_message(filters.text & ~filters.command(["start","setthumb","setcaption"]))
async def save_caption(client, message):

    user = message.from_user.id

    if user in wait_caption:
        captions[user] = message.text
        wait_caption.remove(user)
        await message.reply_text("Caption saved ✅")


# PROCESS FILE
@bot.on_message(filters.document | filters.video)
async def process_file(client, message):

    if not await check_join(client, message):
        return

    user = message.from_user.id

    status = await message.reply_text("Downloading...")

    file_path = await message.download()

    await status.edit("Uploading...")

    await message.reply_document(
        file_path,
        caption=captions.get(user),
        thumb=thumbs.get(user),
        force_document=True
    )

    os.remove(file_path)

    await status.delete()


print("Bot Started Successfully")
bot.run()
