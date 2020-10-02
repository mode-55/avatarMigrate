import pytest 
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from avatarMigrate import rds


def test_db_connect():
    pass