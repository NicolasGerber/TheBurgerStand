from uuid import uuid4
from Entities.pedidos import Pedido
from Repository.pedido_repository import salvar_pedido

def create_order(OrderInfo):

    novo_id = str(uuid4())
    NewOrder = Pedido(
            id=novo_id,
            cliente=OrderInfo['cliente'],
            item=OrderInfo['item'],
            status="Pendente"
        )

    return salvar_pedido(NewOrder)