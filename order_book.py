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
    orders = session.query(Order).filter(Order.filled == None).all() #create a interable to look through orders

    for existing_order in orders:
        if ((existing_order.buy_currency == new_order.sell_currency) and (existing_order.sell_currency == new_order.buy_currency) and (existing_order.sell_amount / existing_order.buy_amount >= new_order.buy_amount/new_order.sell_amount)):
            # set filled to current time stamp
            new_order.filled = datetime.now()
            existing_order.filled = datetime.now()
            # setting counterparty id to each other
            existing_order.counterparty_id = new_order.id
            new_order.counterparty_id = existing_order.id

            # order buy sell relationship
            ratio = new_order.buy_amount/new_order.sell_amount

            if (new_order.sell_amount < existing_order.buy_amount):
                # create child order
                new_order = Order(sender_pk=new_order.sender_pk,receiver_pk=new_order.receiver_pk, buy_currency=new_order.buy_currency, 
                sell_currency=new_order.sell_currency, buy_amount=existing_order.buy_amount - new_order.sell_amount, sell_amount= ratio* (existing_order.buy_amount - new_order.sell_amount), creator_id = new_order.id)
                
                # add child order to session
                #session.add(new_order)
                #session.commit()
            elif (new_order.buy_amount > existing_order.sell_amount):
                # create child order
                new_order = Order(sender_pk=new_order.sender_pk,receiver_pk=new_order.receiver_pk, buy_currency=new_order.buy_currency, 
                sell_currency=new_order.sell_currency, buy_amount=new_order.buy_amount - existing_order.sell_amount, sell_amount= ratio*(new_order.buy_amount - existing_order.sell_amount), creator_id = new_order.id)

                # add child order to session
                #session.add(new_order)
                #session.commit()
    pass
