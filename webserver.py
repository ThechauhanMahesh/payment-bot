import json
from aiohttp import web
from main import routes, bot 
from datetime import datetime 


@routes.post('/paypal')
async def get_handler(request):
    data = await request.json()
    if data['event_type'] == "PAYMENTS.PAYMENT.CREATED": 
        transaction_data = data['resource']['transactions'][0]

        created_at = datetime.utcnow()
        amount = transaction_data['amount']['total']
        user_id, duration = transaction_data['custom'].split("|")
    
        print(f"User {user_id} has paid for {duration} days ({amount}$)")
        await bot.send_message(int(user_id), f"Your payment of {amount}$ has been received, your subscription has been extended by {duration} days.")
        #! handle database thing here 
        return web.Response(text="*ok*")


@routes.post("/crypto/{user_id}/{duration}")
async def crypto_handler(request):
    data = await request.post()

    amount = round(float(data.get("value")), 2)
    user_id = int(request.match_info['user_id'])
    duration = int(request.match_info['duration'])

    if data.get('is_paid') == "1":
        print(f"User {user_id} has paid for {duration} days ({amount}$)")
        await bot.send_message(user_id, f"Your payment of {amount}$ has been received, your subscription has been extended by {duration} days.")
        #! handle database thing here
        
    return web.Response(status=200)