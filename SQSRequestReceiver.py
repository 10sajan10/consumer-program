import boto3
import botocore

class SQSRequestReceiver:

    def __init__(self):
        self.sqs_client = boto3.client('sqs')
        self.url = 'https://sqs.us-east-1.amazonaws.com/186579595491/cs5250-requests'

    def retrieve_messages_from_queue(self,maxno=10):
        try:
            response = self.sqs_client.receive_message(
            QueueUrl=self.url,
            MaxNumberOfMessages=maxno,
            VisibilityTimeout=60,
            WaitTimeSeconds=10
        )
            messages = response.get('Messages', [])
            print(messages)
            return messages
        except botocore.exceptions.ClientError as e:
            print("Something went wrong")
            print(e)
            exit()



sqs= SQSRequestReceiver()
print(sqs.retrieve_messages_from_queue())

