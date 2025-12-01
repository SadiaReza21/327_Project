from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.inventory_controller import get_products_in_inventory
from db.database import get_db
from schemas.product import ProductResponse

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/available", response_model=list[ProductResponse])
def available_products(db: Session = Depends(get_db)):
    """
    Return all products that are both in Products table
    and available in Inventory table.
    """
    products = get_products_in_inventory(db)
    return products