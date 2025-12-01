from sqlalchemy.orm import Session
from models.archived import Archived


def get_archived_product_by_id(db: Session, product_id: int):
    """
    Fetch a single archived product by its ID.
    Returns None if the product does not exist in the archived table.
    """
    return db.query(Archived).filter(Archived.product_id == product_id).first()


def get_products_in_archived(db: Session):
    """
    Return products that are in the Archived table.
    Only includes archived products.
    """
    archived_products = (
        db.query(Archived)
        .filter(Archived.is_archived == True, Archived.stock > 0)
        .all()
    )
    return archived_products
