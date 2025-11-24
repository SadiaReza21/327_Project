from fastapi import FastAPI, Form, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import date, datetime
import time
import os
from fastapi import APIRouter
from Model.data_classes import Category, Product

templates = Jinja2Templates(directory=".")
router = APIRouter()

@router.get("/add_product")
def add_product(request: Request):
    # Getting the available category list from database
    category_list = Category.get_category_dict() 
    return templates.TemplateResponse(
        "View/add_product.html", 
        {"request": request, "categories": category_list}
    )

# Receives data from html form
@router.post("/submit_product")
async def submit_product(
    request: Request,
    p_name: str = Form(...),
    p_description: str = Form(...),
    p_price: float = Form(...),
    p_quantity: int = Form(...),
    p_category: str = Form(...),
    product_image: UploadFile = Form(None)  
):
    """
    Adds a new product to database.

    Args:
        request (Request): FastAPI request object.
        p_name (str): Product name.
        p_description (str): Product description.
        p_price (str): Product price.
        p_category (str): Category id.

    Returns:
        TemplateResponse: Rendered thank-you page.
    """

    current_milliseconds = int(time.time() * 1000)
    product_id = current_milliseconds  

    folder_path = f"ProductImages/{product_id}"
    os.makedirs(folder_path, exist_ok=True)

    image_filename = "default.jpg"
    image_url = "ProductImages/default.png"

    if product_image and product_image.filename:
        # 1. sanitize filename
        original_ext = product_image.filename.split(".")[-1].lower()
        if original_ext not in ["jpg", "jpeg", "png", "webp"]:
            raise HTTPException(status_code=400, detail="Invalid image format")

        image_filename = f"{product_id}.{original_ext}"
        file_path = f"{folder_path}/{image_filename}"

        # 2. save image
        content = await product_image.read()
        with open(file_path, "wb") as f:
            f.write(content)

        image_url = f"ProductImages/{product_id}/{image_filename}"  

    new_product = Product(product_id, p_category, p_name, p_description, p_price, p_quantity, image_url, date.today(), True)
    result = Product.create_product(new_product)    

    if(result):
        return templates.TemplateResponse(
                "View/thanks.html", 
                {"request": request,
                "product": new_product}
            )    
    else:
        import shutil
        shutil.rmtree(folder_path, ignore_errors=True)
        return HTMLResponse("""
            <script>
                alert("Error: Could not add product. Please try again.");
                window.location.href = "/add_product"; 
            </script>
        """)


