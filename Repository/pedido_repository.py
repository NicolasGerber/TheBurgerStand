from Entities.pedidos import Order
from database import db


class OrderRepository:
    def save_order(self, NewOrder):
        try:
            db.session.add(NewOrder)
            db.session.commit()
            return NewOrder
        except Exception as e:
            db.session.rollback()
            print(f'Error: {e}')
            raise e  #o erro vai pro service/controler se virarem


    def find_order_by_id(self, id):
        try:
            return Order.query.get(id)
        except Exception as e:
            raise e

    def find_all_orders(self):
        try:
            return Order.query.all()
        except Exception as e:
            raise e