#ChauhanMahesh/Vasusen/DroneBots/COL

import logging
import constants 
from aiohttp import web
from pyrogram import Client 
from .utils import PayPal, BlockBee

routes = web.RouteTableDef()

logging.basicConfig(
    format = "[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("bot.log", "w"), logging.StreamHandler()],
    level=logging.INFO
)

bot = Client(
    name='bot', 
    api_id=constants.API_ID, 
    api_hash=constants.API_HASH,
    bot_token=constants.BOT_TOKEN, 
    plugins=dict(root="main/plugins")
)

paypal_client = PayPal(
    client_id=constants.PAYPAL_CLIENT_ID,
    client_secret=constants.PAYPAL_CLIENT_SECRET,
    bot_username=constants.BOT_USERNAME,
    mode="live"
)
blockbee_client = BlockBee(
    webhook_url=constants.WEBHOOK_URL,
    api_key=constants.BLOCKBEE_API_KEY, 
    bot_username=constants.BOT_USERNAME, 
)