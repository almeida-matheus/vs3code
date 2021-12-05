import boto3
from botocore.exceptions import ClientError

import sys
sys.path.append("...")
# from ...config import BUCKET_NAME, BUCKET_PATH, ACCESS_KEY, SECRET_KEY
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

        # self.s3_client.put_object(Body=binary_content, Bucket=BUCKET_NAME, Key='my/key/including/anotherfilename.txt')

        # content="String content to write to a new S3 file"
        # self.s3_resource.Object('my-bucket-name', 'newfile.txt').put(Body=content)

        # self.s3_resource.Bucket('bucketname').upload_file('/local/file/here.txt','folder/sub/path/to/s3key')

    def list_all_objects(self, bucket_name):
        all_object_files = []
        bucket = self.s3_resource.Bucket(bucket_name)
        return bucket.objects.all()

        # # for object_summary in bucket.objects.filter(Prefix=parent_path, Delimiter="/"): # ? first level
        # if BUCKET_PATH:
        #     for object_summary in bucket.objects.filter(Prefix=parent_path):
        #         all_object_files.append(object_summary.key)
        #         # print(object_summary.key)
        # else:
        #     for object_summary in bucket.objects.all():
        #         all_object_files.append(object_summary.key)

        # return all_object_files