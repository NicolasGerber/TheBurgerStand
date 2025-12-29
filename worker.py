import json
import time
from Configs.sqs_client import get_sqs_client, get_queue_url
from Services.order_service import update_order_status, process_order

def start_worker():
    sqs = get_sqs_client()
    queue_url = get_queue_url('fila-pedidos')

    print(f"WORKER STARTED")
    print(f"WAITING FOR ORDERS")
    print(f">>>>>>>>> >>>>>>>>>> >>>>>>>>>")



    while True:
        try:  #here the worker asks the queue if it has a response
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10
            )

            if 'Messages' in response:
                for message in response['Messages']:
                    body = json.loads(message['Body'])
                    order_id = body.get('id')
                    item_name = body.get('item')

                    print(f"NEW ORDER: {order_id} \n ITEM NAME: {item_name}")
                    update_order_status(order_id)
                    time.sleep(5)
                    process_order(order_id)

                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                print(f"Order has been processed , removing from queue")



            else:
                print(".", end="", flush=True)
        except Exception as e:
            print(f"WORKER HAS AN ERROR: {e}")
            time.sleep(5)
