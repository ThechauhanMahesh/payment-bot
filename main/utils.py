import logging 
import aiohttp 
import paypalrestsdk 



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


    def create_link(self, user_id: int, amount: int, duration: int) -> str:
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
                "custom": f"{user_id}|{duration}",
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
        logging.debug("BlockBee client configured")

    async def create_link(self, user_id: int, amount: int, duration: int) -> str:
        async with aiohttp.ClientSession() as session:
            params = {
                "apikey": self.api_key,
                "redirect_url": f"https://t.me/{self.bot_username}",
                "value": amount,
                "currency": "USD",
                "item_description": "DroneBots subscription",
                "post": "1", 
                "notify_url": f"{self.webhook_url}/crypto/{user_id}/{duration}"
            }
            async with session.get("https://api.blockbee.io/checkout/request/", params=params) as response:
                data = await response.json()
                logging.info(f"BlockBee response: {data}")
                return data.get("payment_url", None)  
