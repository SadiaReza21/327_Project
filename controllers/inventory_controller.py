from fastapi import HTTPException
from sqlalchemy.orm import Session
from controllers.product_controller import get_product_by_id
from db.database import SessionLocal
from models.product import Product
from models.inventory import Inventory


def sync_inventory(db: Session):
    """
    Sync Inventory table with Product table based on availability.
    """
    products = db.query(Product).all()

    for p in products:
        inv = db.query(Inventory).filter(Inventory.product_id == p.product_id).first()

        if p.is_available:
            # Add if missing
            if not inv:
                new_inv = Inventory(
                    product_id=p.product_id,
                    name=p.name,
                    stock=p.stock,
                    is_available=p.is_available,
                )
                db.add(new_inv)
            else:
                # Update values
                inv.stock = p.stock
                inv.is_available = p.is_available

        else:
            # Product unavailable → remove from inventory
            if inv:
                db.delete(inv)

    db.commit()
    return {"message": "Inventory synced"}


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

 