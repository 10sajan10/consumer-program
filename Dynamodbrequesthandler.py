import boto3
import time
import logging
from S3_read import S3RequestAndObjectReceiver
from SQSRequestReceiver import SQSRequestReceiver
import json

class DynamoDBRequestHandler:
    def __init__(self, table_name):
        """
        Initializes the DynamoDBRequestHandler with the specified DynamoDB table.

        Args:
            table_name (str): The name of the DynamoDB table.
        """
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')#specified region
        self.table = self.dynamodb.Table(table_name)

    def handle_request(self, request_type, body):
        """
        Handles the request based on its type.

        Args:
            request_type (str): The type of request ('create', 'delete', or 'update').
            body (dict): The body of the request containing relevant information.
            key (str): The ID of the item being processed (used for delete).
        """
        widget_id = body.pop('widgetId')
        if request_type:
            logging.info(request_type)
            if request_type == 'create':
                self.create_item(body, widget_id)
            elif request_type == 'delete':
                self.delete_item(widget_id)
            elif request_type == 'update':
                self.update_item(body,widget_id)
            else:
                logging.error(f"Unknown request type: {request_type}")

    def create_item(self, body, widget_id):
        """Create a new item in the DynamoDB table."""

        other_attributes = body.pop('otherAttributes',None)
        if widget_id:
            # Prepare the item to be put into DynamoDB
            item = {
                'id': widget_id,  # Partition key
                **body  # Start with all attributes from body
            }

            # Flatten the otherAttributes into the item
            if other_attributes:
                for attr in other_attributes:
                    item[attr['name']] = attr['value']  # Map each other attribute

            self.table.put_item(Item=item)
            logging.info(f'Created item with id {widget_id} in DynamoDB.')

        else:
            logging.error("Invalid data for creating item.")

    def delete_item(self, widget_id):
        """Delete an item from the DynamoDB table."""
        try:
            response = self.table.delete_item(
                Key={'id': widget_id},
                ReturnValues='ALL_OLD'  # Return deleted item's attributes
            )
            if 'Attributes' in response:
                logging.info(f"Deleted item with id {widget_id} from DynamoDB.")
            else:
                logging.warning(f"No item with id {widget_id} was found in DynamoDB.")
        except Exception as e:
            logging.error(f"Failed to delete item with id {widget_id}: {e}")
        pass

    def update_item(self, body, widget_id):
        """Update an existing item in the DynamoDB table or create it if it doesn't exist."""
        try:
            # Check if the item exists
            existing_item = self.table.get_item(Key={'id': widget_id}).get('Item')

            if existing_item:
                # Update the existing item by merging attributes
                updated_item = {**existing_item, **body}
                self.table.put_item(Item=updated_item)
                logging.info(f"Updated item with id {widget_id} in DynamoDB.")
            else:
                # Item does not exist, create a new one
                logging.warning(f"Item with id {widget_id} not found. Creating a new item.")
                self.create_item(body, widget_id)

        except Exception as e:
            logging.error(f"Failed to update item with id {widget_id}: {e}")

    def process_request_from_s3(self, source_bucket):
        """
        Continuously process requests from the source bucket until a stop condition is met.

        Args:
            source_bucket (str): The name of the source S3 bucket to read requests from.
        """
        request_receiver = S3RequestAndObjectReceiver(source_bucket)

        cumulative_wait_time = 0  # Initialize cumulative wait time

        while cumulative_wait_time < 5:  # Continue until 5 seconds of cumulative wait time
            # Try to get a request
            request_type, body, key = request_receiver.get_smallest_object()

            if key:
                # Process the request

                self.handle_request(request_type, body)
                request_receiver.s3_client.delete_object(Bucket=source_bucket, Key=key)

                # Reset cumulative wait time since a key was found
                cumulative_wait_time = 0
            else:
                # Wait for a while before checking again
                time.sleep(0.1)  # Wait for 100 ms
                cumulative_wait_time += 0.1  # Increment cumulative wait time

        logging.info("No new requests for 5 seconds. Stopping processing.")

    def SQS_message_delete(self, sqsreceiver, source_queueurl, receipt_handle):
            sqsreceiver.sqs_client.delete_message(QueueUrl=source_queueurl,ReceiptHandle=receipt_handle)

    def process_request_from_queue(self, source_queueurl):
        if source_queueurl:
            SQSrequest_receiver = SQSRequestReceiver(source_queueurl)

            cumulative_wait_time = 0  # Initialize cumulative wait time

            while cumulative_wait_time < 3:  # Continue until 5 seconds of cumulative wait time
                # Try to get a request
                messages = SQSrequest_receiver.retrieve_messages_from_queue(maxno=10)
                if messages is not None:
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
                            self.handle_request(request_type,json_data)
                        else:
                            logging.error("Invalid data for creating object.")
                        self.SQS_message_delete(SQSrequest_receiver, source_queueurl,receipt_handle)
                        cumulative_wait_time = 0

                else:
                    # Wait for a while before checking again
                    time.sleep(0.1)  # Wait for 100 ms
                    cumulative_wait_time += 1  # Increment cumulative wait time

            logging.info("No new requests for 3 ReTries. Stopping processing.")
