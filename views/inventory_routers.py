from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from controllers.inventory_controller import get_products_in_inventory, restock_product
from db.database import get_db
from models.product import Product
from schemas.product import ProductResponse

router = APIRouter(prefix="/inventories", tags=["Inventories"])


@router.get("/available", response_model=list[ProductResponse])
def available_products(db: Session = Depends(get_db)):
    """
    Retrieve all products that are both in the Products table and available in Inventory.

    Args:
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        list[ProductResponse]: List of available Product objects.
    """
    products = get_products_in_inventory(db)
    return products


class RestockRequest(BaseModel):
    """
    Request model for restocking a product.

    Attributes:
        product_id (int): ID of the product to restock.
        additional_stock (int): Amount of stock to add (must be positive).
    """

    product_id: int
    additional_stock: int


@router.put("/restock", response_model=ProductResponse)
def restock_product_in_inventory(
    request: RestockRequest, db: Session = Depends(get_db)
):
    """
    Increase the stock of a product and return the updated product.

    Args:
        request (RestockRequest): Restock request containing `product_id` and `additional_stock`.
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        ProductResponse: The updated Product object.

    Raises:
        HTTPException: 404 if the product does not exist.
        HTTPException: 400 if `additional_stock` is negative.
    """
    updated_product = restock_product(db, request.product_id, request.additional_stock)
    return updated_product
