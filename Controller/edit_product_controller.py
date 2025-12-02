from fastapi import FastAPI, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from fastapi import APIRouter
import os
from Model.product_class import Product
from Model.category_class import Category

templates = Jinja2Templates(directory=".")
edit_product_router = APIRouter(prefix="/r_edit_product")


@edit_product_router.get("/edit_product")
def edit_product( request: Request,  p_id: str):
    """
    Displays edit product page with existing product's information that was 
    fetched by the corresponding product's id.

    Args:
        request (Request): FastAPI request object.
        p_id (str): Product id.

    Returns:
        TemplateResponse: Shows edit_product.html with the product's existing
        information fetched from database.
    """
    existing_product = Product.get_product(p_id)
    category_list = Category.get_category_dict() 
    return templates.TemplateResponse(
        "View/edit_product.html", 
        {
            "request": request, "product": existing_product, 
            "categories": category_list
        }
    )


@edit_product_router.post("/update_product")
async def update_product(
        request: Request,
        p_id: str = Form(...),
        p_name: str = Form(...),
        p_description: str = Form(...),
        p_price: float = Form(...),
        p_quantity: int = Form(...),
        p_category: str = Form(...),
        prev_product_image: str = Form(...),
        product_image: UploadFile = Form(None)  
    ):
    """
    Updates an existing product's information in the database. 
    Replaces the older image if a new one is chosen.

    Args:
        request (Request): FastAPI request object.
        p_id (Str): Product id of the targeted product.
        p_name (str): Product name.
        p_description (str): Product description.
        p_price (str): Product price.
        p_quantity (int): Product quantity in stock.
        p_category (str): Category id.
        prev_product_image (str): URL of the product's existing image.
        product_image (file): New image of the product

    Returns:
        TemplateResponse: Shows admin_dashbaord.html if update is successfull.
        Otherwise shows edit_product.html with an error message.
    """
    image_filename = "default.png"
    image_url = prev_product_image

    folder_path = ""

    if product_image and product_image.filename:

        folder_path = f"ProductImages/{p_id}"
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
        image_filename = f"{p_id}.{original_ext}"
        file_path = f"{folder_path}/{image_filename}"

        # Save the image in that folder
        content = await product_image.read()
        with open(file_path, "wb") as f:
            f.write(content)

        image_url = f"ProductImages/{p_id}/{image_filename}"  

    new_product = Product(
        p_id, p_category, p_name, p_description, p_price, p_quantity, 
        image_url, date.today(), True, False)
    result = Product.update_product(new_product)

    if(result):
        return HTMLResponse("""
            <script>
                alert("Product updated successfully!!");
                window.location.href = "/"; 
            </script>
        """)  
    else:  
        return HTMLResponse("""
            <script>
                alert("Error: Could not update product!! Please try again!");
                window.location.href = 
                    "/r_edit_product/edit_product?p_id={{ p_id }}"; 
            </script>
        """)
