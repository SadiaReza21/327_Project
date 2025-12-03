import mysql.connector
from mysql.connector import Error

def get_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="bazarkori_db"
        )
        cursor = conn.cursor(dictionary=True)
        yield cursor
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print("Error connecting to MySQL:", e)
        raise e
