# mysql_connector.py

import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        # connect to the locally hosted MySQL instance with default user and password.
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='password',
            database='bookmanager'
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred when connecting to the database")
        return None