from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.inventory_controller import get_products_in_inventory
from db.database import get_db
from schemas.product import ProductResponse
from controllers.product_controller import (
    get_product_by_id,
    get_all_products,
    fetch_products_by_category,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/get_products", response_model=list[ProductResponse])
def fetch_all_products(db: Session = Depends(get_db)):
    """Retrieve all products from the database.

    Args:
        db (Session, optional): SQLAlchemy database session injected by Depends.

    Returns:
        list[ProductResponse]: List of all Product objects.
    """
    products = get_all_products(db)
    return products


@router.get("/get_product_by_id/{product_id}")
def fetch_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Fetch a single product by its ID.

    Args:
        product_id (int): ID of the product to retrieve.
        db (Session, optional): SQLAlchemy database session injected by Depends.

    Returns:
        ProductResponse: Product object if found.

    Raises:
        HTTPException: 404 if product is not found.
    """
    product = get_product_by_id(db, product_id)
    return product


@router.get("/category/{category_id}", response_model=list[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    """Retrieve all products belonging to a specific category.

    Args:
        category_id (int): ID of the category to filter products.
        db (Session, optional): SQLAlchemy database session injected by Depends.

    Returns:
        list[ProductResponse]: List of Product objects in the given category.

    Raises:
        HTTPException: 404 if no products are found in the category.
    """
    products = fetch_products_by_category(db, category_id)
    if not products:
        raise HTTPException(
            status_code=404, detail="No products found for this category"
        )
    return products
