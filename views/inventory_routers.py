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
    Return all products that are both in Products table
    and available in Inventory table.
    """
    products = get_products_in_inventory(db)
    return products


class RestockRequest(BaseModel):
    product_id: int
    additional_stock: int

@router.put("/restock", response_model=ProductResponse)
def restock_product_in_inventory(request: RestockRequest, db: Session = Depends(get_db)):
    """
    Add stock to a product and return the updated product.
    """
    updated_product = restock_product(db, request.product_id, request.additional_stock)
    return updated_product