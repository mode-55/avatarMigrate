import mysql.connector
import sys
import boto3
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def update_database():
    try:
        sql_file = open("sql_update.sql")
        sql_as_string = sql_file.read()
    except IOError:
      print ("Error: sql_update.sql file does not appear to exist in current directory.")
      return 0
    try:
        conn =  mysql.connector.connect(
            host=os.getenv("DATABASE_URL"), 
            user=os.getenv("DATABASE_USERNAME"), 
            passwd=os.getenv("DATABASE_PASSWORD"), 
            port="3306", 
            database=os.getenv("DATABASE_NAME"))

        cursor = conn.cursor()
        for result in cursor.execute(sql_as_string, multi=True):
            if result.with_rows:
                print("Rows produced by statement '{}':".format(result.statement))
                print(result.fetchall())
            else:
                print("Number of rows affected by statement '{}': {}".format(
                result.statement, result.rowcount))
            #commit update     
        conn.commit()
        conn.close()

    except Exception as e:
        print("Database connection failed due to {}".format(e))          



def create_sql_update_file(statement):
    # Open a file with access mode 'a'
    file_object = open('sql_update.sql', 'a')
    # Append statement from log at the end of file
    file_object.write(statement)
    # Close the file
    file_object.close()