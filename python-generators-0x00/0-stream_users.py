import mysql.connector
from mysql.connector import Error

# --- Database Configuration ---
# IMPORTANT: Replace with your MySQL server details
# These should match the credentials used when populating the database
DB_CONFIG = {
    'host': '127.0.0.1',  
    'user': 'kokoscripts',  
    'password': '************', 
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
            # print(f"Successfully connected to database '{DB_CONFIG['database']}'.")
            pass # Suppress connection message for cleaner generator output
        return conn
    except Error as e:
        print(f"Error connecting to database '{DB_CONFIG['database']}': {e}")
        return None

def stream_users():
    """
    A generator function that fetches rows one by one from the user_data table.
    It connects to the ALX_prodev database and yields each row.
    Ensures that the database connection and cursor are properly closed.
    """
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if conn:
            cursor = conn.cursor(dictionary=True) # Use dictionary=True to get rows as dictionaries
            query = "SELECT user_id, name, email, age FROM user_data;"
            cursor.execute(query)

            # The single loop for yielding rows
            for row in cursor:
                yield row
        else:
            print("Could not establish database connection for streaming.")
    except Error as e:
        print(f"Error during user data streaming: {e}")
    finally:
        # Ensure cursor and connection are closed even if an error occurs
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            # print("Database connection closed after streaming.")


# --- Example Usage ---
if __name__ == "__main__":
    print("Streaming users from the database:")
    user_count = 0
    try:
        for user in stream_users():
            print(f"User ID: {user['user_id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}")
            user_count += 1
            # Optional: Add a break to limit output for testing large datasets
            # if user_count >= 10:
            #     print("Stopped after 10 users for demonstration purposes.")
            #     break
    except Exception as e:
        print(f"An error occurred during streaming: {e}")
    finally:
        print(f"\nFinished streaming. Total users processed: {user_count}")

