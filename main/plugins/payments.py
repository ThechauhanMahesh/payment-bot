from main import bot, paypal_client
from telethon import events, Button 
from telethon.events.callbackquery import CallbackQuery


@bot.on(events.CallbackQuery(pattern=r"paypal\|(\d+)\|(\d+)"))
async def crypto(event: CallbackQuery.Event):
    amount = int(event.pattern_match.group(1))
    days = int(event.pattern_match.group(2))
    await event.edit("Generating PayPal link...", buttons=None)
    link = paypal_client.create_link(event.sender_id, amount, days)
    if not link:
        await event.edit("Failed to generate PayPal link :(")
        return 
    await event.edit(f"Pay {amount}$ ", buttons=Button.url("Pay", link))