import mysql.connector
from mysql.connector import Error

# --- Database Configuration (Updated with your details) ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'kokoscripts',
    'password': 'your_actual_password', # Replace with your actual password
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
            pass # Suppress connection message for cleaner generator output
        return conn
    except Error as e:
        print(f"Error connecting to database '{DB_CONFIG['database']}': {e}")
        return None

def stream_users_in_batches(batch_size):
    """
    A generator function that fetches rows from the user_data table in batches.
    It connects to the ALX_prodev database and yields lists of user dictionaries.
    Ensures that the database connection and cursor are properly closed.

    Args:
        batch_size (int): The number of rows to include in each batch.
    """
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if conn:
            # Use buffered=True to fetch all results into memory if necessary,
            # or use unbuffered=True for very large datasets where memory is a concern.
            # For simplicity and to fit the single loop per function, we'll use buffered.
            # If unbuffered is used, the cursor itself acts as the generator.
            cursor = conn.cursor(dictionary=True)
            query = "SELECT user_id, name, email, age FROM user_data;"
            cursor.execute(query)

            batch = []
            # Loop 1: Iterates through all rows fetched by the cursor
            for row in cursor:
                batch.append(row)
                if len(batch) >= batch_size:
                    yield batch
                    batch = [] # Reset batch after yielding

            # Yield any remaining rows that didn't form a full batch
            if batch:
                yield batch
        else:
            print("Could not establish database connection for streaming batches.")
    except Error as e:
        print(f"Error during batch streaming: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def batch_processing(batch_size):
    """
    A generator function that processes batches of users to filter those
    over the age of 25. It uses stream_users_in_batches to get the data.

    Args:
        batch_size (int): The size of batches to fetch from the database.
    """
    # Loop 2: Iterates through batches yielded by stream_users_in_batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Iterates through users within the current batch
        for user in batch:
            if user['age'] > 25:
                yield user

# --- Example Usage ---
if __name__ == "__main__":
    print("Processing users over the age of 25 in batches:")
    processed_user_count = 0
    try:
        # Define your desired batch size
        my_batch_size = 5

        # Iterate through the filtered users using the batch_processing generator
        for user in batch_processing(my_batch_size):
            print(f"Filtered User: Name: {user['name']}, Age: {user['age']}, Email: {user['email']}")
            processed_user_count += 1
            # Optional: Add a break to limit output for testing
            # if processed_user_count >= 10:
            #     print("Stopped after processing 10 filtered users for demonstration.")
            #     break
    except Exception as e:
        print(f"An error occurred during batch processing: {e}")
    finally:
        print(f"\nFinished batch processing. Total filtered users: {processed_user_count}")

