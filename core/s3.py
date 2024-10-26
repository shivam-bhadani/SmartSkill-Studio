import boto3
from .exceptions import BadRequestException

class S3:
    def __init__(self, access_key_id, secret_access_key, region):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
        )

    def generate_upload_presigned_url(self, file_key, file_type, bucket, expiresIn=3600):
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket,
                    'Key': file_key,
                    'ContentType': file_type
                },
                ExpiresIn=expiresIn # default expiry is 1 hour
            )
            return presigned_url
        except Exception as e:
            raise BadRequestException()
        
    def generate_read_presigned_url(self, file_key, bucket, expiresIn=259200):
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket, 
                    'Key': file_key
                },
                ExpiresIn=expiresIn # default expiry is 3 days
            )
            return presigned_url
        except Exception as e:
            raise BadRequestException()
        