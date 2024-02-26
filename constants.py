from decouple import config



# Basics
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

BOT_USERNAME = config("BOT_USERNAME", default=None)

# PayPal
PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID", default=None)
PAYPAL_CLIENT_SECRET = config("PAYPAL_CLIENT_SECRET", default=None)

# BlockBee
BLOCKBEE_API_KEY = config("BLOCKBEE_API_KEY", default=None)