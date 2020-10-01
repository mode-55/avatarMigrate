import os
import pytest
from avatarMigrate import cli
# This is what we want to achieve :  
# `$ avatarMigrate [source_bucket] [target_bucket] [database_url] [database_username] [database_password]`


source_bucket = os.getenv("SOURCE_BUCKET")
target_bucket = os.getenv("TARGET_BUCKET")
database_url = os.getenv("DATABASE_URL")
database_username = os.getenv("DATABASE_USERNAME")
database_password = os.getenv("DATABASE_PASSWORD")

@pytest.fixture
def parser():
    return cli.create_parser()

def test_parser_without_source_bucket(parser):
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_parser_without_target_bucket(parser):
    with pytest.raises(SystemExit):
        parser.parse_args([source_bucket])

def test_parser_with_source_target_bucket(parser):
    args = parser.parse_args([source_bucket,target_bucket])
    assert args.source_bucket == source_bucket
    assert args.target_bucket == target_bucket

