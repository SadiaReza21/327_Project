import threading
import time
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.archived import Archived
from models.product import Product
from models.inventory import Inventory


def update_inventory_status(db: Session):
    """
    Update Inventory table based on Products table.
    Removes out-of-stock/unavailable products and updates stock values.
    """
    products = db.query(Product).all()

    for p in products:
        inv = db.query(Inventory).filter(Inventory.product_id == p.product_id).first()

        if p.stock > 0:
            if not inv:
                # Add new product to inventory
                inv = Inventory(
                    product_id=p.product_id,
                    name=p.name,
                    stock=p.stock,
                    is_available=p.is_available,
                )
                db.add(inv)
            else:
                # Update existing product
                inv.stock = p.stock
                inv.is_available = p.is_available
        else:
            # Remove unavailable/out-of-stock product from inventory
            if inv:
                # Move to archived first
                archived_item = Archived(
                    product_id=inv.product_id,
                    name=inv.name,
                    stock=inv.stock,
                    is_archived=True
                )
                db.add(archived_item)  # SQLAlchemy inserts into `archived` table
                db.delete(inv)  # SQLAlchemy deletes from `inventories` table
                p.is_archived = True
                p.is_available = False

    db.commit()
    return {"message": "Inventory updated"}


def get_products_in_inventory(db: Session):
    """
    Return products that are both in the Products table
    and available in the Inventory table.
    """
    products = (
        db.query(Product)
        .join(Inventory, Product.product_id == Inventory.product_id)
        .filter(Inventory.is_available == True, Inventory.stock > 0)
        .all()
    )
    return products


def background_inventory_loop():
    """Runs forever, every 5 seconds."""
    while True:
        db = SessionLocal()
        try:
            update_inventory_status(db)
        finally:
            db.close()
        time.sleep(5)
