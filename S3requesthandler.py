import boto3
import json
import time
from S3_read import S3RequestAndObjectReceiver
from SQSRequestReceiver import SQSRequestReceiver
import logging

class S3RequestHandler:
    def __init__(self, target_bucket,):
        """
        Initializes the S3RequestHandler with the target S3 bucket.

        Args:
            target_bucket (str): The name of the target S3 bucket.
        """
        self.s3_client = boto3.client('s3')
        self.target_bucket = target_bucket


    def handle_request(self, request_type, body, key):
        """
        Handles the request based on its type.

        Args:
            request_type (str): The type of request ('create', 'delete', or 'update').
            body (dict): The body of the request containing relevant information.
            key (str): The key of the object being processed (used for delete).
        """
        if request_type:
            logging.info(request_type)
            print(request_type)
            if request_type == 'create':
                self.create_object(body, key)
            elif request_type == 'delete':
                self.delete_object(key)
            elif request_type == 'update':
                self.update_object(body,key)
            else:
                logging.error(f"Unknown request type: {request_type}")
                print(f"Unknown request type: {request_type}")



    def create_object(self, body, key):
        """Create a new object in the target S3 bucket."""
        self.s3_client.put_object(Bucket=self.target_bucket, Key=key, Body=json.dumps(body))
        logging.info(f"Object created: {self.target_bucket}{key}")
        print(f"Object created: {self.target_bucket}{key}")


    def delete_object(self, key):
        """Delete an object from the target S3 bucket."""
        try:
            self.s3_client.delete_object(Bucket=self.target_bucket, Key=key)
            logging.info(f'Deleted object {key} from bucket {self.target_bucket}')
            print(f"Deleted object {key} from bucket {self.target_bucket}")
        except self.s3_client.exceptions.NoSuchKey:
            logging.warning(f'Object {key} does not exist in bucket {self.target_bucket}. Nothing to delete.')
            print(f'Object {key} does not exist in bucket {self.target_bucket}. Nothing to delete.')

    def update_object(self, body, key):
        """Placeholder for updating an object in the target S3 bucket."""
        logging.error("Update logic not yet implemented.")
        print("Update logic not yet implemented.")
    def process_requests_from_s3(self,source_bucket):
        """
        Continuously process requests from the source bucket until a stop condition is met.

        Args:
            source_bucket (str): The name of the source S3 bucket to read requests from.
        """
        if source_bucket:
            s3request_receiver = S3RequestAndObjectReceiver(source_bucket)

            cumulative_wait_time = 0  # Initialize cumulative wait time

            while cumulative_wait_time < 5:  # Continue until 5 seconds of cumulative wait time
            # Try to get a request
                request_type, body, key = s3request_receiver.get_smallest_object()

                if key:
                    json_data = json.loads(body)
                    request_type = json_data.pop('type', None)

                    """Create a new object in the target S3 bucket."""
                    widget_id = json_data.get('widgetId', None)
                    owner = json_data.get('owner', None)
                    if widget_id:
                        if not owner:
                            owner = "unidentified"
                        target_key = f'widgets/{owner}/{widget_id}'
                    self.handle_request(request_type, body, target_key)
                    s3request_receiver.s3_client.delete_object(Bucket=source_bucket, Key=key)

                    # Reset cumulative wait time since a key was found
                    cumulative_wait_time = 0
                else:
                    # Wait for a while before checking again
                    time.sleep(0.1)  # Wait for 100 ms
                    cumulative_wait_time += 0.1  # Increment cumulative wait time

            logging.info("No new requests for 5 seconds. Stopping processing.")
            print("No new requests for 5 seconds. Stopping processing.")

    def SQS_message_delete(self, sqsreceiver, source_queueurl, receipt_handle):
            sqsreceiver.sqs_client.delete_message(QueueUrl=source_queueurl,ReceiptHandle=receipt_handle)

    def process_request_from_queue(self, source_queueurl):
        if source_queueurl:
            SQSrequest_receiver = SQSRequestReceiver(source_queueurl)

            cumulative_wait_time = 0  # Initialize cumulative wait time

            while cumulative_wait_time < 5:  # Continue until 5 seconds of cumulative wait time
                # Try to get a request
                messages = SQSrequest_receiver.retrieve_messages_from_queue(maxno=10)
                if messages:
                    for message in messages:
                        message_body = message['Body']
                        receipt_handle = message['ReceiptHandle']
                        message_id = message['MessageId']
                        json_data = json.loads(message_body)
                        request_type = json_data.pop('type', None)

                        """Create a new object in the target S3 bucket."""
                        widget_id = json_data.get('widgetId', None)
                        owner = json_data.get('owner', None)
                        if widget_id:
                            if not owner:
                                owner = "unidentified"
                            target_key = f'widgets/{owner}/{widget_id}'
                            self.handle_request(request_type,json_data, target_key)
                        else:
                            logging.error("Invalid data for creating object.")
                            print("Invalid data for creating object.")
                        self.SQS_message_delete(SQSrequest_receiver, source_queueurl,receipt_handle)
                        cumulative_wait_time = 0

                else:
                    # Wait for a while before checking again
                    time.sleep(0.1)  # Wait for 100 ms
                    cumulative_wait_time += 0.1  # Increment cumulative wait time

            logging.info("No new requests for 5 seconds. Stopping processing.")
            print("No new requests for 5 seconds. Stopping processing")


S3RequestHandler('usu-cs5250-sajan-web').process_request_from_queue('https://sqs.us-east-1.amazonaws.com/186579595491/cs5250-requests')


