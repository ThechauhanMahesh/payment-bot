import io 
import random 
import constants 
from main import db 
import pandas as np 
from datetime import datetime
from pyrogram.types import Message
from pyrogram import filters, Client, enums


@Client.on_message(filters.command(r"date") & filters.chat(constants.ADMINS))
async def show_date(_, message: Message):
    try:
        _, from_date, to_date = message.text.split(" ")
        from_date = datetime.strptime(from_date, "%d/%m/%Y")
        to_date = datetime.strptime(to_date, "%d/%m/%Y")
    except ValueError:
        return await message.reply("Invalid date format! Use `/date <from> <to>`", parse_mode=enums.ParseMode.MARKDOWN)
    
    transactions = await db.get_transactions(from_date, to_date)
    if not transactions: return await message.reply("No transactions found.")

    data = np.DataFrame(transactions)
    data.columns = ['Date', 'Crypto', 'PayPal', 'UPI', 'Total Amount']

    total_sum = data['Total Amount'].sum()

    with io.BytesIO() as output:
        data.to_csv(output, index=False)
        output.name = "transactions.csv"
        x = await message.reply_document(output, caption=f"Total amount: {'{:,}'.format(round(total_sum, 3))} ₹")
        await x.reply_animation(
            animation=random.choice([
                'https://i.pinimg.com/originals/c7/f4/08/c7f4085f145b758feac4e1d471b665a0.gif', 
                'https://images.moneycontrol.com/static-mcnews/2023/12/money-rich.gif?impolicy=website&width=1600&height=900', 
                'https://thereadingfangirl.files.wordpress.com/2014/03/perfect.gif', 
            ]), 
            quote=True
        )
