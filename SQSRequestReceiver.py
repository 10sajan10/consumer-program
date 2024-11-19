import boto3
import json
import logging

class SQSRequestReceiver:

    def __init__(self):
        self.sqs_client = boto3.client('sqs')
