import os
import asyncio
from pyrogram import Client, filters
from aiohttp import web

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= BOT =================

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Bot is working!")

# ================= FAKE SERVER =================

async def handle(request):
    return web.Response(text="Bot is alive")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle)

    port = int(os.getenv("PORT", 8080))  # Railway needs this
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ================= MAIN =================

async def main():
    await bot.start()
    print("🤖 Bot Running")

    await start_webserver()   # 👈 IMPORTANT

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
