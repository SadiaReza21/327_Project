import threading
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from controllers.inventory_controller import background_inventory_loop
from views.product_routers import router as product_router
from views.category_routers import router as category_router
from views.inventory_routers import router as inventory_router
from frontend.frontend_routers import router as frontend_router


app = FastAPI(
    title="My FastAPI App",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all headers
)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(frontend_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(inventory_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Bazar Kori API"}


@app.on_event("startup")
def start_background_task():
    thread = threading.Thread(target=background_inventory_loop, daemon=True)
    thread.start()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)