import boto3
import time
from S3_read import S3RequestAndObjectReceiver  # Ensure this module is adapted to work with DynamoDB

class DynamoDBRequestHandler:
    def __init__(self, table_name):
        """
        Initializes the DynamoDBRequestHandler with the specified DynamoDB table.

        Args:
            table_name (str): The name of the DynamoDB table.
        """
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def handle_request(self, request_type, body, key):
        """
        Handles the request based on its type.

        Args:
            request_type (str): The type of request ('create', 'delete', or 'update').
            body (dict): The body of the request containing relevant information.
            key (str): The ID of the item being processed (used for delete).
        """
        if request_type:
            print(request_type)
            if request_type == 'create':
                self.create_item(body)
            elif request_type == 'delete':
                self.delete_item(key)
            elif request_type == 'update':
                self.update_item(body)
            else:
                print(f"Unknown request type: {request_type}")

    def create_item(self, body):
        """Create a new item in the DynamoDB table."""
        widget_id = body.pop('widgetId')
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
            print(f'Created item with id {widget_id} in DynamoDB.')
        else:
            print("Invalid data for creating item.")

    def delete_item(self, widget_id):
        """Delete an item from the DynamoDB table."""
        #self.table.delete_item(Key={'id': widget_id})
        print('Delete Logic not yet implemented')
        pass

    def update_item(self, body):
        """Update an existing item in the DynamoDB table."""
        print('Update Logic not yet implemented')
        pass

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

dynamodb_handler = DynamoDBRequestHandler(table_name='widgets')
dynamodb_handler.process_requests('usu-sajan-testrequest')