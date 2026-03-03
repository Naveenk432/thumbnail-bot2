from pyrogram import Client, filters

api_id = 22580782
api_hash = "946a0cc78ab034f489ebd3584f7b3152"
bot_token = "8306956637:AAFvt2fEhH057P1dyh3jlG6J712WE7vlJ14"

app = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    print("Message received!")   # <-- IMPORTANT
    await message.reply_text("Bot working 🔥")

print("Bot running...")

app.run()
