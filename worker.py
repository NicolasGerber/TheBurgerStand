from Configs.sqs_client import get_sqs_client, get_queue_url


def process_order():
    sqs = get_sqs_client()
    queue_url = get_queue_url('order_queue')

    print(f"[*] Processing order...")
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
            )