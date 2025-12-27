import boto3

def get_sqs_client(): #this is the func to create a connection with sqs, but we are using localstack so tells boto3 to not try connect to internet but with local docker
    LOCALSTACK_URL = "http://localhost:4566"

    sqs = boto3.client(
        'sqs',
        region_name='us-east-1',
        endpoint_url=LOCALSTACK_URL,
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
    return sqs

def get_queue_url(queue_name): #this function gets the complete url based on the params queue name
    sqs = get_sqs_client()
    try:
        response =sqs.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']
    except sqs.exceptions.QueueDoesNotExist:
        print(f"Queue {queue_name} does not exist. Creating...")
        raise Exception("Queue does not exist")
        # response = sqs.create_queue(QueueName=queue_name)
        # return response['QueueUrl']
