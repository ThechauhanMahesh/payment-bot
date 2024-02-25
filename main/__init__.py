#ChauhanMahesh/Vasusen/DroneBots/COL

from telethon import TelegramClient
import logging
import constants 
from .utils import PayPal

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = TelegramClient(
    'bot', 
    constants.API_ID, 
    constants.API_HASH
)
bot.start(bot_token=constants.BOT_TOKEN) 

paypal_client = PayPal(
    client_id=constants.PAYPAL_CLIENT_ID,
    client_secret=constants.PAYPAL_CLIENT_SECRET,
    bot_username=constants.BOT_USERNAME,
    mode="sandbox"
)