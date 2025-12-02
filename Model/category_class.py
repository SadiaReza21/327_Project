from database_connection import get_db_connection
from mysql.connector import Error

class Category:


    def __init__(self, id: int, name: str):
        self.category_id = id
        self.category_name = name


    @staticmethod
    def get_category_dict() -> dict[int, str]:
        """
        Fetches all category id - name pair from the database and returns 
        them as a dictionary.

        Returns:
            TemplateResponse: Returns a dictionary of category id - name pair.
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT category_id, category_name FROM categories"
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

