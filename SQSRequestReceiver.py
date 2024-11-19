import boto3
import json
import logging

class SQSRequestReceiver:

    def __init__(self):
        self.sqs_client = boto3.client('sqs')
        self.url = 'https://sqs.us-east-1.amazonaws.com/186579595491/cs5250-requests'

    def retrieve_messages_from_queue(self):
        response = self.sqs_client.receive_message(
            QueueUrl=self.url,
            MaxNumberOfMessages=10,  # Retrieve up to 10 messages at once
            WaitTimeSeconds=10  # Long polling
        )
        messages = response.get('Messages', [])

        if messages:
            for message in messages:
                print(message)



sqs= SQSRequestReceiver()
sqs.retrieve_messages_from_queue()

