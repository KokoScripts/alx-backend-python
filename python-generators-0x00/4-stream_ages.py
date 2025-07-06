import mysql.connector
from mysql.connector import Error

# --- Database Configuration (Updated with your details) ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'kokoscripts',
    'password': 'your_actual_password', # IMPORTANT: Replace with your actual password
    'database': 'ALX_prodev'
}

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    Returns a connection object to ALX_prodev if successful, None otherwise.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        if conn.is_connected():
            pass # Suppress connection message for cleaner output
        return conn
    except Error as e:
        print(f"Error connecting to database '{DB_CONFIG['database']}': {e}")
        return None

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the 'user_data' table.

    Args:
        page_size (int): The maximum number of rows to retrieve for the page.
        offset (int): The starting offset for fetching rows.

    Returns:
        list: A list of dictionaries, where each dictionary represents a user row.
              Returns an empty list if no users are found for the given page/offset,
              or if a database error occurs.
    """
    conn = None
    cursor = None
    users_on_page = []
    try:
        conn = connect_to_prodev()
        if conn:
            cursor = conn.cursor(dictionary=True) # Get rows as dictionaries
            # SQL query to fetch a page of users using LIMIT and OFFSET
            query = f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset};"
            cursor.execute(query)
            users_on_page = cursor.fetchall() # Fetch all results for the current page
    except Error as e:
        print(f"Error fetching page (size={page_size}, offset={offset}): {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return users_on_page

def lazy_paginate(page_size):
    """
    A generator function that lazily fetches and yields individual user rows
    from the 'user_data' table in pages. It only fetches the next page when
    all users from the current page have been yielded.

    This function adheres to the "no more than 1 loop" constraint for its
    primary pagination control.

    Args:
        page_size (int): The number of users to fetch per page.

    Yields:
        dict: A dictionary representing a single user row.
    """
    offset = 0
    # This is the single primary loop controlling the pagination logic.
    while True:
        # Fetch the current page of users
        current_page_users = paginate_users(page_size, offset)

        # If the page is empty, it means there are no more users to fetch.
        if not current_page_users:
            break

        # Iterate through the users in the current page and yield each one.
        # This inner loop processes the elements of the *current* fetched page.
        for user in current_page_users:
            yield user

        # Increment the offset to prepare for fetching the next page
        offset += page_size

# --- Example Usage ---
if __name__ == "__main__":
    print("Lazily paginating users:")
    my_page_size = 3 # Define how many users per page

    user_counter = 0
    try:
        # Iterate through the users yielded by the lazy_paginate generator
        for user in lazy_paginate(my_page_size):
            user_counter += 1
            print(f"User {user_counter}: Name: {user['name']}, Age: {user['age']}, Email: {user['email']}")
            # Optional: Break early for testing large datasets
            # if user_counter >= 10:
            #     print("\nStopped after 10 users for demonstration purposes.")
            #     break
    except Exception as e:
        print(f"An error occurred during lazy pagination: {e}")
    finally:
        print(f"\nFinished lazy pagination. Total users yielded: {user_counter}")

