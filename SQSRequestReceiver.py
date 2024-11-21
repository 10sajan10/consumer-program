import boto3
import botocore
import logging

class SQSRequestReceiver:

    def __init__(self, url):
        self.sqs_client = boto3.client('sqs')
        self.url = url

    def retrieve_messages_from_queue(self,maxno=20):
        try:
            response = self.sqs_client.receive_message(
            QueueUrl=self.url,
            MaxNumberOfMessages=maxno,
            VisibilityTimeout=60,
            WaitTimeSeconds=10
        )
            messages = response.get('Messages', None)
            if not messages:
                logging.info("No messagessss")
            return messages
        except botocore.exceptions.ClientError as e:
            logging.error("Something went wrong")
            logging.error(e)
            exit()


