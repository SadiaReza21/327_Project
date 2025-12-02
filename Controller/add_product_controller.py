from fastapi import FastAPI, Form, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import date
import time
import os
from fastapi import APIRouter
from Model.category_class import Category
from Model.product_class import Product

templates = Jinja2Templates(directory=".")
add_product_router = APIRouter(prefix="/r_add_product")


@add_product_router.get("/add_product")
def add_product(request: Request):
    """
    Displays the add product page.

    Args:
        request (Request): FastAPI request object

    Returns:
        TemplateResponse: Shows add_product.html with category options 
        from database.
    """
    category_list = Category.get_category_dict() 
    return templates.TemplateResponse(
        "View/add_product.html", 
        {"request": request, "categories": category_list}
    )



# Receives data from html form
@add_product_router.post("/submit_product")
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
    Adds a new product to database by calling functions.

    Args:
        request (Request): FastAPI request object.
        p_name (str): Product name.
        p_description (str): Product description.
        p_price (str): Product price.
        p_quantity (int): Product quantity in stock.
        p_category (str): Category id.
        product_image (file): One image of the product

    Returns:
        TemplateResponse: Shows admin_dashbaord.html if product is added 
        successfully. Otherwise shows the add_product.html 
        with an error message.
    """

    current_milliseconds = int(time.time() * 1000)
    product_id = current_milliseconds

    # Default image and name if picture is not added
    image_filename = "default.png"
    image_url = "ProductImages/default.png"

    folder_path = ""

    if product_image and product_image.filename:

        folder_path = f"ProductImages/{product_id}"
        os.makedirs(folder_path, exist_ok=True)

        # Checking file type and filename
        original_ext = product_image.filename.split(".")[-1].lower()
        if original_ext not in ["jpg", "jpeg", "png", "webp"]:
            return HTMLResponse("""
                <script>
                    alert("Error: Invalid Image Format!! Please try again!");
                    window.location.href = "/r_add_product/add_product"; 
                </script>
            """)

        # Making folder with product id for image
        image_filename = f"{product_id}.{original_ext}"
        file_path = f"{folder_path}/{image_filename}"

        # Save the image in that folder
        content = await product_image.read()
        with open(file_path, "wb") as f:
            f.write(content)

        image_url = f"ProductImages/{product_id}/{image_filename}"  

    new_product = Product(
        product_id, p_category, p_name, p_description, 
        p_price, p_quantity, image_url, date.today(), True, False)
    result = Product.create_product(new_product)    

    if(result):
        return HTMLResponse("""
            <script>
                alert("Product added successfully!!");
                window.location.href = "/"; 
            </script>
        """)  
    else:
        if folder_path != "" :
            import shutil
            shutil.rmtree(folder_path, ignore_errors=True)
        return HTMLResponse("""
            <script>
                alert("Error: Could not add product!! Please try again!");
                window.location.href = "/r_add_product/add_product"; 
            </script>
        """)


