import mysql.connector
from mysql.connector import Error

# --- Database Configuration (Using your provided details) ---
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

def stream_user_ages():
    """
    A generator function that fetches user ages one by one from the user_data table.
    It connects to the ALX_prodev database and yields each age.
    Ensures that the database connection and cursor are properly closed.
    This function uses no more than 1 loop for its core logic.

    Yields:
        float or decimal: The age of a user.
    """
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if conn:
            cursor = conn.cursor(dictionary=True) # Use dictionary=True to access 'age' by name
            query = "SELECT age FROM user_data;"
            cursor.execute(query)

            # The single loop for yielding ages
            for row in cursor:
                yield row['age']
        else:
            print("Could not establish database connection for streaming ages.")
    except Error as e:
        print(f"Error during user age streaming: {e}")
    finally:
        # Ensure cursor and connection are closed even if an error occurs
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def calculate_average_age():
    """
    Calculates the average age of users by consuming the stream_user_ages generator
    without loading the entire dataset into memory.

    Returns:
        float: The average age, or 0.0 if no ages are found.
    """
    total_age = 0.0
    count = 0

    # Consume the generator to get ages one by one
    for age in stream_user_ages():
        total_age += float(age) # Ensure age is treated as a float for calculation
        count += 1

    return total_age / count if count > 0 else 0.0

# --- Example Usage ---
if __name__ == "__main__":
    print("Streaming user ages from the database:")
    age_count = 0
    try:
        for age in stream_user_ages():
            print(f"User Age: {age}")
            age_count += 1
            # Optional: Add a break to limit output for testing large datasets
            # if age_count >= 10:
            #     print("Stopped after 10 ages for demonstration purposes.")
            #     break
    except Exception as e:
        print(f"An error occurred during age streaming: {e}")
    finally:
        print(f"\nFinished streaming ages. Total ages processed: {age_count}")

    print("\n--- Calculating Average Age ---")
    try:
        avg_age = calculate_average_age()
        if avg_age > 0:
            print(f"The average age of users is: {avg_age:.2f}")
        else:
            print("No users found to calculate average age.")
    except Exception as e:
        print(f"An error occurred while calculating average age: {e}")

