# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"          
DB_PORT = "3306"               
DB_NAME = "bazar_kori"

DATABASE_URL = f"mysql+mysqlconnector://root:@localhost:3306/bazar_kori"

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
