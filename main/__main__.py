import asyncio 
import logging
from . import bot
from aiohttp import web
from pyrogram import idle
from webserver import routes 

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


print("Successfully deployed!")


async def setup():
    await bot.start()
    web_app = web.Application()
    web_app.add_routes(routes)
    server = web.AppRunner(web_app)
    await server.setup()
    await web.TCPSite(server, '0.0.0.0', 8800).start()
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())

