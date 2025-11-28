import mysql.connector
from mysql.connector import Error

# Database Conncetion
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "bazarkori_db"  
}

def get_db_connection():
    """
    Centralized DB connection function.
    Always returns a new MySQL connection.
    """
    return mysql.connector.connect(**DB_CONFIG)