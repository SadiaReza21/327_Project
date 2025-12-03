import mysql.connector

class Database:
    """
    Handles database connection for this application.
    """
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "bazar_kori"
    
    def connect(self):
        """
        Creates a connection to the MySQL database.

        Attempts to connect using the host, username, password,
        and database name. If successful, returns a MySQL connection object.
        If the connection fails, logs the error and returns None.

        Returns:
            mysql.connector.connection.MySQLConnection or None:
                - A valid MySQL connection object if the connection succeeds.
                - ``None`` if the connection fails.
        """
        try:
            connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            return connection
        except Exception as e:
            print(f"Error: {e}")
            return None