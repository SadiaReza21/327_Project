from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Controller.add_product_controller import router
from Model.data_classes import Product, Category


app = FastAPI()

app.include_router(router)

templates = Jinja2Templates(directory=".")

app.mount("/ProductImages", StaticFiles(directory="ProductImages"), name="product_images")

@app.get("/")
async def root(request: Request):
    product_list = Product.get_product_list()
    category_list = Category.get_category_dict() 
    return templates.TemplateResponse(
        "View/admin_dashboard.html", 
        {"request": request, "products": product_list, "categories": category_list}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)