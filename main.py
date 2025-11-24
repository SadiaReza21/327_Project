from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Controller.add_product_controller import router


app = FastAPI()

app.include_router(router)

templates = Jinja2Templates(directory=".")

app.mount("/ProductImages", StaticFiles(directory="ProductImages"), name="product_images")

@app.get("/")
async def root():
    html_content = open("View/admin_dashboard.html", "r", encoding="utf-8").read()
    return HTMLResponse(html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)