#ChauhanMahesh/Vasusen/COL/DroneBots
import constants 
from pyrogram import filters, Client 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(filters.regex(r"^/start$") & filters.private)
async def start_handler(_, message: Message):
    await message.reply_text(
        "TEXT",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Terms & Conditions", url=constants.TAC_URL)
            ]]
        )
    )

@Client.on_message(filters.regex(r"^/help$") & filters.private)
async def help_handler(_, message: Message):
    await message.reply_text(
        "TEXT",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Contact", url=constants.CONTACT_USERNAME)
            ]]
        )
    )