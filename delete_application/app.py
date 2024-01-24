import os
import boto3
import json
from http import cookies
import os

def lambda_handler(event, context):
    #Deletes Application

    #Get user_id and appid from path parameters

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

    #Delete item from table

    try:
        table.delete_item(
            Key={
                'user_id': user_id,
                'appid': appid
            }
        )
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Application not found!')
        }
    

    return {
        'statusCode': 200,
        'body': json.dumps('Application deleted successfully!')
    }
