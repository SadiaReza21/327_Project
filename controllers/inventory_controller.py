import threading
import time
from fastapi import HTTPException
from sqlalchemy.orm import Session
from controllers.product_controller import get_product_by_id
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


def restock_product(db: Session, product_id: int, additional_stock: int):
    """
    Add stock to an existing product.
    
    Args:
        db (Session): SQLAlchemy session
        product_id (int): ID of the product to restock
        additional_stock (int): Amount of stock to add

    Returns:
        Product: Updated product object
    """
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if additional_stock < 0:
        raise HTTPException(status_code=400, detail="Stock to add must be positive")
    
    product.stock += additional_stock
    db.commit()
    db.refresh(product) 
    return product


def background_inventory_loop():
    """Runs forever, every 5 seconds."""
    while True:
        db = SessionLocal()
        try:
            update_inventory_status(db)
        finally:
            db.close()
        time.sleep(5)
