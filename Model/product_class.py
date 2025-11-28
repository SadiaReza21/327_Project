from database_connection import get_db_connection
from mysql.connector import Error
from typing import List, Dict, Any
from datetime import date, datetime

class Product:

    def __init__(
            self, product_id: int , category_id: int , name: str , description: str, price: float, stock: int, 
            image: str, date_added: date, is_available: bool, is_archived: bool):
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
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                INSERT INTO product 
                (product_id, category_id, name, description, price, stock, image_url, date_added, is_available, is_archived)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                product.product_id,
                product.category_id,
                product.name,
                product.description,
                product.price,
                product.stock,
                product.image_url,
                product.date_added,
                product.is_available,
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
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                UPDATE product SET
                category_id = %s, name = %s, description = %s, price = %s, stock = %s, image_url = %s, date_added = %s, is_available = %s, is_archived = %s 
                WHERE product_id = %s
            """
            values = (                
                product.category_id,
                product.name,
                product.description,
                product.price,
                product.stock,
                product.image_url,
                product.date_added,
                product.is_available,
                product.is_archived,
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
    def get_product(product_id: str) -> "Product":
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM product WHERE product_id = %s"
            value =(product_id,)
            cursor.execute(sql,value)
            row = cursor.fetchone()

            if row is None:
                return None
            
            new_product = Product(row["product_id"], row["category_id"], row["name"], row["description"], row["price"], row["stock"], row["image_url"], row["date_added"], row["is_available"], row["is_archived"]) 
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
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM product WHERE is_archived = False"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                #Creating product objects for each row fetched for database
                new_product = Product(row["product_id"], row["category_id"], row["name"], row["description"], row["price"], row["stock"], row["image_url"], row["date_added"], row["is_available"], row["is_archived"]) 
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
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM product WHERE is_archived = True"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                #Creating product objects for each row fetched for database
                new_product = Product(row["product_id"], row["category_id"], row["name"], row["description"], row["price"], row["stock"], row["image_url"], row["date_added"], row["is_available"], row["is_archived"]) 
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
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "UPDATE product SET is_archived = True WHERE product_id = %s"    
            value = (product_id,)   
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
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "UPDATE product SET is_archived = False WHERE product_id = %s"    
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