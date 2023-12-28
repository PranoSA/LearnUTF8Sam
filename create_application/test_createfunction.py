import sys
#from unicode_exam_api.create_application.app import lambda_handler
#import unicode_exam_api.create_application.app as app

from app import lambda_handler

import boto3
import json
import os
import unittest
from moto import mock_dynamodb
import moto as moto 
#from create_application import lambda_handler  # replace with your actual import


@mock_dynamodb
class TestCreateApplicationFunction(unittest.TestCase):
    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

        # Create the DynamoDB table
        self.table = self.dynamodb.create_table(
            TableName='Applications',
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'appid',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'appid',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists
        self.table.meta.client.get_waiter('table_exists').wait(TableName='Applications')

    def test_create_application(self):
        event = {
            "headers": {
                "Cookie": "user=test_user"
            },
            "body": "{\"appid\": \"app1\", \"name\": \"Application 1\", \"created_at\": \"2022-01-01\", \"updated_at\": \"2022-01-01\", \"description\": \"This is a test application\", \"conversions\": [{\"value\": \"test1\"}, {\"value\": \"test2\"}]}"
        }

        lambda_handler(event, {})

        response = self.table.get_item(
            Key={
                'user_id': 'test_user',
                'appid': 'app1'
            }
        )

        self.assertEqual(response['Item']['name'], 'Application 1')
        self.assertEqual(response['Item']['description'], 'This is a test application')
        self.assertEqual(response['Item']['conversions'], [{'value': 'test1'}, {'value': 'test2'}])
