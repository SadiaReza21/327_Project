import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any
from datetime import date, datetime

# Database Conncetion
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "bazarkori_db"  
}

class Category:

    def __init__(self, id: int, name: str):
        self.category_id = id
        self.category_name = name

    @staticmethod
    def get_category_dict() -> dict[int, str]:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT category_id, category_name FROM category"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            return {row["category_id"]: row["category_name"] for row in rows}
            
        except Error as e:
            print(f"Category get_list error: {e}")
            return {}
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()   

class Product:

    def __init__(
            self, product_id: int , category_id: int , name: str , description: str, price: float, stock: int, 
            image: str, date_added: date, is_available: bool):
        self.product_id: int = product_id
        self.category_id: int = category_id
        self.name: str = name
        self.description: str = description or ""
        self.price: float = price
        self.stock: int = stock
        self.image_url: str = image
        self.date_added: date = date_added
        self.is_available: bool = is_available

    @staticmethod
    def create_product(product: "Product") -> bool:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            sql = """
                INSERT INTO product 
                (product_id, category_id, name, description, price, stock, image_url, date_added, is_available)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                product.is_available
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
    def get_product_list() -> List["Product"]:
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM product"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                #Creating product objects for each row fetched for database
                new_product = Product(row["product_id"], row["category_id"], row["name"], row["description"], row["price"], row["stock"], row["image_url"], row["date_added"], row["is_available"]) 
                result.append(new_product)
            return result
            
        except Error as e:
            print(f"Product get_list error: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()