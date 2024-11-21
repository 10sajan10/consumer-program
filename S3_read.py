import boto3
import json
import logging
import botocore

class S3RequestAndObjectReceiver:
    def __init__(self, source_bucket):
        self.s3_client = boto3.client('s3')
        self.source_bucket = source_bucket

    def get_smallest_object(self):
        """
        Retrieves the object with the smallest key from the source bucket, parses its contents, and
        returns the request type along with the modified body (without 'type' and 'requestId').
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.source_bucket, MaxKeys=1)

            if 'Contents' in response:
                key = response['Contents'][0]['Key']
                logging.info(f'Smallest key: {key}')

                # Retrieve the object content
                object_response = self.s3_client.get_object(Bucket=self.source_bucket, Key=key)
                body = object_response['Body'].read().decode('utf-8')
                if not body.strip():  # If the body is empty or contains only whitespace
                    logging.error(f'Object {key} is empty, skipping.')
                    return None, None, key  # Skip to the next object
                # Parse the body as JSON
                body_json = json.loads(body)

                # Extract the request type and remove 'type' and 'requestId' from the body
                request_type = body_json.pop('type', None)
                body_json.pop('requestId', None)
                # Return the request type and the modified body
                return request_type, body_json, key
            else:
                return None, None, None

        except botocore.exceptions.ClientError as e:
            logging.error(f'{e}')
            exit()
