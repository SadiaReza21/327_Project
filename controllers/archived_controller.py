from sqlalchemy.orm import Session
from models.archived import Archived
from models.product import Product


def sync_archive(db: Session):
    """
    Sync Archived table based on Product archive status.
    """
    products = db.query(Product).all()

    for p in products:
        archived_item = db.query(Archived).filter(
            Archived.product_id == p.product_id
        ).first()

        # Add to archive if flagged but not present
        if p.is_archived and not archived_item:
            new_arch = Archived(
                product_id=p.product_id,
                name=p.name,
                stock=p.stock,
                is_archived=True
            )
            db.add(new_arch)

        # Remove from archive if product is available again
        if p.is_available and archived_item:
            db.delete(archived_item)

    db.commit()
    return {"message": "Archive synced"}




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
