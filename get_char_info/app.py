import json
import boto3 
import os 
import requests
from decimal import Decimal
from urllib.parse import unquote

base_uri = "https://codepoints.net/api/v1/codepoint/"

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    if 'AWS_SAM_LOCAL' in os.environ:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
    else:
        dynamodb = boto3.resource('dynamodb')

    #Get Char String From URL
    char = unquote(event['pathParameters']['char'])
    print(char)
    
    #How Does This Work With Unicode?

    table = dynamodb.Table('Unicode')
    unicode_value = ord(char)
    response = table.get_item(
        Key={
            'char': char
        }
    ) 
    
    #Check If Response Exists
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'], cls=DecimalEncoder)
        }
    else:
        #Get the Unicode Value of Char 
        #Get the Unicode Info From Codepoints.net
        unicode_info = requests.get(base_uri + hex(unicode_value)[2:])
        #Get the na Fields From JSON respone

        unicode_name = unicode_info.json()['na']

        #Store In DynamoDB
        table.put_item(
            Item={
                'char': char,
                'unicode_value': unicode_value,
                'unicode_name': unicode_name
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'char': char,
                'unicode_value': unicode_value,
                'unicode_name': unicode_name
            })
        }
