import boto3
from botocore.exceptions import ClientError
import sys
sys.path.append("...")
from config import BUCKET_NAME, ACCESS_KEY, SECRET_KEY

class S3:

    def __init__(self):
        if ACCESS_KEY and SECRET_KEY:
            self.s3_resource = boto3.resource(
                's3',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY
            )
            self.s3_client = boto3.resource(
                's3',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY
            )
        else:
            self.s3_resource = boto3.resource('s3')
            self.s3_client = boto3.client('s3')

    def get_bucket_name(self):
        return BUCKET_NAME

    def list_all_buckets(self):
        return self.s3_resource.buckets.all()

    def list_all_objects(self, bucket_name):
        bucket = self.s3_resource.Bucket(bucket_name)
        return bucket.objects.all()

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