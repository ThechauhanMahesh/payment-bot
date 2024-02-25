#ChauhanMahesh/Vasusen/COL/DroneBots
from main import bot 
from telethon import events, Button 
from telethon.tl.custom.message import Message

@bot.on(events.NewMessage(pattern="/start"))
async def start(event: Message):
    await event.reply(
        "Hello! I'm a bot!", 
        buttons=[
            [
                Button.inline("PayPal 5 $", data="paypal|5|5"), 
                Button.inline("Crypto 5 $", data="crypto|5|5")
            ], 
            [
                Button.inline("PayPal 10 $", data="paypal|10|15"), 
                Button.inline("Crypto 10 $", data="crypto|10|15")
            ], 
            [
                Button.inline("PayPal 20 $", data="paypal|20|30"), 
                Button.inline("Crypto 20 $", data="crypto|20|30")
            ], 
            [
                Button.inline("PayPal 40 $", data="paypal|40|90"), 
                Button.inline("Crypto 40 $", data="crypto|40|90")
            ], 
        ]
    )