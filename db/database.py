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
"""
SQLAlchemy engine for connecting to the MySQL database.

Attributes:
    DATABASE_URL (str): Full database URL including user, password, host, port, and database name.
    engine (Engine): SQLAlchemy Engine instance used for database operations.
"""


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Creates a SQLAlchemy session factory.

Attributes:
    SessionLocal (sessionmaker): A factory to create new database sessions.
"""


Base = declarative_base()
"""
Base class for SQLAlchemy models.

All ORM models should inherit from this base class.
"""


def get_db():
    """
    Creates a new database session for use with FastAPI dependencies.

    This function can be used with `Depends` in FastAPI endpoints to provide a session.

    Yields:
        Session: A SQLAlchemy database session.

    Example:
        ```python
        from fastapi import Depends
        from database import get_db

        @app.get("/products")
        def read_products(db: Session = Depends(get_db)):
            return db.query(Product).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
