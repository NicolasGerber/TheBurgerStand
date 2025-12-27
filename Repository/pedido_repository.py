from Entities.pedidos import Pedido
from database import db


class PedidoRepository:
    def salvar_pedido(self, NewOrder):
        try:
            db.session.add(NewOrder)
            db.session.commit()
            return NewOrder
        except Exception as e:
            db.session.rollback()
            print(f'erro ao salvar pedido {e}')
            raise e  #o erro vai pro service/controler se virarem


    def find_order_by_id(self, id):
        try:
            return Pedido.query.get(id)
        except Exception as e:
            raise e

    def find_all_orders(self):
        try:
            return Pedido.query.all()
        except Exception as e:
            raise e