import boto3 
import os 
import requests

base_uri = "https://codepoints.net/api/v1/codepoint/"

def lambda_handler(event, context):
    if 'AWS_SAM_LOCAL' in os.environ:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
    else:
        dynamodb = boto3.resource('dynamodb')

    #Get Char String From URL
    char = event['pathParameters']['char']
    
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
            'body': response['Item']
        }
    else:
        #Get the Unicode Value of Char 
        #Get the Unicode Info From Codepoints.net
        unicode_info = requests.get(base_uri + unicode_value)
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
            'body': {
                'char': char,
                'unicode_value': unicode_value,
                'unicode_name': unicode_name
            }
        }
