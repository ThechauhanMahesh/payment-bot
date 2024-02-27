import asyncio 
import logging
from main import bot
from aiohttp import web
from pyrogram import idle
from webserver import routes 

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


print("Successfully deployed!")


async def start_bot():
    await bot.start()

async def setup_web_app():
    web_app = web.Application()
    web_app.add_routes(routes)
    
    server = web.AppRunner(web_app)
    await server.setup()

    site = web.TCPSite(server, '0.0.0.0', 8800)
    await site.start()

async def main():
    try:
        await start_bot()
        await setup_web_app()
        await idle()
    except Exception as e:
        raise e 

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())