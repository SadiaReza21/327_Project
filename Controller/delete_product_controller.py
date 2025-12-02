from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from Model.product_class import Product

templates = Jinja2Templates(directory=".")
delete_product_router = APIRouter(prefix="/r_delete_product")


@delete_product_router.post("/delete_product")
def archive_product( request: Request,  p_id: str = Form(...)):
    """
    Deleted the product from the database.

    Args:
        request (Request): FastAPI request object.
        p_id (str): Product id.

    Returns:
        TemplateResponse: Shows admin_dashbaord.html with success 
        message or error message.
    """
    result = Product.delete_product(p_id)
    if(result):
        return HTMLResponse(f"""
                <script>
                    alert("Product deleted successfully!!");
                    window.location.href = "/"; 
                </script>
            """)
    else:
            return HTMLResponse(f"""
                <script>
                    alert("Error: Product deletion failed!!");
                    window.location.href = "/"; 
                </script>
            """)