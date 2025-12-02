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
    """
    Retrieve all products from the database.

    :param db: SQLAlchemy database session (injected by Depends).
    :type db: Session
    :return: List of all Product objects.
    :rtype: list[ProductResponse]
    """
    products = get_all_products(db)
    return products


@router.get("/get_product_by_id/{product_id}")
def fetch_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single product by its ID.

    :param product_id: ID of the product to retrieve.
    :type product_id: int
    :param db: SQLAlchemy database session (injected by Depends).
    :type db: Session
    :return: Product object if found.
    :rtype: ProductResponse
    :raises HTTPException: 404 if product is not found.
    """
    product = get_product_by_id(db, product_id)
    return product


@router.get("/category/{category_id}", response_model=list[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all products belonging to a specific category.

    :param category_id: ID of the category to filter products.
    :type category_id: int
    :param db: SQLAlchemy database session (injected by Depends).
    :type db: Session
    :return: List of Product objects in the given category.
    :rtype: list[ProductResponse]
    :raises HTTPException: 404 if no products are found in the category.
    """
    products = fetch_products_by_category(db, category_id)
    if not products:
        raise HTTPException(
            status_code=404, detail="No products found for this category"
        )
    return products
