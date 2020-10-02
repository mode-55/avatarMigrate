import boto3
import botocore
import sys
from avatarMigrate import rds

s3_client = boto3.client('s3')

def bucket_exists(bucket):
    s3 = boto3.resource('s3')
    if(s3.Bucket(bucket) in s3.buckets.all()):
        return True
    else:
        print('%s bucket DOES NOT exist!' % bucket)


def migrate_objects(source_bucket,target_bucket):
    if(bucket_exists(source_bucket) and bucket_exists(target_bucket)):
        paginator = s3_client.get_paginator('list_objects_v2')
        kwargs = {
            'Bucket': source_bucket,
            'Prefix':'image/avatar-',
            'PaginationConfig':{
                'MaxItems': 100,
                'PageSize': 4,
                }
            }

        pages = paginator.paginate(**kwargs)
        copy_event_log = ""
        for page in pages:
            try:
                contents = page["Contents"]
                for source_bucket_object in contents:
                    object_key = source_bucket_object['Key']
                    try:
                        print ("Waiting for object to persist through s3 service")
                        #Implement waiter to ensure the object is in the bucket
                        waiter = s3_client.get_waiter('object_exists')
                        waiter.wait(Bucket=source_bucket, Key=object_key)
                        copy_source = {'Bucket': source_bucket, 'Key': object_key}
                        target_object_key = 'avatar/' + object_key.split('/')[1]
                        #copy object from source to target
                        s3_client.copy_object(Bucket=target_bucket, Key=target_object_key, CopySource=copy_source)
                        #Add waiter to ensure the object is in the target bucket before updating the log. 
                        waiter.wait(Bucket=target_bucket, Key=target_object_key)
                        #keep a log to send to cloudwatch
                        copy_event_log += target_object_key + ' Found in ' + target_bucket + '\n'
                        #Build Mysql statement to update only the object that have been copied. 
                        sql = 'UPDATE test.avatar set url = "'+target_object_key+'" WHERE url = "'+object_key+'";\n'
                        rds.create_sql_update_file(sql)

                    except botocore.exceptions.ClientError as error:
                        raise error
                    except botocore.exceptions.ParamValidationError as error:
                        raise ValueError('The parameters you provided are incorrect: {}'.format(error))
                print(copy_event_log)
                return True
            except KeyError:
                break
    

