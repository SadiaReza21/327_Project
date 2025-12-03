from model.database import Database

class Admin:
    """
    Model class for admin-related database operations.
    """
    def __init__(self):
        self.db = Database()

    def authenticate(self, email, password):
        """
        Authenticate an admin using email and password.

        Connects to the database and checks if an admin record exists
        with the given email and password. Returns True if authentication
        is successful, otherwise False.

        Args:
            email (str): Admin's email address.
            password (str): Admin's password in plaintext.

        Returns:
            bool: 
                - ``True`` if the admin is authenticated.
                - ``False`` if authentication fails or an error occurs.
        """
        
        connection = self.db.connect()
        if not connection:
            return False

        try:
            cursor = connection.cursor(dictionary=True)

            sql = "SELECT * FROM admins WHERE email = %s AND password = %s"
            cursor.execute(sql, (email, password))
            admin = cursor.fetchone()

            cursor.close()
            connection.close()

            if admin:
                return True
            return False

        except Exception as e:
            print("Authentication Error:", e)
            return False

        finally:
            cursor.close()
            connection.close()
