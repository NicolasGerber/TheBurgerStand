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


    def find_order_by_id(self, order_id):
        try:
            return Order.query.get(order_id)
        except Exception as e:
            raise e

    def find_all_orders(self):
        try:
            return Order.query.all()
        except Exception as e:
            raise e

    def update_order(self, order_id, new_status_string):
        try:
            order = Order.query.get(order_id)

            if order:
                order.status = new_status_string
                db.session.commit()

                return order
            return None
        except Exception as e:
            db.session.rollback()
            raise e

    def get_orders_locked_repo(self, status_list): #Find the status in the list
        return Order.query.filter(Order.status.in_(status_list)).all()