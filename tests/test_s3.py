import pytest 
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from avatarMigrate import s3


def test_buckets_exists():
    buckets = [os.getenv("SOURCE_BUCKET"),os.getenv("TARGET_BUCKET")]
    for bucket in buckets:
        response = s3.bucket_exists(bucket)
        assert response == True

def test_migrate_objects():
    s3.migrate_objects(os.getenv("SOURCE_BUCKET"),os.getenv("TARGET_BUCKET"))


