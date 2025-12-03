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

