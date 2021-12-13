import boto3
from botocore.exceptions import ClientError
import sys
sys.path.append("...")
from config import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class S3:

    def __init__(self):
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            self.s3_resource = boto3.resource(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            self.s3_client = boto3.resource(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
        else:
            self.s3_resource = boto3.resource('s3')
            self.s3_client = boto3.client('s3')

    def get_bucket_name(self):
        return AWS_STORAGE_BUCKET_NAME

    def list_all_buckets(self):
        return self.s3_resource.buckets.all()

    def list_all_objects(self, bucket_name):
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            return bucket.objects.all()
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                return False
            if e.response['Error']['Code'] == 'NoSuchBucket':
                return False
            else:
                return False
        except Exception as e:
            return False

    def get_object(self, bucket, key):
        ''' return object content '''
        try:
            obj =  self.s3_resource.Object(bucket, key)
            return obj.get()['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                return False
        except Exception as e:
            return False

    def delete_object(self,bucket_name, key):
        ''' delete object key '''
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            response = bucket.Object(key).delete()
            return response['ResponseMetadata']['HTTPStatusCode']
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                return False
        except Exception as e:
            return False

    def download_object(self,bucket_name, key):
        ''' return file content '''
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            file_obj = bucket.Object(key).get()
            return file_obj['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                return False
        except Exception as e:
            return False

    def put_object(self, bucket, key, content=None):
        ''' put content of key'''
        try:
            if not content: # create dir
                self.client.put_object(Bucket=bucket,Key=key)
            else: # create file with content
                self.s3_client.put_object(Body=content, Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                return False
        except Exception as e:
            return False

    def upload_object(self, bucket_name, file):
        ''' return file content '''
        key = file.filename
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            upload_obj = bucket.Object(key).put(Body=file)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                return False
        except Exception as e:
            return False