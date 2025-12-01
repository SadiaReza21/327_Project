# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"          # or your MySQL server host
DB_PORT = "3306"               # default MySQL port
DB_NAME = "bazarkori_db"

DATABASE_URL = f"mysql+mysqlconnector://root:@localhost:3306/bazarkori_db"

engine = create_engine(
    DATABASE_URL,
    echo=True,          
    future=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
