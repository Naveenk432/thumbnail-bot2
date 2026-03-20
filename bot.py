import os
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ✅ YOUR GROUP USERNAME
CHANNEL = "knmoviesrequest"

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


# ✅ FORCE JOIN CHECK
async def check_join(client, message):
    user_id = message.from_user.id
    try:
        await client.get_chat_member(CHANNEL, user_id)
        return True
    except UserNotParticipant:
        await message.reply_text(
            f"⚠️ Please join our group first!\n\n👉 https://t.me/{CHANNEL}"
        )
        return False
    except Exception as e:
        print(e)
        return True


# START
@bot.on_message(filters.command("start"))
async def start(client, message):
    if not await check_join(client, message):
        return

    await message.reply_text("👋 Bot is working!")


# TEXT (HI, HELLO etc)
@bot.on_message(filters.text & ~filters.command(["start","setthumb","setcaption"]))
async def text_handler(client, message):
    if not await check_join(client, message):
        return

    await message.reply_text("Send file or use commands 👍")


# FILE
@bot.on_message(filters.document | filters.video)
async def process_file(client, message):
    if not await check_join(client, message):
        return

    await message.reply_text("File received ✅")


print("Bot Started Successfully")
bot.run()
