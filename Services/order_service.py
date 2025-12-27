from uuid import uuid4
from Entities.pedidos import Order, OrderStatus
from Repository.pedido_repository import OrderRepository
from Configs.sqs_client import get_sqs_client, get_queue_url
import json

repo = OrderRepository()

def create_order(order_info):


    NewOrder = Order(
            id=str(uuid4()),
            cliente=order_info['cliente'],
            item=order_info['item'],
            status=OrderStatus.RECEBIDO.value
        )
    saved_order= repo.save_order(NewOrder)

    try:
        #creates the client and url
        sqs = get_sqs_client()
        queue_url = get_queue_url('fila-pedidos')

        #creates a dict msg
        msg_dict = NewOrder.to_dict()

        #transform dict to json so it can be sended
        msg_json = json.dumps(msg_dict)

        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=msg_json
        )
        print(f"Successfully sent order {saved_order.id}")
    except Exception as e:
        print(f"CRITICAL ERROR: failed to sent to SQS: {e}")

    return saved_order

def get_order(id):
    return repo.find_order_by_id(id).to_dict()

def get_all_orders():
    orders_list = repo.find_all_orders()
    return [order.to_dict() for order in orders_list]