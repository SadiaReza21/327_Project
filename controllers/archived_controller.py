from sqlalchemy.orm import Session
from models.archived import Archived
from models.product import Product


def sync_archive(db: Session):
    """
    Synchronize the Archived table based on the Product table's archive status.

    Iterates through all products and ensures the Archived table
    reflects the current state:
      - If a product is marked as archived (`is_archived=True`) but not in
        the Archived table, it is added.
      - If a product is available again (`is_available=True`) and exists in
        the Archived table, it is removed.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing a message confirming the archive has been synced.
    """

    products = db.query(Product).all()

    for p in products:
        archived_item = (
            db.query(Archived).filter(Archived.product_id == p.product_id).first()
        )

        if p.is_archived and not archived_item:
            new_arch = Archived(
                product_id=p.product_id, name=p.name, stock=p.stock, is_archived=True
            )
            db.add(new_arch)

        if p.is_available and archived_item:
            db.delete(archived_item)

    db.commit()
    return {"message": "Archive synced"}
