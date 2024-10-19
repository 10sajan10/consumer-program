import boto3
import json
import time
from S3_read import S3RequestAndObjectReceiver
import logging

class S3RequestHandler:
    def __init__(self, target_bucket):
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
            if request_type == 'create':
                self.create_object(body)
            elif request_type == 'delete':
                self.delete_object(key)
            elif request_type == 'update':
                self.update_object(body)
            else:
                logging.error(f"Unknown request type: {request_type}")



    def create_object(self, body):
        """Create a new object in the target S3 bucket."""
        widget_id = body.get('widgetId')
        owner = body.get('owner', None)
        if widget_id:
            if not owner:
                owner = "unidentified"
            target_key = f'widgets/{owner}/{widget_id}'
            self.s3_client.put_object(Bucket=self.target_bucket, Key=target_key, Body=json.dumps(body))
            logging.info(f'Created object at {target_key}')
        else:
            logging.error("Invalid data for creating object.")

    def delete_object(self, key):
        """Delete an object from the target S3 bucket."""
        logging.error(f'Delete logic not yet implemented')

    def update_object(self, body):
        """Placeholder for updating an object in the target S3 bucket."""
        logging.error("Update logic not yet implemented.")

    def process_requests(self, source_bucket):
        """
        Continuously process requests from the source bucket until a stop condition is met.

        Args:
            source_bucket (str): The name of the source S3 bucket to read requests from.
        """
        request_receiver = S3RequestAndObjectReceiver(source_bucket)

        while True:  # Replace with your stop condition
            # Try to get a request
            request_type, body, key = request_receiver.get_smallest_object()

            if key:
                # Process the request
                self.handle_request(request_type, body, key)
                request_receiver.s3_client.delete_object(Bucket=source_bucket, Key=key)
            else:
                # Wait a while before checking again
                time.sleep(0.1)  # Wait for 100 ms

