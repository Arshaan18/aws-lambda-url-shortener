import json
import boto3
import string
import random
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def lambda_handler(event, context):
    print(f"Event received: {json.dumps(event)}")
    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method', 'GET')
    path = event.get('path') or event.get('rawPath', '/')

    if http_method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
            long_url = body.get('long_url')
            if not long_url:
                return response(400, {'error': 'long_url is required'})
            short_code = generate_short_code()
            created_at = datetime.utcnow().isoformat()
            table.put_item(Item={
                'short_code': short_code,
                'long_url': long_url,
                'created_at': created_at,
                'hits': 0
            })
            return response(200, {
                'short_code': short_code,
                'long_url': long_url,
                'created_at': created_at,
                'message': 'Short URL created successfully'
            })
        except Exception as e:
            return response(500, {'error': str(e)})

    elif http_method == 'GET':
        try:
            short_code = path.strip('/').split('/')[-1]
            if not short_code:
                return response(400, {'error': 'short_code is required'})
            result = table.get_item(Key={'short_code': short_code})
            item = result.get('Item')
            if not item:
                return response(404, {'error': 'Short URL not found'})
            table.update_item(
                Key={'short_code': short_code},
                UpdateExpression='SET hits = hits + :val',
                ExpressionAttributeValues={':val': 1}
            )
            return response(200, {
                'short_code': short_code,
                'long_url': item['long_url'],
                'hits': int(item['hits']) + 1,
                'created_at': item['created_at']
            })
        except Exception as e:
            return response(500, {'error': str(e)})
    else:
        return response(405, {'error': 'Method not allowed'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }
