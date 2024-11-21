import logging
import os
from datetime import datetime
from S3requesthandler import S3RequestHandler
from Dynamodbrequesthandler import DynamoDBRequestHandler
import argparse

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
log_file_path = os.path.join(log_dir, log_filename)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
                    handlers=[
                        logging.FileHandler(log_file_path),  # Log to the file with today's date
                        logging.StreamHandler()  # Also log to console
                    ])

parser = argparse.ArgumentParser(description="Process source and target S3 bucket names and DynamoDB table name.")
parser.add_argument('-rb', '--sourcebucket', type=str, default=None,required=False, help="The name of the request S3 bucket.")
parser.add_argument('-rq', '--sourcequeue', type=str, default=None,required=False, help="The name of the request S3 bucket.")
parser.add_argument('-wb', '--target', type=str, default=None, required=False, help="The name of the widgets S3 bucket.")
parser.add_argument('-dt', '--dynamodb', type=str, default=None, required=False, help="The name of the DynamoDB table.")
args = parser.parse_args()

request_queue = args.sourcequeue
request_bucket = args.sourcebucket
widget_bucket = args.target
table_name = args.dynamodb

def main():

    if widget_bucket and table_name:
        logging.error('Please specify only one Target')
        exit()

    if request_queue and request_bucket:
        logging.error('Please specify only one Request Source')
        exit()

    if request_bucket and widget_bucket:
        logging.info(
            f"Processing requests from source S3 bucket: {request_bucket} to target S3 bucket: {widget_bucket}")
        s3_handler = S3RequestHandler(widget_bucket)
        s3_handler.process_request_from_s3(request_bucket)

        # S3 to DynamoDB
    elif table_name and request_bucket:
        logging.info(f"Processing requests from S3 bucket: {request_bucket} to DynamoDB table: {table_name}")
        dynamodb_handler = DynamoDBRequestHandler(table_name)
        dynamodb_handler.process_request_from_s3(request_bucket)

        # SQS to DynamoDB
    elif table_name and request_queue:
        logging.info(f"Processing requests from SQS queue: {request_queue} to DynamoDB table: {table_name}")
        dynamodb_handler = DynamoDBRequestHandler(table_name)
        dynamodb_handler.process_request_from_queue(request_queue)

        # SQS to S3
    elif widget_bucket and request_queue:
        logging.info(f"Processing requests from SQS queue: {request_queue} to target S3 bucket: {widget_bucket}")
        s3_handler = S3RequestHandler(widget_bucket)
        s3_handler.process_request_from_queue(request_queue)

    else:
        logging.error("Insufficient arguments provided. Please specify required arguments for processing.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")