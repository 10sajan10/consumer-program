import boto3
import json

BUCKET_NAME = 'usu-cs5250-sajan-requests'
PREFIX = "widgets"
TARGET_BUCKET = 'usu-sajan-testbucket'

s3_client = boto3.client('s3')

# Retrieve the smallest key from the bucket
response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=1)

# Check if there is an object
if 'Contents' in response:
    key = response['Contents'][0]['Key']
    print(f'Smallest key: {key}')

    # Get the object content
    object_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    body = object_response['Body'].read().decode('utf-8')
    json_body = json.loads(body)

    # Process JSON content
    print(json_body)
    owner = json_body['owner']
    widget_id = json_body['widgetId']

    # Upload to target bucket with new key
    new_key = f'{PREFIX}/{owner}/{widget_id}'
    s3_client.put_object(Bucket=TARGET_BUCKET, Key=new_key, Body=body)

    print(f"Object uploaded to {TARGET_BUCKET} with key {new_key}")

else:
    print("No objects found in the bucket.")
