import boto3
import json
from http import cookies
import os

def lambda_handler(event, context):

    if 'AWS_SAM_LOCAL' in os.environ:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
    else:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Applications')

    cookie_string = event['headers']['Cookie']
    cookie = cookies.SimpleCookie()
    cookie.load(cookie_string)
    user_id = cookie['user'].value

    body = json.loads(event['body'])
    appid = body['appid']
    name = body['name']
    created_at = body['created_at']
    updated_at = body['updated_at']
    description = body['description']
    conversions = body['conversions']

    if not isinstance(conversions, list) or not all(isinstance(item, dict) and 'value' in item and isinstance(item['value'], str) for item in conversions):
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid format for conversions. It should be a list of enumeratedConversations.')
        }

    table.put_item(
        Item={
            'user_id': user_id,
            'appid': appid,
            'name': name,
            'created_at': created_at,
            'updated_at': updated_at,
            'description': description,
            'conversions': conversions
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Application created successfully!')
    }