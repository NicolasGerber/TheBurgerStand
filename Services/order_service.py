from uuid import uuid4
from Entities.pedidos import Pedido, OrderStatus
from Repository.pedido_repository import PedidoRepository

repo = PedidoRepository()

def create_order(order_info):
    NewOrder = Pedido(
            id=str(uuid4()),
            cliente=order_info['cliente'],
            item=order_info['item'],
            status=OrderStatus.RECEBIDO
        )
    pedido_salvo = repo.salvar_pedido(NewOrder)
    return pedido_salvo

def get_order(id):
    return repo.find_order_by_id(id).to_dict()

def get_all_orders():
    orders_list = repo.find_all_orders()
    return [order.to_dict() for order in orders_list]