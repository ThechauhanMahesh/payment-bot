import sys
import logging
import constants 
import importlib
import paypalrestsdk 
from pathlib import Path

def load_plugins(plugin_name):
    path = Path(f"main/plugins/{plugin_name}.py")
    name = "main.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["main.plugins." + plugin_name] = load
    print("main has Imported " + plugin_name)


class PayPal:
    def __init__(self, client_id: str, client_secret: str, bot_username: str, mode: str = "live"):
        paypalrestsdk.configure({
            "mode": mode,
            "client_id": client_id,
            "client_secret": client_secret,
        })

        self.bot_username = bot_username

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
            for req_link in payment.links:
                if req_link.method == "REDIRECT":
                    return req_link.href
        else:
            return None 