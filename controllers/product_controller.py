from sqlalchemy.orm import Session
from models.product import Product

def get_all_products(db: Session) -> list[Product]:
    """Fetch all products."""
    products = db.query(Product).all()
    return products


def get_product_by_id(db: Session, product_id: int):
    """
    Fetch a single product by its ID.
    Returns None if the product does not exist.
    """
    return db.query(Product).filter(Product.product_id == product_id).first()



def fetch_products_by_category(db: Session, category_id: int) -> list[Product]:
    return db.query(Product).filter(Product.category_id == category_id).all()



