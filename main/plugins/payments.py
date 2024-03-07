import asyncio 
import constants
from typing import Union 
from pyrogram import filters, Client 
from main import paypal_client, blockbee_client, upi_client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message


@Client.on_callback_query(filters.regex(r"plans"))
@Client.on_message(filters.regex(r"^/pay$") & filters.private)
async def show_options(_, message: Union[Message, CallbackQuery]):
    if isinstance(message, Message): function = message.reply_text
    else: function = message.edit_message_text

    await function(
        "Select a plan.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("BASIC 🥉 ", "plan|basic"), 
                    InlineKeyboardButton("BASIC X 3 🥉", "plan|basicx3")                    
                ], 
                [InlineKeyboardButton("MONTHLY 🥈", "plan|monthly")],
                [InlineKeyboardButton("PRO 🥇", "plan|pro")]
            ]
        )
    )

@Client.on_callback_query(filters.regex(r"plan\|(.+)"))
async def show_plans(_, cb: CallbackQuery):
    plan = cb.matches[0].group(1)
    try: 
        plan_data = constants.plans[plan]
        await cb.edit_message_text(f"{plan_data.get('title')}\n\n{plan_data.get('description')}\n\nChoose payment mode : ", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"🇮🇳 UPI {plan_data.get('price', {}).get('upi', {}).get('amount')} ₹", f"payments|upi|{plan}"),
                    InlineKeyboardButton(f"💳 PayPal {plan_data.get('price', {}).get('paypal', {}).get('amount')} $", f"payments|paypal|{plan}"),
                ],[
                    InlineKeyboardButton(f"🪙 Crypto {plan_data.get('price', {}).get('crypto', {}).get('amount')} $", f"payments|crypto|{plan}"),
                    InlineKeyboardButton("👤 Other", url=constants.CONTACT_USERNAME)
                ], 
                [InlineKeyboardButton("Back", "plans")]
            ]
        ))
    except KeyError:
        await cb.answer("Plan not available!", show_alert=True)
        return
    

@Client.on_callback_query(filters.regex(r"payments\|(.+)\|(.+)"))
async def handle_payment_cb(_, cb: CallbackQuery):
    payment_mode = cb.matches[0].group(1)
    plan = cb.matches[0].group(2)

    try:
        plan_data = constants.plans[plan]
        payment_data = plan_data["price"][payment_mode]
    except KeyError:
        await cb.answer("Plan not available!", show_alert=True)
        return
    
    if payment_mode == "upi":
        client = upi_client
    elif payment_mode == "paypal":
        client = paypal_client
    elif payment_mode == "crypto":
        client = blockbee_client
    else:
        await cb.answer("Invalid payment mode!", show_alert=True)
        return
    
    link = await client.create_link(user_id=cb.from_user.id, amount=payment_data.get("amount"), duration=plan_data.get("duration"), plan=plan)
    if not link:
        await cb.answer("Failed to generate checkout link :(", show_alert=True)
        return
    
    message = await cb.edit_message_text(f"Pay {payment_data.get('amount')} {payment_data.get('symbol')} for {plan_data.get('title')} plan.", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Pay {payment_data.get('amount')} {payment_data.get('symbol')}", url=link),
                InlineKeyboardButton("Cancel", "plans")
            ]
        ]
    ))
    await asyncio.sleep(5 * 60) # 5 mins sleep 
    try: 
        await message.delete()
    except: pass 
