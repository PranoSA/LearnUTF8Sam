import boto3
import json
from http import cookies
import os
import uuid

def lambda_handler(event, context):

    if 'AWS_SAM_LOCAL' in os.environ:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.20.128.154:4566', region_name='us-east-1')
        #dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:4566', region_name='us-east-1')
        #dynamodb = boto3.resource('dynamodb', endpoint_url='http://sd1230912391294124991.sdsad.123121:4566', region_name='us-east-1')
        print('local \n')
    else:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Applications')

    cookie_string = event['headers']['Cookie']
    cookie = cookies.SimpleCookie()
    cookie.load(cookie_string)
    user_id = cookie['user'].value

    body = json.loads(event['body'])
    #appid = body['appid']
    appid = str(uuid.uuid4())
    name = body['name']
    created_at = body['created_at']
    updated_at = body['updated_at']
    description = body['description']
    conversions = body['conversions']

    #print(table)

  #  return {
        #'statusCode': 300,
        #'body': json.dumps("Lets See if return")
   # }

    print(conversions)

    if not isinstance(conversions, list) or not all(isinstance(item, dict) and 'value' in item and isinstance(item['value'], str) for item in conversions):
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid format for conversions. It should be a list of enumeratedConversations.')
        }
    
    Item={
        'user_id': user_id,
        'appid': appid,
        'name': name,
        'created_at': created_at,
        'updated_at': updated_at,
        'description': description,
        'conversions': conversions
    }

    try:
        print("trying dynamo")
        print(Item)

        table.put_item(
            Item=Item,
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Application created successfully!')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to Connect to DynamoDB')
        }