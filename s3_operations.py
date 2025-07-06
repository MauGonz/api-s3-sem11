import boto3
import json

s3 = boto3.client('s3')

def create_directory_handler(event, context):
    print(f"Received event: {event}")
    print(f"Type of event['body']: {type(event.get('body'))}")
    print(f"Content of event['body']: {event.get('body')}")

    try:
        body = event.get('body')

        if isinstance(body, str):
            payload = json.loads(body)
        elif isinstance(body, dict):
            payload = body
        else:
            raise TypeError("Request body must be a string (JSON) or a dictionary.")

        bucket_name = payload.get('bucket_name')
        directory_name = payload.get('directory_name')

        if not bucket_name or not directory_name:
            return {
                'statusCode': 400,
                'message': 'Missing bucket_name or directory_name in request body.'
            }

        s3.put_object(Bucket=bucket_name, Key=(directory_name + '/'))

        return {
            'statusCode': 200,
            'message': f'Directory {directory_name} created in bucket {bucket_name} successfully'
        }
    except json.JSONDecodeError as e:
        print(f"JSON Decoding Error: {e}")
        return {
            'statusCode': 400,
            'message': f"Invalid JSON format in request body: {e}"
        }
    except TypeError as e:
        print(f"Type Error in Lambda: {e}")
        return {
            'statusCode': 400,
            'message': f"Bad request payload type: {e}"
        }
    except Exception as e:
        print(f"General Error in Lambda: {e}")
        return {
            'statusCode': 500,
            'message': str(e)
        }
