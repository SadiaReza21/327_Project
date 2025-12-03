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

engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Creates a new database session for use with FastAPI dependencies.

    Yields:
        Session: SQLAlchemy session.

    Example::

        from fastapi import Depends
        from db.database import get_db

        @app.get("/products")
        def read_products(db: Session = Depends(get_db)):
            return db.query(Product).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
