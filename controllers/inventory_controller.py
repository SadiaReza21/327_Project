from fastapi import HTTPException
from sqlalchemy.orm import Session
from controllers.product_controller import get_product_by_id
from db.database import SessionLocal
from models.product import Product
from models.inventory import Inventory


def sync_inventory(db: Session):
    """
    Synchronize the Inventory table with the Product table based on product availability.

    For each product:
        - If the product is available and not in Inventory, it is added.
        - If the product is available and already in Inventory, stock and availability are updated.
        - If the product is unavailable and exists in Inventory, it is removed.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing a message confirming the inventory has been synced.
    """
    products = db.query(Product).all()

    for p in products:
        inv = db.query(Inventory).filter(Inventory.product_id == p.product_id).first()

        if p.is_available and p.stock > 0:
            if not inv:
                new_inv = Inventory(
                    product_id=p.product_id,
                    name=p.name,
                    stock=p.stock,
                    is_available=p.is_available,
                )
                db.add(new_inv)
            else:
                inv.stock = p.stock
                inv.is_available = p.is_available

        else:
            if inv:
                db.delete(inv)

    db.commit()
    return {"message": "Inventory synced"}


def get_products_in_inventory(db: Session):
    """
    Retrieve products that are available in both Products and Inventory tables.

    Only includes products that:
        - Are marked as available in Inventory (`is_available=True`)
        - Have stock greater than 0 (`stock > 0`)

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[Product]: List of available Product objects.
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
    Increase the stock of an existing product.

    Args:
        db (Session): SQLAlchemy database session.
        product_id (int): ID of the product to restock.
        additional_stock (int): Amount of stock to add (must be positive).

    Returns:
        Product: The updated Product object.

    Raises:
        HTTPException: 404 if the product is not found.
        HTTPException: 400 if the additional_stock is negative.
    """

    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if additional_stock <= 0:
        raise HTTPException(status_code=400, detail="Stock to add must be positive")

    product.stock += additional_stock
    db.commit()
    db.refresh(product)
    return product
