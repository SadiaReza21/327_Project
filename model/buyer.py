from model.database import Database


class Buyer:
    """
    Model class for buyer-related database operations.
    """
    def __init__(self):
        self.db = Database()

    def signup(self, name, phone, email, password):
        """
        Register a new buyer.

        Checks whether the email already exists, and if not, inserts a new
        buyer record into the database.

        Args:
            name (str): Buyer's full name.
            phone (str): Buyer's phone number.
            email (str): Buyer's email address.
            password (str): Buyer's password in plaintext.

        Returns:
            dict: A dictionary containing:
                - ``status`` (str): "success" or "error".
                - ``message`` (str): Description of the signup result.
        """
        
        connection = self.db.connect()
        if not connection:
            return False

        try:
            cursor = connection.cursor()

            sql_1 = "SELECT id FROM buyers WHERE email = %s"
            cursor.execute(sql_1, (email,))
            existing = cursor.fetchone()

            if existing:
                return {"status": "error", "message": "Email is already registered"}

            sql_2 = """
                INSERT INTO buyers (name, phone, email, password)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_2, (name, phone, email, password))
            connection.commit()

            return {"status": "success", "message": "Buyer registered successfully"}

        except Exception as e:
            print("Signup Error:", e)
            return {"status": "error", "message": "Signup failed"}

        finally:
            cursor.close()
            connection.close()


    def authenticate(self, email, password):
        """
        Authenticate a buyer with email and password.

        Verifies the buyer's credentials against the database and returns
        the buyer's ID and email if authentication is successful.

        Args:
        email (str): Buyer's email address.
        password (str): Buyer's password in plaintext.

        Returns:
          dict: A dictionary containing:
            - ``success`` (bool): True if authentication succeeds, False otherwise.
            - ``id`` (int): Buyer's ID (only if success is True).
            - ``email`` (str): Buyer's email (only if success is True).

    
        """
        connection = self.db.connect()
        if not connection:
            return False

        try:
            cursor = connection.cursor(dictionary=True)

            sql_3 = "SELECT * FROM buyers WHERE email = %s AND password = %s"
            cursor.execute(sql_3, (email, password))
            buyer = cursor.fetchone()

            if buyer:
               return {"success": True, "id": buyer["id"], "email": buyer["email"]}
            return {"success": False}

        except Exception as e:
            print("Authentication Error:", e)
            return False

        finally:
            cursor.close()
            connection.close()

    def get_buyer(self, id): 
        """
        Retrieve buyer information by ID.

        Fetches the buyer's profile details (name, phone, email) from
        the database using their unique ID.

        Args:
            id (int): Buyer's unique identifier.

        Returns:
            dict: A dictionary containing:
                - ``name`` (str): Buyer's full name.
                - ``phone`` (str): Buyer's phone number.
                - ``email`` (str): Buyer's email address.
            
            Or on error:
                - ``status`` (str): "error".
                - ``message`` (str): Error description.

        """
        connection = self.db.connect()
        if not connection:
            return False

        try:
            cursor = connection.cursor(dictionary=True)

            sql_1 = "SELECT * from buyers WHERE id = %s"
            cursor.execute(sql_1, (id,))
            buyer = cursor.fetchone()

            return {"name" : buyer["name"], "phone" : buyer["phone"], "email": buyer["email"]}

        except Exception as e:
            print("Fetch Error:", e)
            return {"status": "error", "message": "Fetch failed"}

        finally:
            cursor.close()
            connection.close()

    def edit_profile(self, id, name, phone):
        """
         Update a buyer's profile information.

        Updates the name and phone number for a buyer identified by
        their unique ID.

        Args:
            id (int): Buyer's unique identifier.
            name (str): New name for the buyer.
            phone (str): New phone number for the buyer.

        Returns:
            dict: A dictionary containing:
                - ``status`` (str): "success" or "error".
                - ``message`` (str): Description of the update result.

        """
            
        connection = self.db.connect()
        if not connection:
            return False

        try:
            cursor = connection.cursor()

            sql_1 = "UPDATE buyers SET name = %s, phone = %s WHERE id = %s"
            cursor.execute(sql_1, (name, phone, id))
            connection.commit()

            return {"status": "success", "message": "Buyer information updated successfully"}

        except Exception as e:
            print("Update Error:", e)
            return {"status": "error", "message": "Update failed"}

        finally:
            cursor.close()
            connection.close()

