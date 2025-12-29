import json
import sys
import os

sys.path.append(os.getcwd()) #This assures that python finds the confg and service files
from Configs.sqs_client import get_sqs_client,get_queue_url
from Services.order_service import OrderStatus, get_locked_orders
from Repository.pedido_repository import OrderRepository

def rescue_and_enqueue(locked_orders):
    print("SEEKING...")
    sqs = get_sqs_client()
    try:
        queue_url = get_queue_url("fila-pedidos")
    except Exception as e:
        return print(f"ERROR IN RESCUER: {e}")


    if not locked_orders:
        return print("NO ORDERS FOUND BY RESCUER")

    count = 0
    for order in locked_orders:
        try:
            message_body={
                "id": order.id,
                "item": order.item
            }
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body)
            )
            print(f"ORDER {order.id} RESCUED")
            count += 1
        except Exception as e:
            print(f"ERROR IN RESCUER: {e}")
    print(f"RESCUED {count} ORDERS")
    return None
