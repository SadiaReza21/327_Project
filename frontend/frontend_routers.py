from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import httpx
from controllers import product_controller, category_controller, inventory_controller
from db.database import get_db


router = APIRouter()

# Templates for home and products
templates = Jinja2Templates(directory="frontend")


@router.get("/home")
def home(request: Request, db: Session = Depends(get_db)):
    products = inventory_controller.get_products_in_inventory(db)
    categories = category_controller.get_all_categories(db)
    return templates.TemplateResponse(
        "home_page.html",
        {"request": request, "products": products, "categories": categories},
    )


@router.get("/product/{product_id}")
def product_details(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = product_controller.get_product_by_id(db, product_id)
    if not product:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": "Product not found"}
        )

    category = category_controller.get_category_by_id(db, product.category_id)
    related_products = product_controller.fetch_products_by_category(db, product.category_id)

    return templates.TemplateResponse(
        "product_details.html",
        {"request": request, "product": product, "category": category, "related_products": related_products},
    )

@router.get("/add-category")
def add_category(request: Request):
    return templates.TemplateResponse(
        "add_category.html",
        {"request": request}
    )    


@router.get("/restock-product/{product_id}")
def restock_product_modal(request: Request, product_id: int, db: Session = Depends(get_db)):
    """
    Fetch product data and render the restock modal page.
    """
    product_data = product_controller.get_product_by_id(db, product_id)

    return templates.TemplateResponse(
        "product_restock.html",
        {"request": request, "product": product_data}
    ) 
