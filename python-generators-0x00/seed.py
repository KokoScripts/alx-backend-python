import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'kokoscripts',
    'password': 'mmekekon98...', # Added a comma here
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
            print(f"Successfully connected to database '{DB_CONFIG['database']}'.")
        return conn
    except Error as e:
        print(f"Error connecting to database '{DB_CONFIG['database']}': {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    db_connection = connect_to_prodev()

    if db_connection:
        print("You are now connected to the ALX_prodev database.")
        # You can perform database operations here, e.g., fetching data
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT user_id, name, email, age FROM user_data LIMIT 5;")
            records = cursor.fetchall()
            print("\nFirst 5 records from user_data table:")
            for row in records:
                print(f"User ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Age: {row[3]}")
            cursor.close()
        except Error as e:
            print(f"Error fetching data: {e}")
        finally:
            db_connection.close()
            print("Database connection closed.")
    else:
        print("Failed to establish a connection to the ALX_prodev database.")
