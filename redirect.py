import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):

    short_code = event['pathParameters']['short_code']

    response = table.get_item(
        Key={'short_code': short_code}
    )

    item = response.get('Item')

    if not item:
        return {
            "statusCode": 404,
            "body": "Not Found"
        }

    # update clicks
    table.update_item(
        Key={'short_code': short_code},
        UpdateExpression="SET clicks = if_not_exists(clicks, :start) + :inc",
        ExpressionAttributeValues={
            ':inc': 1,
            ':start': 0
        }
    )

    return {
        "statusCode": 301,
        "headers": {
            "Location": item['long_url']
        }
    }
