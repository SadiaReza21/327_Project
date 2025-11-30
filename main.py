from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Model.category_class import Category
from Model.product_class import Product
from Controller.add_product_controller import add_product_router
from Controller.archive_product_controller import archive_product_router
from Controller.edit_product_controller import edit_product_router


app = FastAPI()

app.include_router(add_product_router)
app.include_router(archive_product_router)
app.include_router(edit_product_router)

templates = Jinja2Templates(directory="View")

app.mount("/ProductImages", StaticFiles(directory="ProductImages"), name="product_images")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    product_list = Product.get_unarchived_product_list()
    archived_product_list = Product.get_archived_product_list()
    category_list = Category.get_category_dict() 
    return templates.TemplateResponse(
        "admin_dashboard.html", 
        {"request": request, "products": product_list, "archived_products": archived_product_list, "categories": category_list}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)