import logging 
import aiohttp 
import paypalrestsdk 



class PayPal:
    def __init__(self, client_id: str, client_secret: str, bot_username: str, mode: str = "live"):
        paypalrestsdk.configure({
            "mode": mode,
            "client_id": client_id,
            "client_secret": client_secret,
        })
        self.bot_username = bot_username
        logging.debug("PayPal client configured")

    def create_link(self, user_id: int, amount: int, duration: int) -> str:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": f"https://t.me/{self.bot_username}",
                "cancel_url": f"https://t.me/{self.bot_username}",
            },
            "transactions": [{
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "custom": f"{user_id}|{duration}",
                "soft_descriptor": "DroneBots",
            }]
        })

        if payment.create():
            logging.info(f"PayPal reposnse: {payment}")
            for req_link in payment.links:
                if req_link.method == "REDIRECT":
                    return req_link.href
        else:
            return None 
        

class BlockBee:
    def __init__(self, api_key: str, bot_username: str) -> None:
        self.api_key = api_key  
        self.bot_username = bot_username
        logging.debug("BlockBee client configured")

    async def create_link(self, user_id: int, amount: int, duration: int) -> str:
        async with aiohttp.ClientSession() as session:
            params = {
                "apikey": self.api_key,
                "redirect_url": f"https://t.me/{self.bot_username}",
                "value": amount,
                "currency": "USD",
                "item_description": "DroneBots subscription",
                "post": "0"
            }
            async with session.get("https://api.blockbee.io/checkout/request/", params=params) as response:
                data = await response.json()
                logging.info(f"BlockBee response: {data}")
                return data.get("payment_url", None)  
