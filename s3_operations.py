import boto3
import json

s3 = boto3.client('s3')

def get_request_body(event):
    body = event.get('body')

    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request body string.")
    elif isinstance(body, dict):
        return body
    else:
        raise TypeError("Request body must be a JSON string or a dictionary.")


def create_bucket_handler(event, context):
    try:
        body = get_request_body(event)
        
        bucket_name = body.get('bucket_name') 

        if not bucket_name:
            return {
                'statusCode': 400,
                'message': 'Missing "bucket_name" in request body.'
            }

        s3.create_bucket(Bucket=bucket_name)
        return {
            'statusCode': 200,
            'message': f'Bucket {bucket_name} created successfully'
        }
    except (ValueError, TypeError) as e:
        return {
            'statusCode': 400, 
            'message': str(e)
        }
    except Exception as e:
        print(f"Error in create_bucket_handler: {e}") 
        return {
            'statusCode': 500,
            'message': f"Failed to create bucket: {str(e)}"
        }

def create_directory_handler(event, context):
    try:
        body = get_request_body(event)
        
        bucket_name = body.get('bucket_name')
        directory_name = body.get('directory_name')

        if not bucket_name or not directory_name:
            return {
                'statusCode': 400,
                'message': 'Missing "bucket_name" or "directory_name" in request body.'
            }

        if not directory_name.endswith('/'):
            directory_name += '/'

        s3.put_object(Bucket=bucket_name, Key=directory_name)
        return {
            'statusCode': 200,
            'message': f'Directory {directory_name} created in bucket {bucket_name} successfully'
        }
    except (ValueError, TypeError) as e:
        return {
            'statusCode': 400, 
            'message': str(e)
        }
    except Exception as e:
        print(f"Error in create_directory_handler: {e}") 
        return {
            'statusCode': 500,
            'message': f"Failed to create directory: {str(e)}"
        }

def upload_file_handler(event, context):
    try:
        body = get_request_body(event)
        
        bucket_name = body.get('bucket_name')
        file_name = body.get('file_name')
        file_content_base64 = body.get('file_content')

        if not bucket_name or not file_name or file_content_base64 is None:
            return {
                'statusCode': 400,
                'message': 'Missing "bucket_name", "file_name", or "file_content" in request body.'
            }
        
        try:
            file_content_bytes = base64.b64decode(file_content_base64)
        except Exception as e:
            return {
                'statusCode': 400,
                'message': f"Invalid Base64 content for file_content: {str(e)}"
            }

        content_type = 'application/octet-stream'
        if file_name.lower().endswith('.png'):
            content_type = 'image/png'

        s3.put_object(
            Bucket=bucket_name, 
            Key=file_name, 
            Body=file_content_bytes,
            ContentType=content_type
        )
        
        return {
            'statusCode': 200,
            'message': f'File {file_name} uploaded to bucket {bucket_name} successfully'
        }
    except (ValueError, TypeError) as e:
        return {
            'statusCode': 400,
            'message': str(e)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': f"Failed to upload file: {str(e)}"
        }
