import boto3
import botocore
from botocore.exceptions import ClientError
import uuid
from django.utils import timezone

def create_aws_client(servies='s3', aws_access_key_id = None, aws_secret_access_key = None):

    s3 = boto3.client('s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    
    return s3

# def upload_file_to_s3(s3_client, bucket_name, file):
#     # Generate a unique key for the file
#     object_key = str(uuid.uuid4())

#     try:
#         # Upload the file to S3
#         s3_client.upload_fileobj(file, bucket_name, object_key)

#         # Generate the URL of the uploaded file
#         s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
         
#         return {"url": s3_url, "object_key": object_key}
#     except ClientError as e:
#         print(f"Failed to upload file to S3: {e}")
#         return None

def upload_file_to_s3_bucket(s3_client, bucket_name, file):

    object_key = f"{timezone.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:8]}_{file.name}"
    s3_client.upload_fileobj(file, bucket_name, object_key)

        # Generate a presigned URL to access the uploaded file
    url  = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"

    
    return {"url": url, "object_key": object_key}

    


def delete_image_from_s3(s3_client, object_key, bucket_name):

    # Delete the object (file) from the S3 bucket
    res = s3_client.delete_object(Bucket=bucket_name, Key=object_key)
    return res