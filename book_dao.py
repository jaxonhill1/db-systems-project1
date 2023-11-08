# book_dao.py

from mysql_connector import create_connection
from mysql.connector import IntegrityError
from utils import verify_fields

def add_book(isbn, title, year, published_by, previous_edition, price):
    connection = create_connection()
    if connection is None:
        return False
    
    # verify that the fields are not empty
    if verify_fields(isbn, title, year, published_by, previous_edition, price) == False:
        print("One or more of the fields are empty.")
        return False

    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO Book (ISBN, title, year, published_by, previous_edition, price)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (isbn, title, year, published_by, previous_edition, price))
        connection.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        connection.close()

def query_user():
    print("Please select the column you want to search by:")
    print("1. ISBN")
    print("2. Title")
    print("3. Year")
    print("4. Published by (Publisher Name)")
    print("5. Price")
    column_choice = input("Enter the number of your choice: ")
    column_map = {
        '1': 'ISBN',
        '2': 'title',
        '3': 'year',
        '4': 'published_by',
        '5': 'price'
    }
    return column_map.get(column_choice, None)

def user_search():

    print("Choose the search criteria:")
    print("1. All books")
    print("2. By title")
    print("3. By ISBN")
    print("4. By publisher")
    print("5. By price range")
    print("6. By year")
    print("7. By title and publisher")
    choice = input("Enter an option [1-7]: ")
    
    try:
        if choice == '1':
            return system_search()
        elif choice == '2':
            booktitle = input('Enter the title of the book: ')
            return system_search(title=booktitle)
        elif choice == '3':
            bookISBN = input('Enter the ISBN of the book: ')
            return system_search(ISBN=bookISBN)
        elif choice == '4':
            bookpublisher = input('Enter the name of the publisher: ')
            return system_search(publisher=bookpublisher)
        elif choice == '5':
            min_price = float(input("Enter minimum price: "))
            max_price = float(input("Enter maximum price: "))
            return system_search(min_price=min_price, max_price=max_price)
        elif choice == '6':
            bookYear = int(input('Enter the year the book was published: '))
            return system_search(year=bookYear)
        elif choice == '7':
            title = input("Enter title: ")
            publisher = input("Enter publisher: ")
            return system_search(title=title, publisher=publisher)
        else:
            print("Invalid choice.")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def system_search(ISBN=None, min_price=None, max_price=None, title=None, publisher=None, year=None):
    connection = create_connection()
    if connection is None:
        return False
    try:
        with connection.cursor() as cursor:
            if ISBN:
                query = "SELECT * FROM Book WHERE ISBN = %s"
                cursor.execute(query, (ISBN,))
            elif year:
                query = "SELECT * FROM Book WHERE year = %s"
                cursor.execute(query, (year,))
            elif min_price is not None and max_price is not None:
                query = "SELECT * FROM Book WHERE price BETWEEN %s AND %s"
                cursor.execute(query, (min_price, max_price))
            elif title and publisher:
                query = "SELECT * FROM Book WHERE title = %s AND published_by = %s"
                cursor.execute(query, (title, publisher))
            elif title:
                query = "SELECT * FROM Book WHERE title = %s"
                cursor.execute(query, (title,))
            elif publisher:
                query = "SELECT * FROM Book WHERE published_by = %s"
                cursor.execute(query, (publisher,))
            else:
                query = "SELECT * FROM Book"
                cursor.execute(query)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def edit_book(isbn, column_choice, new_value):
    # Map the user's choice to the actual column name in the database
    column_map = {
        '1': 'title',
        '2': 'year',
        '3': 'published_by',
        '4': 'previous_edition',
        '5': 'price'
    }

    # Get the actual column name from the map using the choice provided
    column_name = column_map.get(column_choice)

    # If the column name is not in the map, print an error and return
    if column_name is None:
        print("Invalid column choice.")
        return False

    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        with connection.cursor() as cursor:
            # Update query where we use the column name in the SQL query
            query = f"UPDATE Book SET {column_name} = %s WHERE ISBN = %s"
            # Execute the query passing in the new value and the ISBN
            cursor.execute(query, (new_value, isbn))
            connection.commit()
            print(f"Book with ISBN {isbn} updated successfully in column {column_name}.")
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        connection.close()

def delete_book(bookISBN):
    connection = create_connection()
    if connection is None:
        return False
    try:
        books = system_search(ISBN=bookISBN)
        if len(books) == 1:
            book = books[0]
            isbn = book[0]
            with connection.cursor() as cursor:
                query = "DELETE FROM Book WHERE ISBN = %s"
                cursor.execute(query, (isbn,))
                connection.commit()
                print("Book deleted successfully.")
        elif not books:
            print("No books found to delete.")
        else:
            print("Multiple books found, please refine your search.")
    except IntegrityError as e:
        print("Cannot delete this book because it is referenced by another record. Please delete the dependent records first.") 
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        connection.close()
