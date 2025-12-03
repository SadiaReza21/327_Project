from database_connection import get_db_connection
from mysql.connector import Error
from typing import List, Dict, Any
from datetime import date, datetime

class Product:


    def __init__(
            self, product_id: int , category_id: int , name: str , 
            description: str, price: float, stock: int, 
            image: str, date_added: date, is_available: bool, 
            is_archived: bool):
        self.product_id: int = product_id
        self.category_id: int = category_id
        self.name: str = name
        self.description: str = description or ""
        self.price: float = price
        self.stock: int = stock
        self.image_url: str = image
        self.date_added: date = date_added
        self.is_available: bool = is_available
        self.is_archived:bool = is_archived


    @staticmethod
    def create_product(product: "Product") -> bool:
        """
        Insert a new product's information in the database.

        Args:
            product (Product): A product object holding the new 
            product's information.

        Returns:
            bool: True if insertion was successfull and False otherwise.
        """
        conn = None
        cursor = None
        try:
            if (product.product_id == None or product.name == "" or 
                product.stock == None or product.price == None or 
                product.category_id == None or product.image_url == ""):
                raise ValueError("Required information is not filled!")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                sql = """
                    INSERT INTO products 
                    (product_id, category_id, name, description, price, stock, 
                    image_url, date_added, is_available, is_archived)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    product.product_id, product.category_id, product.name,
                    product.description, product.price, product.stock,
                    product.image_url, product.date_added, product.is_available,
                    product.is_archived
                )
                cursor.execute(sql, values)
                conn.commit()
                return True
        except Error as e:
            print(f"Error creating product: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()


    @staticmethod
    def update_product(product: "Product") -> bool:
        """
        Updates product's information in the database.

        Args:
            product (Product): A product object holding the product's 
            new information.

        Returns:
            bool: True if update was successfull and False otherwise.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                UPDATE products SET
                category_id = %s, name = %s, description = %s, price = %s, 
                stock = %s, image_url = %s, date_added = %s, 
                is_available = %s, is_archived = %s 
                WHERE product_id = %s
            """
            values = (                
                product.category_id, product.name, product.description,
                product.price, product.stock, product.image_url,
                product.date_added, product.is_available, product.is_archived,
                product.product_id
            )
            cursor.execute(sql, values)
            conn.commit()
            return True

        except Error as e:
            print(f"Error updating product: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()


    @staticmethod
    def delete_product(product_id: str) -> bool:
        """
        Delete product's information from the database.

        Args:
            product_id (str): The id of the product that needs to be deleted.

        Returns:
            bool: True if deletion was successfull and False otherwise.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "DELETE from products WHERE product_id = %s"
            value = (product_id,)
            cursor.execute(sql, value)
            conn.commit()
            return True

        except Error as e:
            print(f"Error deleting product: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()


    @staticmethod
    def get_product(product_id: str) -> "Product":
        """
        Returns a product object for a specific product_id.

        Args:
            product_id (str): Product id of the desired product.

        Returns:
            Product: A product object holding that desired product's
            information, fetched form the database.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM products WHERE product_id = %s"
            value =(product_id,)
            cursor.execute(sql,value)
            row = cursor.fetchone()

            if row is None:
                return None
            
            new_product = Product(
                row["product_id"], row["category_id"], 
                row["name"], row["description"], row["price"], row["stock"],
                row["image_url"], row["date_added"], row["is_available"], 
                row["is_archived"]) 
            return new_product
            
        except Error as e:
            print(f"Could not get product: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    

    @staticmethod
    def get_unarchived_product_list() -> List["Product"]:
        """
        Returns a list of product objects which are unarchived.       

        Returns:
            List: List of product objects that are not archived,
            fetched from database.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM products WHERE is_archived = False"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                #Creating product objects for each row fetched for database
                new_product = Product(
                    row["product_id"], row["category_id"], row["name"], 
                    row["description"], row["price"], row["stock"], 
                    row["image_url"], row["date_added"], row["is_available"],
                    row["is_archived"]) 
                result.append(new_product)
            return result
            
        except Error as e:
            print(f"Getting product list failed: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    

    @staticmethod
    def get_archived_product_list() -> List["Product"]:
        """
        Returns a list of product objects which are archived.       

        Returns:
            List: List of product objects that are archived, fetched from 
            database by left joining products and archived table.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT archived.product_id AS p_id, products.category_id, 
                products.name, products.description, products.price, 
                archived.stock, products.image_url, products.date_added, 
                products.is_available, products.is_archived FROM archived 
                LEFT JOIN products 
                ON archived.product_id = products.product_id
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                #Creating product objects for each row fetched for database
                new_product = Product(
                    row["p_id"], row["category_id"], row["name"], 
                    row["description"], row["price"], row["stock"], 
                    row["image_url"], row["date_added"], row["is_available"], 
                    row["is_archived"]) 
                result.append(new_product)
            return result
            
        except Error as e:
            print(f"Getting archived product list failed: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()


    @staticmethod
    def archive_product(product_id: str) -> bool:
        """
        Archives a product by changing is_archived value to True in 
        product table and adding that product to archived table in database.       

        Args:
            product_id (str): The product's id that needs to be archived.

        Returns:
            bool: True if archiving is successfull, False otherwise.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                UPDATE products SET is_archived = True, stock = 0 WHERE product_id = %s
            """    
            value = (product_id,)   
            cursor.execute(sql, value)
            #Getting the product of that id to fetch it's name
            prod = Product.get_product(product_id)
            # Make stock 0 for archived product table, later stock quantity 
            sql = "INSERT INTO archived (product_id, stock, name, is_archived) VALUES (%s, %s, %s, %s)"    
            value = (product_id, 0, prod.name, True)   
            cursor.execute(sql, value)
            conn.commit()
            return True

        except Error as e:
            print(f"Error archiving product: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()


    @staticmethod
    def unarchive_product(product_id: str) -> bool:
        """
        Unarchives a product by changing is_archived value to False in 
        product table and deleting that product from archived table.       

        Args:
            product_id (str): The product's id that needs to be unarchived.

        Returns:
            bool: True if unarchiving is successfull, False otherwise.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                UPDATE products SET is_archived = False WHERE product_id = %s
            """    
            value = (product_id,)   
            cursor.execute(sql, value)
            sql = "DELETE from archived WHERE product_id = %s"    
            value = (product_id,)   
            cursor.execute(sql, value)
            conn.commit()
            return True

        except Error as e:
            print(f"Error unarchiving product: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()