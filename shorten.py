import json
import boto3
import random
import string

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("url-mappings")

API_URL = "https://008jmqrlo7.execute-api.us-east-1.amazonaws.com"

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]

    if method == "POST":

        body = json.loads(event["body"])
        long_url = body["url"]

        # Check if user provided custom alias
        short_code = body.get("alias")

        if not short_code:
            short_code = generate_code()

        table.put_item(
            Item={
                "short_code": short_code,
                "long_url": long_url
            }
        )

        short_url = f"{API_URL}/{short_code}"

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "short_url": short_url
            })
        }
