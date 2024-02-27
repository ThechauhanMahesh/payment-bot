
import datetime 
import constants 
import paypalrestsdk
from aiohttp import web
from datetime import datetime 
from main import routes, bot, logger 


@routes.post("/crypto/{user_id}/{duration}")
async def crypto_handler(request):
    data = await request.post()
    logger.debug(data)

    created_at = datetime.utcnow()
    amount = round(float(data.get("value")), 2)
    user_id = int(request.match_info['user_id'])
    duration = int(request.match_info['duration'])

    if data.get('is_paid') == "1":
        logger.info(f"[Crypto] Payment of {amount}$ received from user {user_id} for {duration} days.")
        await bot.send_message(user_id, f"Your payment of {amount}$ has been received, your subscription has been extended by {duration} days.")
        #! handle database thing here

    return web.Response(status=200)

@routes.get("/paypal")
async def index(request):
    logger.debug(request.rel_url.query)
    params = request.rel_url.query

    payer_id =  params['PayerID']
    payment_id = params['paymentId']

    payment = paypalrestsdk.Payment.find(payment_id)
    payment.execute({"payer_id": payer_id})

    created_at = datetime.utcnow()
    amount = payment['transactions'][0]['amount']['total']
    user_id, duration = payment['transactions'][0]['custom'].split("|")

    #! handle database thing here
    logger.info(f"[PayPal] Payment of {amount}$ received from user {user_id} for {duration} days.")
    await bot.send_message(int(user_id), f"Your payment of {amount}$ has been received, your subscription has been extended by {duration} days.")
    return web.HTTPFound(f"https://t.me/{constants.BOT_USERNAME}")