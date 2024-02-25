from aiohttp import web
from datetime import datetime 

routes = web.RouteTableDef()

@routes.post('/paypal')
async def get_handler(request):
    data = await request.json()
    if data['event_type'] == "PAYMENTS.PAYMENT.CREATED": 
        transaction_data = data['resource']['transactions'][0]

        created_at = datetime.utcnow()
        amount = transaction_data['amount']['total']
        user_id, duration = transaction_data['custom'].split("|")
    
        print(f"User {user_id} has paid for {duration} days ({amount}$)")
        # add data in database here 
        # user_id is user's id 
        # durtaion is the duration of the subscription
        # created_at is when the payment was confirmed
        return web.Response(text="*ok*")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=8080)