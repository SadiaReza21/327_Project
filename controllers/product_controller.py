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


def check_product_status(db: Session):
    """
    Sync product flags based on their stock.
    stock == 0  → is_available = False, is_archived = True
    stock > 0   → is_available = True,  is_archived = False
    """
    products = db.query(Product).all()

    for p in products:
        if p.stock > 0:
            p.is_available = True
            p.is_archived = False
        else:
            p.is_available = False
            p.is_archived = True

    db.commit()
    return {"message": "Product status checked"}


