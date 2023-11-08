# menu.py
import sys
from publisher_dao import add_publisher
from book_dao import add_book, edit_book, delete_book, user_search, system_search

# main menu, to be displayed on system startup and after any successful or failed operation
def print_main_menu():
    print("")
    print("-" * 40 + "Book Manager Software" + "-" * 40)
    menu_options = {
        1: 'Add a Publisher',
        2: 'Add a Book',
        3: 'Edit a Book',
        4: 'Delete a Book',
        5: 'Search Books',
        6: 'Exit'
    }
    for key, value in menu_options.items():
        print(f"{key}. {value}")
    print("Please select a function, type [1 - 6] and press enter: ", end="")

# UI to be displayed when user selects Add a Publisher
def add_publisher_ui():
    print("")
    print("Enter the publisher's details:")
    name = input("Name: ")
    phone = input("Phone: ")
    city = input("City: ")
    if add_publisher(name, phone, city):
        print("Publisher added successfully.")
    else:
        print("Failed to add publisher.")

# UI to be displayed when Adding a Book
def add_book_ui():
    print("")
    print("Enter the book's details:")
    isbn = input("ISBN: ")
    title = input("Title: ")
    year = input("Year: ")
    published_by = input("Published by (Publisher Name): ")
    previous_edition = input("Previous Edition ISBN: ")
    price = input("Price: ")
    if add_book(isbn, title, year, published_by, previous_edition, price):
        print("Book added successfully.")
    else:
        print("Failed to add book.")

# UI to be displayed when Editing a Book
def edit_book_ui():
    print("")
    print("Enter the ISBN of the book to edit:")
    isbn = input("ISBN: ")
    # First, find the book by ISBN
    books_to_edit = system_search(ISBN=isbn)
    if books_to_edit:

        # if more than one is somehow selected (shouldn't be possible) select the first
        book_to_edit = books_to_edit[0]

        # Assuming that the book_to_edit variable contains the details of the book as a dictionary
        print(f"Editing book: {book_to_edit[1]} by {book_to_edit[3]}")

        print("What detail would you like to edit?")
        print("1. Title")
        print("2. Year")
        print("3. Publisher")
        print("4. Previous Edition")
        print("5. Price")
        choice = input("Select an option [1-5]: ")

        # the choice will be passed to edit_book so that it can select the correct column
        if choice == '1':
            new_title = input("Enter the new title: ")
            edit_book(isbn, choice, new_title)
        elif choice == '2':
            new_year = input("Enter the new year: ")
            edit_book(isbn, choice, new_year)
        elif choice == '3':
            new_publisher = input("Enter the new publisher name: ")
            edit_book(isbn, choice, new_publisher)
        elif choice == '4':
            new_prev_edition = input("Enter the new previous edition ISBN: ")
            edit_book(isbn, choice, new_prev_edition)
        elif choice == '5':
            new_price = input("Enter the new price: ")
            edit_book(isbn, choice, new_price)
        else:
            print("Invalid choice.")
    else:
        print("Book not found")

# UI to be displayed when deleting books. Can only be deleted by ISBN
def delete_book_ui():
    print("")
    print("Enter the ISBN of the book to delete:")
    isbn = input("ISBN: ")
    if delete_book(isbn):
        print("Book deleted successfully.")  

# Rather than displaying the UI here in menu.py, this passes to book_dao.py as there were a lot of else-if statements required
def search_books_ui():
    print("")
    print(user_search())

def main():
    while True:
        print_main_menu()
        try:
            option = int(input())
            if option == 1:
                add_publisher_ui()
            elif option == 2:
                add_book_ui()
            elif option == 3:
                edit_book_ui()
            elif option == 4:
                delete_book_ui()
            elif option == 5:
                search_books_ui()
            elif option == 6:
                print("Exiting the Book Manager Software. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user. Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()
