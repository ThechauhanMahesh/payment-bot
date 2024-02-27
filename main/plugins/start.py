#ChauhanMahesh/Vasusen/COL/DroneBots

from pyrogram import filters, Client 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(filters.regex(r"^/start$") & filters.private)
async def start_handler(_, message: Message):
    await message.reply_text(
        "Hello! I'm a bot!", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("UPI 5 ₹", callback_data="upi|5|5"),
                    InlineKeyboardButton("PayPal 5 $", callback_data="paypal|5|5"), 
                    InlineKeyboardButton("Crypto 5 $", callback_data="crypto|5|5"), 
                ], 
                [
                    InlineKeyboardButton("UPI 10 ₹", callback_data="upi|10|15"),
                    InlineKeyboardButton("PayPal 10 $", callback_data="paypal|10|15"), 
                    InlineKeyboardButton("Crypto 10 $", callback_data="crypto|10|15"), 
                ], 
                [
                    InlineKeyboardButton("UPI 20 ₹", callback_data="upi|20|30"),
                    InlineKeyboardButton("PayPal 20 $", callback_data="paypal|20|30"), 
                    InlineKeyboardButton("Crypto 20 $", callback_data="crypto|20|30"), 
                ], 
                [
                    InlineKeyboardButton("UPI 40 ₹", callback_data="upi|40|90"),
                    InlineKeyboardButton("PayPal 40 $", callback_data="paypal|40|90"), 
                    InlineKeyboardButton("Crypto 40 $", callback_data="crypto|40|90"), 
                ], 
            ]
        )
    )