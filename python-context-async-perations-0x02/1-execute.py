import sqlite3

class ExecuteQuery:
    """
    Custom context manager for executing SQL queries.
    Manages connection setup and teardown, and returns results.
    """

    def __init__(self, db_path, query, params=None):
        self.db_path = db_path
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    db_path = "my_database.db"
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(db_path, query, params) as result:
        print(result)
