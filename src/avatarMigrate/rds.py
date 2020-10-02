
import mysql.connector
import sys
import boto3
import os

ENDPOINT="avatar-1.conzzjannagu.eu-west-2.rds.amazonaws.com"
PORT="3306"
USR="admin"
REGION="eu-west-2"
DBNAME=""
DBPASSWORD="PassWord101"

def update_database():
    try:
        conn =  mysql.connector.connect(host=ENDPOINT, user=USR, passwd=DBPASSWORD, port=PORT, database=DBNAME)
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e))          



def create_sql_update_file(statement):
    # Open a file with access mode 'a'
    file_object = open('sql_update.sql', 'a')
    # Append statement from log at the end of file
    file_object.write(statement)
    # Close the file
    file_object.close()