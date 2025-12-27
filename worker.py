import json
import time
from Configs.sqs_client import get_sqs_client, get_queue_url
from Services.order_service import update_order_status


def start_worker():
    sqs = get_sqs_client()
    queue_url = get_queue_url('fila-pedidos')

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
                    id = body.get('id')
                    item_name = body.get('item')

                    print(f"NEW ORDER: {id} \n ITEM NAME: {item_name}")

                    update_order_status()

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
