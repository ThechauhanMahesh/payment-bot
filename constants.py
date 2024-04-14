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
            "title": "BASIC 🥉", 
            "description": "✅ Invite link not needed\n✅ High speed upload\n✅ Unlimited links both public and private\n✅ forwards from bots too\n✅ Public and private chats supported\n✅ Timer of only 10 seconds\n✅ Save content directly into your channel/group\n\n 10 days validity.",
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
            "title": "BASIC X 3 🥉", 
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
            "title": "MONTHLY 🥈", 
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
            "title": "PRO 🥇", 
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
        "premium":{
            "title": "PREMIUM ⚡️", 
            "description": "✅Unlimited links \n✅No waiting period\n✅High speed upload\n✅Validity of 30 days",
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
API_ID = "4796990"
API_HASH = "32b6f41a4bf740efed2d4ce911f145c7"
BOT_TOKEN = "6306813630:AAEdMg_Zwsv6mgpDwGF38p__vrY62ldxn3w"

BOT_USERNAME = "subscriptionforbot"

# PayPal
PAYPAL_CLIENT_ID = "Aev6mZhtRujS8zk67Uds5D56a-WQ1Xm6Hu3zVEkNYwIHYUMx0e1shwaRc2uOIJgjCTQNO-fRWGOcyyjG"
PAYPAL_CLIENT_SECRET = "EKsXruoKqCCsh42vDv9nIXkeGG0RQfGa_HXHYHXb_b3uoktjkA-726htkGxhCaSGgJeXS_eS96p4YE9K"

# BlockBee
BLOCKBEE_API_KEY = "4yaKo6nFrQzaB8rQGkA54DJUYESrdVXi8rtq1XgauHAjCIAs9MYdZQh3X2J38wpq"
SERVER_URL = "https://payments.dronebots.in"

# UPI
UPI_API_KEY = "084c4db3-05da-4438-b689-06459a349c66"

# Database
MONGODB_URL = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"

DATABASE_DICT = {
    "uploader": {
        "db":"UPL", 
        "collection":"UPL", 
        "defaults" : dict(
            token=None,
            chat=None,
            batch=False, 
        )
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

# MISC 
TAC_URL = "https://github.com/vasusen-code/Terms-Conditions/blob/main/README.md"
CONTACT_USERNAME = "https://t.me/MaheshChauhanBot"
LOGS_CHAT_ID = 1807573686
