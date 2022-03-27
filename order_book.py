from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #Your code here

    #insert new order into database
    new_order = Order( sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], buy_currency=order['buy_currency'], sell_currency=order['sell_currency'], buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )
    session.add(new_order)
    session.commit()

    #check for a match

    #grab data from database
    orders = session.query(Order).all() #create a interable to look through orders

    for existing_order in orders:
        if ((existing_order.filled is None) and (existing_order.buy_currency == new_order.sell_currency) and (existing_order.sell_currency == new_order.buy_currency) and (existing_order.sell_amount / existing_order.buy_amount >= new_order.buy_amount/new_order.sell_amount)):
            new_order.filled = datetime.now()
            existing_order.filled = datetime.now()
            existing_order.counterparty_id = new_order.id
            new_order.counterparty_id = existing_order.id

            if existing_order.sell_amount < new_order.buy_amount:
                new_order = Order(sender_pk=new_order.sender_pk,receiver_pk=new_order.receiver_pk, buy_currency=new_order.buy_currency, sell_currency=new_order.sell_currency, buy_amount=new_order.buy_amount, sell_amount= new_order.sell_amount, creator_id = new_order.id)


    pass
