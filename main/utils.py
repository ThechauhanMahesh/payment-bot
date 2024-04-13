import logging 
import aiohttp 
import constants 
import urllib.parse
import paypalrestsdk 
from uuid import uuid4
from datetime import datetime, UTC
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self, uri: str, db_data: dict) -> None:
        self.db_dict = db_data
        self._client = AsyncIOMotorClient(uri)
        self.stats = self._client.stats.stats
        logging.debug("Database client configured")

    async def update_user(self, user_id: int, data: dict, bot: str) -> None:
        data = self.db_dict[bot]
        db = self._client[data["db"]][data["collection"]]
        return await db.update_one(
            {"id": user_id},
            {
                "$set": {"data":data}, 
                "$setOnInsert": data.get('defaults')
            },
            upsert=True
        )
    
    def deduct_fees(self, input_amount, values):
        closest_key = max((key for key in values if key <= input_amount), default=None)
        if closest_key :
            return values[closest_key]
        return 0 

    async def add_stats(self, amount: int, payment_mode: str):
        if payment_mode in ['paypal', 'crypto']:
            amount = self.deduct_fees(amount, constants.FEES[payment_mode])

        return  await self.stats.update_one(
            {"date": str(datetime.now(tz=UTC).date())},
            {"$inc": {payment_mode: amount}},
            upsert=True
        )

    async def get_transactions(self, from_date, to_date):
        pipeline = [
            {'$match': { 'date': {'$gte': str(from_date), '$lte': str(to_date)}}},
            {'$set': {
                'crypto': {'$multiply': ['$crypto', constants.DOLLAR_RATE]},
                'paypal': {'$multiply': ['$paypal', constants.DOLLAR_RATE]}
            }},
            {'$set': {'total': {'$add': ['$crypto', '$paypal', '$upi']}}},
            {'$project': {'_id': 0}},
            {'$sort': {'date': 1}}
        ]

        cursor = self.stats.aggregate(pipeline)
        return await cursor.to_list(None)
    

class PayPal:
    def __init__(self, client_id: str, client_secret: str, bot_username: str, server_url: str, mode: str = "live"):
        self.app = paypalrestsdk.configure({
            "mode": mode,
            "client_id": client_id,
            "client_secret": client_secret,
        })
        self.server_url = server_url
        self.bot_username = bot_username
        logging.debug("PayPal client configured")


    async def create_link(self, user_id: int, amount: int, duration: int, plan: str, bot: str) -> str:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": f"{self.server_url}/paypal",
                "cancel_url": f"https://t.me/{self.bot_username}",
            },
            "transactions": [{
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "DroneBots subscription",
                "custom": f"{user_id}|{duration}|{plan}|{bot}",
            }], 
            "note_to_payer": "Contact us for any questions on your order.", 
            "application_context": {
                "brand_name": "DroneBots",
                "locale": "en-US",
                "user_action": "commit",
            }
        })

        if payment.create():
            logging.info(f"PayPal reposnse: {payment}")
            for req_link in payment.links:
                if req_link.method == "REDIRECT":
                    return req_link.href
        else:
            return None 
        

class BlockBee:
    def __init__(self, api_key: str, bot_username: str, webhook_url: str) -> None:
        self.api_key = api_key  
        self.webhook_url = webhook_url
        self.bot_username = bot_username
        self._url = "https://api.blockbee.io/checkout/request/"
        logging.debug("BlockBee client configured")

    async def create_link(self, user_id: int, amount: int, duration: int, plan: str, bot: str) -> str:
        async with aiohttp.ClientSession() as session:
            arguments = {"user_id": user_id, "duration": duration, "plan": plan, "bot": bot}
            
            params = {
                "apikey": self.api_key,
                "redirect_url": f"https://t.me/{self.bot_username}",
                "value": amount,
                "currency": "USD",
                "item_description": "DroneBots subscription",
                "notify_url": f"{self.webhook_url}/crypto?" + urllib.parse.urlencode(arguments), 
                "post": "1"
            }
            async with session.get(self._url, params=params) as response:
                data = await response.json()
                logging.info(f"BlockBee response: {data}")
                return data.get("payment_url", None)  
            

class UPI:
    def __init__(self, api_key: str, bot_username: str):
        self.api_key = api_key
        self.bot_username = bot_username
        self._url = "https://api.ekqr.in/api/create_order"
        logging.debug("UPI client configured")

    async def create_link(self, user_id: int, amount: int, duration: int, plan: str, bot: str) -> str:
        txnid = str(uuid4())
        headers = {'Content-Type': 'application/json'}
        amount = str(amount)
        user_id = str(user_id)
        duration = str(duration)
        json_data = dict(
            key=self.api_key,
            client_txn_id=txnid,
            amount=amount,
            p_info="DroneBots subscription",
            customer_name=str(user_id),
            customer_email=f"user{user_id}@dronebots.in", 
            customer_mobile="9999999999",
            redirect_url=f"https://t.me/{self.bot_username}",
            udf1=user_id,
            udf2=duration,
            udf3=f"{plan}|{bot}",
        )
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(self._url, json=json_data) as response:
                data = await response.json()
                logging.info(f"UPI response: {data}")
                if not data.get("status"):
                    return None
                return data.get("data", {}).get("payment_url", None)
