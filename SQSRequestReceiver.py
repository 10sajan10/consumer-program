import boto3
import botocore

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
                print("No messages")
            for message in messages:
                print(message)
                print("\n")
            return messages
        except botocore.exceptions.ClientError as e:
            print("Something went wrong")
            print(e)
            exit()

sqs = SQSRequestReceiver('https://sqs.us-east-1.amazonaws.com/186579595491/cs5250-requests').retrieve_messages_from_queue(10)

