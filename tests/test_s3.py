import pytest 
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from avatarMigrate import s3


def test_buckets_exists():
    buckets = [os.getenv("SOURCE_BUCKET"),os.getenv("TARGET_BUCKET")]
    for bucket in buckets:
        bucket_name = s3.validate_bucket(bucket)
        assert bucket == bucket_name

def test_list_source_bucket_objects():
    pass


