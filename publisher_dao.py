# publisher_dao.py

from mysql_connector import create_connection
from utils import verify_fields

def add_publisher(name, phone, city):
    
    connection = create_connection()
    if connection is None:
        return False
    
    # verify that all fields were entered correctly (non empty)
    if verify_fields(name, phone, city) == False:
        print("One or more of the input fields are empty.")
        return False
    
    # try to execute an INSERT command with the provided data
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Publisher (name, phone, city) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, phone, city))
        connection.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        connection.close()
