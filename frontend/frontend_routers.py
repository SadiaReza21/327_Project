from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from controllers import product_controller, category_controller, inventory_controller
from db.database import get_db


router = APIRouter()

templates = Jinja2Templates(directory="frontend")


# router for home page
@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    """
    Render the home page with available products and categories.

    Args:
        request (Request): FastAPI request object for Jinja2 templates.
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        HTMLResponse: Renders the home page with products and categories.
    """
    products = inventory_controller.get_products_in_inventory(db)
    categories = category_controller.get_all_categories(db)
    return templates.TemplateResponse(
        "home_page.html",
        {"request": request, "products": products, "categories": categories},
    )


# router for logged-in buyer home page
@router.get("/home/{buyer_id}")
def home_buyer(request: Request, buyer_id: int, db: Session = Depends(get_db)):
    """
    Render the home page for a logged-in buyer, showing available products and categories.

    Args:
        request (Request): FastAPI request object for Jinja2 templates.
        buyer_id (int): ID of the logged-in buyer.
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        HTMLResponse: Renders the home page with products, categories, and buyer info.
    """
    products = inventory_controller.get_products_in_inventory(db)
    categories = category_controller.get_all_categories(db)

    return templates.TemplateResponse(
        "logged_in_home_page.html",
        {
            "request": request,
            "products": products,
            "categories": categories,
            "buyer_id": buyer_id,
        },
    )


# router for product details page
@router.get("/product/{product_id}")
def product_details(
    request: Request, product_id: int, buyer_id: int, db: Session = Depends(get_db)
):
    """
    Render the product details page for a specific product.

    Args:
        request (Request): FastAPI request object for Jinja2 templates.
        product_id (int): ID of the product to display.
        buyer_id (int): ID of the logged-in buyer
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        HTMLResponse: Renders the product details page or a 404 page if the product is not found.
    """
    product = product_controller.get_product_by_id(db, product_id)
    if not product:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": "Product not found"}
        )

    category = category_controller.get_category_by_id(db, product.category_id)
    related_products = product_controller.fetch_products_by_category(
        db, product.category_id
    )

    return templates.TemplateResponse(
        "product_details.html",
        {
            "request": request,
            "product": product,
            "category": category,
            "related_products": related_products,
            "buyer_id": buyer_id,
        },
    )


# router for add category page
@router.get("/add-category")
def add_category(request: Request):
    """
    Render the add category page.

    Args:
        request (Request): FastAPI request object for Jinja2 templates.

    Returns:
        HTMLResponse: Renders the add category page.
    """
    return templates.TemplateResponse("add_category.html", {"request": request})


# router for restock product page
@router.get("/restock-product/{product_id}")
def restock_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    """
    Render the restock product page with product data.

    Args:
        request (Request): FastAPI request object for Jinja2 templates.
        product_id (int): ID of the product to restock.
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        HTMLResponse: Renders the product restock page with product information.
    """
    product_data = product_controller.get_product_by_id(db, product_id)

    return templates.TemplateResponse(
        "product_restock.html", {"request": request, "product": product_data}
    )
