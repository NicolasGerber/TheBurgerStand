from uuid import uuid4
from Entities.pedidos import Order, OrderStatus
from Repository.pedido_repository import OrderRepository
from Configs.sqs_client import get_sqs_client, get_queue_url
import json
import time

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

def get_order(order_id):
    return repo.find_order_by_id(order_id).to_dict()

def get_all_orders():
    orders_list = repo.find_all_orders()
    return [order.to_dict() for order in orders_list]

def update_order_status(order_id):
    new_status = OrderStatus.PREPARACAO.value
    print(f"Updating status to {new_status}")
    time.sleep(4)  # This simulate the time to process
    repo.update_order(order_id, new_status)
    print(f"Successfully updated status to {new_status}")
    return new_status

def process_order(order_id):  #THis func encapsulate the "kitchen" logic
    print("......[SERVICE].......")
    print(f"PROCESSING ORDER {order_id}")
    new_status = OrderStatus.PRONTO.value
    time.sleep(4)
    repo.update_order(order_id, new_status)
    print(f"Order {order_id} READY!")
    return new_status

def get_locked_orders():
    target_status = [
        OrderStatus.RECEBIDO.value,
        OrderStatus.PREPARACAO.value,
        'Pendente',
        'Pendende_Pagamento'
    ]
    print("......[SERVICE].......")
    print("LOOKING FOR LOST ORDERS")
    orders_list = repo.get_orders_locked_repo(status_list=target_status)

    if not orders_list:
        print(f"No orders found")
        return
    return orders_list.sort(key=lambda x: x.created_at)
    # print(f"[SERVICE] RUSHING {len(orders_list)} ORDERS TO THE KITCHEN")
    #
    # for order in orders_list:
    #     process_order(order.id)
    # print(f"[SERVICE] ALL MISSING ORDERS PROCESSED")
