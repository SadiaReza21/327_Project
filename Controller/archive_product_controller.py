from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from Model.product_class import Product

templates = Jinja2Templates(directory=".")
archive_product_router = APIRouter(prefix="/r_archive_product")


@archive_product_router.post("/archive_product")
def archive_product( request: Request,  p_id: str = Form(...)):
    """
    Archives a product in the database.

    Args:
        request (Request): FastAPI request object.
        p_id (str): Product id.

    Returns:
        TemplateResponse: Shows admin_dashbaord.html with success 
        message or error message.
    """
    result = Product.archive_product(p_id)
    if(result):
        return HTMLResponse(f"""
                <script>
                    alert("Product archived successfully!!");
                    window.location.href = "/"; 
                </script>
            """)
    else:
            return HTMLResponse(f"""
                <script>
                    alert("Error: Product archiving failed!!");
                    window.location.href = "/"; 
                </script>
            """)
    

@archive_product_router.post("/unarchive_product")
def unarchive_product( request: Request,  p_id: str = Form(...)):
    """
    Unarchives a product in the database.

    Args:
        request (Request): FastAPI request object.
        p_id (str): Product id.

    Returns:
        TemplateResponse: Shows admin_dashbaord.html with success message
        or error message.
    """
    result = Product.unarchive_product(p_id)
    if(result):
        return HTMLResponse(f"""
                <script>
                    alert("Product unarchived successfully!!");
                    window.location.href = "/"; 
                </script>
            """)
    else:
            return HTMLResponse(f"""
                <script>
                    alert("Error: Product unarchiving failed!!");
                    window.location.href = "/"; 
                </script>
            """)
