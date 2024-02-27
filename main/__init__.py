#ChauhanMahesh/Vasusen/DroneBots/COL

import logging
import constants 
from aiohttp import web
from pyrogram import Client 
from .utils import PayPal, BlockBee, UPI, Database

routes = web.RouteTableDef()

logging.basicConfig(
    format = "[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("bot.log", "w"), logging.StreamHandler()],
    level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = Client(
    name='bot', 
    api_id=constants.API_ID, 
    api_hash=constants.API_HASH,
    bot_token=constants.BOT_TOKEN, 
    plugins=dict(root="main/plugins")
)
db = Database(
    uri=constants.MONGODB_URL,
    database_name=constants.DATABASE_NAME
)
paypal_client = PayPal(
    mode="live", 
    server_url=constants.SERVER_URL,
    bot_username=constants.BOT_USERNAME,
    client_id=constants.PAYPAL_CLIENT_ID,
    client_secret=constants.PAYPAL_CLIENT_SECRET,
)
blockbee_client = BlockBee(
    webhook_url=constants.SERVER_URL,
    api_key=constants.BLOCKBEE_API_KEY, 
    bot_username=constants.BOT_USERNAME, 
)

upi_client = UPI(
    api_key=constants.UPI_API_KEY,
    bot_username=constants.BOT_USERNAME,
)