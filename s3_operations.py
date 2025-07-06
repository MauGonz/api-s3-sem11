import boto3
import json

s3 = boto3.client('s3')

def create_bucket_handler(event, context):
    try:
        body = json.loads(event['body'])
        bucket_name = body['bucket_name']
        s3.create_bucket(Bucket=bucket_name)
        return {
            'statusCode': 200,
            'message': f'Bucket {bucket_name} created successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': str(e)
        }

def create_directory_handler(event, context):
    try:
        body = json.loads(event['body'])
        bucket_name = body['bucket_name']
        directory_name = body['directory_name']
        s3.put_object(Bucket=bucket_name, Key=(directory_name + '/') )
        return {
            'statusCode': 200,
            'message': f'Directory {directory_name} created in bucket {bucket_name} successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': str(e)
        }

def upload_file_handler(event, context):
    try:
        body = json.loads(event['body'])
        bucket_name = body['bucket_name']
        file_name = body['file_name']
        file_content = body['file_content']

        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        return {
            'statusCode': 200,
            'message': f'File {file_name} uploaded to bucket {bucket_name} successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': str(e)
        }