from pyrogram import filters, Client 
from main import paypal_client, blockbee_client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@Client.on_callback_query(filters.regex(r"paypal\|(\d+)\|(\d+)"))
async def paypal_handler(_, cb: CallbackQuery):
    await cb.answer("Generating checkout link...", show_alert=True)
    amount = int(cb.matches[0].group(1))
    days = int(cb.matches[0].group(2))
    link = paypal_client.create_link(cb.from_user.id, amount, days)
    if not link:
        await cb.answer("Failed to generate PayPal link :(")
        return 
    await cb.edit_message_text(f"Pay {amount}$ ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Pay", url=link)]]))


@Client.on_callback_query(filters.regex(r"crypto\|(\d+)\|(\d+)"))
async def crypto_handler(_, cb: CallbackQuery):
    await cb.answer("Generating checkout link...", show_alert=True)
    amount = int(cb.matches[0].group(1))
    days = int(cb.matches[0].group(2))
    link = await blockbee_client.create_link(cb.from_user.id, amount, days)
    if not link:
        await cb.edit_message_text("Failed to generate crypto link :(")
        return
    await cb.edit_message_text(f"Pay {amount}$ ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Pay", url=link)]]))