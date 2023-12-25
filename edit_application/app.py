import os
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
    appid = event['pathParameters']['applicationid']

    body = json.loads(event['body'])
    name = body['name']
    updated_at = body['updated_at']
    description = body['description']
    conversions = body['conversions']

    if 'AWS_SAM_LOCAL' in os.environ:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
    else:
        dynamodb = boto3.resource('dynamodb')


    # Check if conversions is a list of enumeratedConversations
    if not isinstance(conversions, list) or not all(isinstance(item, dict) and 'value' in item and isinstance(item['value'], str) for item in conversions):
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid format for conversions. It should be a list of enumeratedConversations.')
        }

    table.update_item(
        Key={
            'user_id': user_id,
            'appid': appid
        },
        UpdateExpression='SET name = :name, updated_at = :updated_at, description = :description, conversions = :conversions',
        ExpressionAttributeValues={
            ':name': name,
            ':updated_at': updated_at,
            ':description': description,
            ':conversions': conversions
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Application updated successfully!')
    }