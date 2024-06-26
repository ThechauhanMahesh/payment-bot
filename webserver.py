import datetime 
import constants 
import paypalrestsdk
from aiohttp import web
from main import routes, bot, logger, db
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

uploader_bot_msg = """

"""


message_content = {
    "uploader" : """ 
@Terabox_downloader_1bot
@Terabox_Video_Down_Bot
@Terabox_Vid_down_robot

Subscription have been added!✅
""", 
    "save_restricted" : """
**USE ANY OF THESE BOTS**

DC 4 server based 🇩🇪

➤  @PremiumSRCB5_Bot 
➤  @PremiumSRCB4_Bot
➤  @PremiumSRCB3_Bot

DC 1 server based 🇺🇸

⚠️ Use DC 1 bots only if you get slow download speed (less than 1mb/s)

➤  @PremiumSRCB1_Bot
➤  @PremiumSRCB2_Bot 

**For updates related to paid bots join @Premium_SRCB ✅**
    """
}


def parse_log_message(date: datetime.date, user_id: int, amount: int, plan: str, duration: int, ends_on: datetime.date, mode: str):
    return f"`{user_id}` paid {amount} {'₹' if mode == 'upi' else '$'} on {date} for {plan}.\nExtended {duration} days and subscription ends on {ends_on}"


@routes.post("/crypto")
async def crypto_handler(request):
    args_data = request.rel_url.query

    data = await request.post()
    logger.debug(data, args_data)

    created_at = datetime.now(tz=UTC).date()
    plan = args_data.get('plan')
    amount = round(float(data.get("value")), 2)
    user_id = int(args_data.get('user_id'))
    duration = int(args_data.get('duration'))
    selected_bot = args_data.get('bot')
    ending_on = created_at + timedelta(days=duration)

    data_to_update = {"dos": str(created_at), "doe": str(ending_on), "plan":plan}

    if data.get('is_paid') == "1":
        logger.info(f"[Crypto] Payment of {amount}$ received from user {user_id} for {duration} days.")
        await db.update_user(user_id=user_id, data=data_to_update, bot=selected_bot)
        try: 
            await bot.send_message(constants.LOGS_CHAT_ID, parse_log_message(
                date=created_at, user_id=user_id, amount=amount, 
                plan=plan, duration=duration, ends_on=ending_on, 
                mode="crypto"
            ))
            await db.add_stats(amount, "crypto")
            await bot.send_message(user_id, f"Your payment of {amount}$ has been received, your subscription has been extended by {duration} days.")
            await bot.send_message(user_id, message_content[selected_bot])
        except: pass 

    return web.Response(status=200)

@routes.get("/paypal")
async def paypal_handler(request):
    logger.debug(request.rel_url.query)
    params = request.rel_url.query

    payer_id =  params['PayerID']
    payment_id = params['paymentId']

    payment = paypalrestsdk.Payment.find(payment_id)
    payment.execute({"payer_id": payer_id})

    created_at = datetime.now(tz=UTC).date()
    amount = payment['transactions'][0]['amount']['total']
    user_id, duration, plan, selected_bot = payment['transactions'][0]['custom'].split("|")

    ending_on = created_at + timedelta(days=int(duration))

    data_to_add = {"dos": str(created_at), "doe": str(ending_on), "plan": plan}
    await db.update_user(user_id=int(user_id), data=data_to_add, bot=selected_bot)
    await db.add_stats(amount, "paypal")

    logger.info(f"[PayPal] Payment of {amount}$ received from user {user_id} for {duration} days.")
    try:
        await bot.send_message(constants.LOGS_CHAT_ID, parse_log_message(
                date=created_at, user_id=user_id, amount=amount, 
                plan=plan, duration=duration, ends_on=ending_on, 
                mode="paypal"
            )) 
        await bot.send_message(int(user_id), f"Your payment of {amount}$ has been received, your subscription has been extended by {duration} days.")
        await bot.send_message(user_id, message_content[selected_bot])
    except: pass 
    return web.HTTPFound(f"https://t.me/{constants.BOT_USERNAME}")

@routes.post("/upi")
async def upi_handler(request):
    data = await request.post()
    logger.debug(data)

    created_at = datetime.now(tz=UTC).date()
    amount = int(data.get("amount"))
    user_id = int(data.get("udf1"))
    duration = int(data.get("udf2"))
    plan, selected_bot = data.get("udf3").split("|")

    ending_on = created_at + timedelta(days=duration)

    if data.get('status') == "success":
        data_to_add = {"dos": str(created_at), "doe": str(ending_on), "plan": plan}
        await db.update_user(user_id=user_id, data=data_to_add, bot=selected_bot)
        logger.info(f"[UPI] Payment of {amount}₹ received from user {user_id} for {duration} days.")
        await db.add_stats(amount, "upi")

        try:
            await bot.send_message(constants.LOGS_CHAT_ID, parse_log_message(
                    date=created_at, user_id=user_id, amount=amount, 
                    plan=plan, duration=duration, ends_on=ending_on, 
                    mode="upi"
                ))  
            await bot.send_message(user_id, f"Your payment of {amount}₹ has been received, your subscription has been extended by {duration} days.")
            await bot.send_message(user_id, message_content[selected_bot])
        except: pass 
    return web.Response(status=200)

@routes.get("/")
async def index(request):
    return web.Response(status=200)
