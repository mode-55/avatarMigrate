import boto3
import botocore

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
                        waiter = s3_client.get_waiter('object_exists')
                        waiter.wait(Bucket=source_bucket, Key=object_key)
                        copy_source = {'Bucket': source_bucket, 'Key': object_key}
                        target_object_key = 'avatar/' + object_key.split('/')[1]
                        s3_client.copy_object(Bucket=target_bucket, Key=target_object_key, CopySource=copy_source)
                        waiter.wait(Bucket=target_bucket, Key=target_object_key)
                        copy_event_log += target_object_key + ' Found in ' + target_bucket + '\n'

                    except botocore.exceptions.ClientError as error:
                        raise error
                    except botocore.exceptions.ParamValidationError as error:
                        raise ValueError('The parameters you provided are incorrect: {}'.format(error))
                print(copy_event_log)

            except KeyError:
                break
    
