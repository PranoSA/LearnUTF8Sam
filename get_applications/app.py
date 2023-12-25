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

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }