import boto3
import time

BUCKET_NAME = 'usu-cs5250-sajan-requests'
PREFIX = None
DELAY = 10


def get_sorted_widget_requests(bucket_name, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name,)

    if 'Contents' in response:
        keys = [obj['Key'] for obj in response['Contents']]
        sorted_keys = sorted(keys)
        return sorted_keys
    else:
        print("No objects found in the specified bucket.")
        return []


def process_widget_request(key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    widget_request = response['Body'].read().decode('utf-8')
    print(f"Processing widget request from {key}: {widget_request}")


def main():
    while True:
        sorted_keys = get_sorted_widget_requests(BUCKET_NAME, PREFIX)
        if sorted_keys:
            smallest_key = sorted_keys[0]
            process_widget_request(smallest_key)
        time.sleep(DELAY)


if __name__ == "__main__":
    main()
