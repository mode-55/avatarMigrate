import boto3

s3_client = boto3.client('s3')

def validate_bucket(bucket_name):
    try:
        waiter = s3_client.get_waiter('bucket_exists')
        waiter.wait(
            Bucket=bucket_name,
            WaiterConfig={
                'Delay': 1,
                'MaxAttempts': 2
            }
        )
        return bucket_name
    except boto3.exceptions.botocore.waiter.WaiterError as error :
        return "Bucket DOES NOT exist!!"


def get_source_bucket_avatars():
    pass