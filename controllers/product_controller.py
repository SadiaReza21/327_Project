from sqlalchemy.orm import Session
from models.product import Product

def get_all_products(db: Session):
    """
    Retrieve all products from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[Product]: List of all Product objects.
    """
    products = db.query(Product).all()
    return products


def get_product_by_id(db: Session, product_id: int):
    """
    Fetch a single product by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        product_id (int): ID of the product to retrieve.

    Returns:
        Product | None: Product object if found, else None.
    """

    return db.query(Product).filter(Product.product_id == product_id).first()



def fetch_products_by_category(db: Session, category_id: int):
    """
    Retrieve all products belonging to a specific category.

    Args:
        db (Session): SQLAlchemy database session.
        category_id (int): ID of the category to filter products.

    Returns:
        list[Product]: List of Product objects in the given category.
    """
    return db.query(Product).filter(Product.category_id == category_id).all()


def check_product_status(db: Session):
    """
    Update product availability and archive flags based on stock.

    Rules applied:
        - stock == 0 → is_available = False, is_archived = True
        - stock > 0  → is_available = True,  is_archived = False

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Message confirming that product statuses have been checked and updated.
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


