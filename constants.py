from decouple import config

START_TEXT = """
If you want to make a payment for subscription,
Send /pay to @SubscriptionForBot ✅

यदि आप subscription के लिए भुगतान करना चाहते हैं,
@SubscriptionForBot ✅ पर /pay भेजें

Read our T&C before any purchase"""


FEES = {
    "crypto":{
        8: 7.79,
        6: 5.84,
        4: 3.83,
        2: 1.85
    }, 
    "paypal": {
        8: 7.23,
        6: 5.34,
        4: 3.43,
        2: 1.54
    }
}

plans = {
    "save_restricted":{
        "basic": {
            "title": "Basic Plan", 
            "description": "✅ Invite link not needed\n✅ High speed upload\n✅ Unlimited links both public and private\n✅ forwards from bots too\n✅ Public and private chats supported\n✅ Timer of only 10 seconds\n✅ Save content directly into your channel/group",
            "price":{
                "upi" : {
                    "amount": 100, 
                    "symbol": "₹"
                }, 
                "crypto":{
                    "amount": 0.2, 
                    "symbol": "$"
                }, 
                "paypal":{
                    "amount": 2, 
                    "symbol": "$"
                }
            }, 
            "duration": 10,
        }, 
        "basicx3":{
            "title": "Basic x3 Plan", 
            "description": "✅ all features of basic plan for a month",
            "price":{
                "upi" : {
                    "amount": 200, 
                    "symbol": "₹"
                }, 
                "crypto":{
                    "amount": 4, 
                    "symbol": "$"
                }, 
                "paypal":{
                    "amount": 4, 
                    "symbol": "$"
                }
            }, 
            "duration": 30,
        },
        "monthly": {
            "title": "Monthly Plan", 
            "description": "✅ All features of basic plan\n✅ /batch (auto save) upto 30 messages",
            "price":{
                "upi" : {
                    "amount": 300, 
                    "symbol": "₹"
                }, 
                "crypto":{
                    "amount": 6, 
                    "symbol": "$"
                }, 
                "paypal":{
                    "amount": 6, 
                    "symbol": "$"
                }
            }, 
            "duration": 30,
        },
        "pro": {
            "title": "Pro Plan", 
            "description": "✅ All features of basic plan\n✅ /batch (auto save) upto 100 messages\n✅ Supports file size upto 4gb\n✅ Timer of 2 seconds only\n✅ Add/delete/replace text in captions",
            "price":{
                "upi" : {
                    "amount": 450, 
                    "symbol": "₹"
                }, 
                "crypto":{
                    "amount": 8, 
                    "symbol": "$"
                }, 
                "paypal":{
                    "amount": 8, 
                    "symbol": "$"
                }
            }, 
            "duration": 30,
        }
    }, 
    "uploader":{
        "premuim":{
            "title": "Premium Plan", 
            "description": "PREMIUM PLAN ⚡️\n\n- Unlimited links 🔗\n- No waiting period 🕐\n- High speed upload 🚀\n- Validity of 30 days 🎁",
            "price":{
                "upi" : {
                    "amount": 125, 
                    "symbol": "₹"
                }, 
                "crypto":{
                    "amount": 3, 
                    "symbol": "$"
                }, 
                "paypal":{
                    "amount": 3, 
                    "symbol": "$"
                }
            }, 
            "duration": 30,
        
        }
    }
}

ADMINS = [1807573686]

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
SERVER_URL = config("SERVER_URL", default=None)

# UPI
UPI_API_KEY = config("UPI_API_KEY", default=None)

DATABASE_DICT = {
    "uploader": {
        "db":"UPL", 
        "collection":"UPL", 
        "defaults" : {}
    },
    "save_restricted": {
        "db":"PremiumSRCB", 
        "collection":"users", 
        "defaults": dict(
            banned=False, 
            api_id=None, 
            api_hash=None, 
            session=None, 
            chat=None, 
            process={"process":False, "batch":False}, 
            caption={"action":None, "string":None}
        )
    }
}
MONGODB_URL = config("MONGODB_URL", default=None)

# MISC 
TAC_URL = "https://github.com/vasusen-code/Terms-Conditions/blob/main/README.md"
CONTACT_USERNAME = "https://t.me/ChauhanMahesh_Bot"

LOGS_CHAT_ID = config("LOGS_CHAT_ID", default=None)

DOLLAR_RATE = 83